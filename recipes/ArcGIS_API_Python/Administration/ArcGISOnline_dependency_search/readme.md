# ArcGIS Online Dependency Checker
Isaac Cave, South Coast Region
April 11, 2023

## Overview
This script checks every item in a list of accounts and checks where it is being used across a selection of item types. It outputs a spreadsheet with a list of items and a number of fields including name, groups, usage (dependent) locations. \
The primary intent is to build a relationship between items in ArcGIS Online, and to allow users to know when an item isn't being used and can be deleted.

## Usage
The script requires the following parameters:

> ### Parameters
> `# Credentials` : Add your *credentials* and *url* to this section with your preferred login method\
> `maphub_accounts`: The list of accounts to check items for. Items must be shared with the credentials account.\
> `max_search` : Maximum number of items. Lower this if you want to test the script\
> `host_types` : The type of items to check dependencies for\
> `dependent_types` : Where to check for the dependencies. Essentially the `host_types` list without `"Feature Service"`\
> `url_base` : The url used for building the Item URL template. Currently uses the login url from the credentials. \
> `url_template` : The finished url for the Item URL in the final output. currently appends `"/home/item.html?id="` to the url \
> `csv_location` : Where the output csv will be located. Name will be `Dependencies_yyyy_mm_dd.csv` \
> `retention` : How many result spreadsheets to keep

There may be a number of relevant limitations. The script may not find all usages in all cases.
> ### Limitations
> Note that the script checks for usage in all items/apps that are **shared with the logged in account**. It only records the owner, it doesn't filter by owner in any way. As such, it may not record if another user's WebMap uses the account's Feature Service if that WebMap isn't shared (for example).\
>  \
> Not all groups will be found. ArcGIS Online will intermitently (3% of cases) throw an error 403 when querying the group name. The group name will be `UNKNOWN` when this happens. \
> This tool does not support all item types. It is not able to search for item usage inside Notebooks, Survey123, or custom items.

Once configured, this script can be run directly, or automated to run in Jenkins. It may take a long time. For 2100 items checked across 1650 usage locations in MapHub, the runtime was 93 minutes. This script should only be run 1-4 times a year (ex. quarterly, end of fiscal)

## Details of output
### Field Description

| Field                    | Description                                                                             |
|--------------------------|-----------------------------------------------------------------------------------------|
| Item Title               | The name of the item                                                                    |
| Item ID                  | item ID of the item                                                                     |
| Item URL                 | URL, to navigate to the item on maphub (currently hardcoded formula)                    |
| Item Owner               | The owner of the item                                                                   |
| Item Type                | Item type (feature service, webmap, etc)                                                |
| Groups                   | Comma separated list of groups the item is a member of. Some groups will be UNKNOWN     |
| Dependent App Names      | Comma separated list of items/apps that use the item                                    |
| Dependent App IDs        | Comma separeted list of item IDs that use the item                                      |
| Dependent App Owners     | Comma separated list of users who are using the item in an app                          |
| Dependent App Count      | Count of the number of locations/apps the item is being used in                         |

The fields are provided to facilitate filtering and searching for items by properties.

### Verified application support
The script has been validated to check for usage in these locations. Others may be support.
| Type                       |
|----------------------------|
| Dashboard                  |
| Story Map                  |
| Web AppBuilder             |
| Web Map                    |
| Web Mapping Application    |
| Web Scene                  |

