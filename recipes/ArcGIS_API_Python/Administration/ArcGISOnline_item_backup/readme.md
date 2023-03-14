# Backing ArcGIS Online Applications

## Overview
This script allows you to backup ArcGIS Online applications (webmaps, dashboard, experience builder, storymaps, etc) to multiple different locations with different retention policies.\
For example, your group may want to back up the most recent version of everything to working storage (W:), and archive many older versions to archive (S:).

## Usage
You will need to configure the script with the following parameters:\
>`maphub_accounts`: A list of accounts whos items will be backed up. The items must be shared with the login account.\
`max_search`: maximum items. Default is fine. It can be lowered if needed.\
`folders`: The folders and retention policy (`"max_backups"`) for each. Structured as nested dictionaries, this allows for multiple backup locations to be used.\
`"max_backups"`: Defines how many backups to be kept. This is NOT a time period. It is an absolute number.\
`backup_types`: A white list of item types to backup from ArcGIS Online. If new item types are added by ESRI, they can be added here.\
`# Credentials`: Add your username and password authentication routine here.

Once configured, this script can be run to create a backup in the specified locations. The backups will be formatted as such: yyyy_mm_dd\ItemName_itemID.json.
This should make it easy to find by date, item name, or item ID.

<br>

This script can be set up to run as a weekly/monthly job via Jenkins or whichever automation setup you use.





