"""
BIER GeoHub Backup

Written by: Michael Dykes (michael.dykes@gov.bc.ca)
Created: July 26 2022
Refactored: March 12 2026

Purpose
-------
Backs up ArcGIS Online item JSON configurations for specific users
and uploads them to S3 Object Storage.

Items backed up include:
    - Web Maps
    - Dashboards
    - Hub Pages
    - Hub Sites
    - StoryMaps
    - Experience Builder apps
    - Web Mapping Applications

Only the **JSON configuration** of items is backed up, not datasets.
"""

# -------------------------
# Import libraries
# -------------------------
import os
import sys
import json
import logging
import tempfile
import re

from arcgis import GIS
from minio import Minio

# -------------------------
# Logging configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("geohub-backup")

# -------------------------
# Load configuration file
# -------------------------
# config.json must exist in the same folder as the script
config_file = os.path.join(os.path.dirname(__file__), "config.json")

with open(config_file) as json_conf:
    CONF = json.load(json_conf)

# ------------------------------------------------
# Configuration values (non-sensitive)
# ------------------------------------------------
PORTAL_URL = CONF["AGO_Portal_URL"]
REST_ENDPOINT = CONF["S3_REST_Endpoint"]
S3_URL = CONF["S3_URL"]
BUCKET_NAME = CONF["S3_BUCKET"]
FOLDER_PATH = CONF["S3_FolderPath"]

AGO_MAX_ITEMS = CONF.get("AGO_Max_Items", 5000)

PART_SIZE = 15728640

# Item types to back up
BACKUP_ITEM_TYPES = [
    "Web Map",
    "Dashboard",
    "Hub Page",
    "Hub Site Application",
    "StoryMap",
    "Web Experience",
    "Web Mapping Application"
]

# ------------------------------------------------
# Load credentials from environment variables
# ------------------------------------------------
PORTAL_USERNAME = os.getenv("AGO_USERNAME")
PORTAL_PASSWORD = os.getenv("AGO_PASSWORD")

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")

missing = []

if not PORTAL_USERNAME:
    missing.append("AGO_USERNAME")

if not PORTAL_PASSWORD:
    missing.append("AGO_PASSWORD")

if not S3_ACCESS_KEY:
    missing.append("S3_ACCESS_KEY")

if not S3_SECRET_KEY:
    missing.append("S3_SECRET_KEY")

if missing:
    log.error(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

# ------------------------------------------------
# Connect to ArcGIS Online
# ------------------------------------------------

log.info("Connecting to ArcGIS Online...")

try:
    gis = GIS(PORTAL_URL, username=PORTAL_USERNAME, password=PORTAL_PASSWORD, expiration=9999)
except Exception as e:
    log.error(f"Failed to connect to ArcGIS Online: {e}")
    sys.exit(1)


# ------------------------------------------------
# Connect to S3 Object Storage
# ------------------------------------------------

log.info("Connecting to S3 Object Storage...")

try:
    s3 = Minio(REST_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY)
except Exception as e:
    log.error(f"Failed to connect to S3: {e}")
    sys.exit(1)


# ------------------------------------------------
# Helper Functions
# ------------------------------------------------

def sanitize_filename(title):
    """
    Clean item titles so they can safely be used as filenames.
    """
    return re.sub(r"[^\w\-_\. ]", "_", title)


def create_temp_json_backup(item):
    """
    Retrieve the JSON configuration of an AGO item
    and write it to a temporary file.
    """
    try:
        item_data = item.get_data()

        if not item_data:
            log.warning(f"{item.title} has no JSON configuration.")
            return None

        tfile = tempfile.NamedTemporaryFile(mode="w", delete=False)

        json.dump(item_data, tfile)

        tfile.flush()
        tfile.close()

        return tfile

    except Exception as e:
        log.error(f"Failed to retrieve JSON for {item.title}: {e}")
        return None


def upload_backup(file_path, item_type, filename):
    """
    Upload backup file to S3.
    """
    object_path = f"{FOLDER_PATH}/{item_type}/{filename}"

    try:

        s3.fput_object(
            BUCKET_NAME,
            object_path,
            file_path,
            part_size=PART_SIZE
        )

        log.info(f"Uploaded: {filename}")

    except Exception as e:
        log.error(f"Upload failed for {filename}: {e}")

# ------------------------------------------------
# Determine logged-in user
# ------------------------------------------------
try:
    current_user = gis.users.me.username
    log.info(f"Running backup for logged-in user: {current_user}")
except Exception as e:
    log.error(f"Unable to determine logged-in user: {e}")
    sys.exit(1)


# ------------------------------------------------
# Backup Process
# ------------------------------------------------
user = current_user
log.info(f"Processing user: {user}")

for item_type in BACKUP_ITEM_TYPES:
    log.info(f"Searching for {item_type} items...")

    try:
        items = gis.content.search(
            query=f"owner:{user}",
            item_type=item_type,
            max_items=AGO_MAX_ITEMS
        )

    except Exception as e:
        log.error(f"Search failed for {item_type}: {e}")
        continue

    for item in items:
        title = item.title

        # Skip backup or copied items
        if "backup" in title.lower() or "copy" in title.lower():
            continue

        safe_title = sanitize_filename(title)

        # Include item ID to avoid filename collisions
        filename = f"{safe_title}_{item.id}.json"

        log.info(f"Backing up: {title}")

        temp_file = create_temp_json_backup(item)

        if not temp_file:
            continue

        try:
            upload_backup(
                temp_file.name,
                item_type,
                filename
            )

        finally:
            # Remove temp file
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)