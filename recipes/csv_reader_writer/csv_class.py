'''
csv_class.py
description: Reads/writes a csv file into a list of python dictionaries

Copyright 2023 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at 

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''
# ************************************************************************
# CSV Class
# ************************************************************************
class CSV:
    """
    Class containing useful CSV read/write functions
    """

    def __init__(self):
        pass

    def create_dict_list(self, csvfile, clean_unicode=True):
        """
        Params
        csvfile: .csv file to be converted
        clean_unicode: if true runs ReplaceSymbols().replace_unicode on unreadable values
        """
        dictionary_list = []
        if _CAN_RUN_PY3:
            reader = csv.DictReader(open(csvfile, "rt"))
            for line in reader:
                dictionary_list.append(line)
        else:
            reader = csv.DictReader(open(csvfile))
            for line in reader:
                new_line = line
                if clean_unicode:
                    # Removes unicode symbols from items in dict list (python 2 only)
                    rs = ReplaceSymbols()
                    for key, value in line.items():
                        try:
                            str(value)
                        except Exception:
                            new_line[key] = rs.replace_unicode(value)
                dictionary_list.append(new_line)
        print("Created dictionary list from csv file: {}".format(csvfile))

        return dictionary_list

    # Writes a csv from an ordered dictionary list
    def export_csv(self, dictionary_list, csvfile, clean_unicode=True):
        """
        Params
        csvfile: .csv file to be converted
        clean_unicode: if true runs ReplaceSymbols().replace_unicode on unreadable values
        """
        # Exports dict list to csv
        if _CAN_RUN_PY3:
            with open(csvfile, "w", newline="") as outfile:
                fp = csv.DictWriter(outfile, dictionary_list[0].keys())
                fp.writeheader()
                fp.writerows(dictionary_list)
        else:
            if clean_unicode:
                # Removes unicode symbols from items in dict list (python 2 only)
                new_dl = []
                rs = ReplaceSymbols()
                for line in dictionary_list:
                    new_line = line
                    for key, value in line.items():
                        try:
                            str(value)
                        except Exception:
                            new_line[key] = rs.replace_unicode(value)
                    new_dl.append(new_line)
                dictionary_list = new_dl
            with open(csvfile, "wb") as outfile:
                fp = csv.DictWriter(outfile, dictionary_list[0].keys())
                fp.writeheader()
                fp.writerows(dictionary_list)

        print("Created CSV: {}".format(csvfile))
