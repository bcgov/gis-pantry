# Author: LAPERRY, MCM MCAD Regional Operations
# Date Created: 2025Aug19
#
# Description: 
#   This script updates ArcGIS Online (AGOL) feature services from a local source. It supports
#   both upsert (update/insert) and truncate/append update methods, handles schema 
#   synchronization, and manages sync settings. The script exports source data to a temporary
#   File Geodatabase, zips it, uploads to AGOL, and then appends that data to the target 
#   feature service.
#   
#   This script is designed to be the recommended all purpose solution for updating feature
#   services, fixing previous issues with schema flexibility and performance.
#
# Modifies:
#   https://community.esri.com/t5/arcgis-online-documents/overwrite-arcgis-online-feature-service-using/ta-p/90445



import arcpy, os, time, uuid, arcgis
from zipfile import ZipFile
from arcgis.gis import GIS
import arcgis.features


class FeatureServiceUpdater:
    def __init__(self, username, password, 
                 agol_url="https://governmentofbc.maps.arcgis.com/", 
                 verify_cert=True):
        """
        Initialize the FeatureServiceUpdater with AGOL credentials and establish connection
        
        Args:
            username (str): ArcGIS Online username
            password (str): ArcGIS Online password
            agol_url (str): ArcGIS Online URL (default: BC Gov AGOL)
            verify_cert (bool): Whether to verify SSL certificate (default: True)
        
        Returns:
            None
        
        Example:
            updater = FeatureServiceUpdater("my_username", "my_password")
        """
        self.username = username
        self.password = password

        arcpy.env.overwriteOutput = True
        arcpy.env.preserveGlobalIds = True

        print("Connecting to AGOL")
        self.gis = GIS(agol_url, self.username, self.password, verify_cert=verify_cert)
        print("Connected to AGOL as {}".format(self.gis.properties.user.username))

    def zip_dir(self, dir_path, zip_path):
        """
        Zips a File Geodatabase directory into a zip file, excluding lock files
        
        Args:
            dir_path (str): Path to the File Geodatabase directory to be zipped
            zip_path (str): Path where the zip file will be created
        
        Returns:
            None
        
        Example:
            self.zip_dir(r"C:\temp\my.gdb", r"C:\temp\my.gdb.zip")
        """
        zip_file = ZipFile(zip_path , mode='w')
        geodatabase_name = os.path.basename(dir_path)
        for root, _ , files in os.walk(dir_path):
            for file in files:
                if 'lock' not in file:
                   file_path = os.path.join(root, file)
                   zip_file.write(file_path , os.path.join(geodatabase_name, file))
        zip_file.close()

    def update_feature_service_schema(self):
        """
        Synchronizes the schema between source feature class and target feature service.
        Adds new fields that exist in source but not in service, and removes fields 
        that exist in service but not in source.
        
        Args:
            None (uses instance variables set by overwrite method)
        
        Returns:
            None
        
        Example:
            self.update_feature_service_schema()
        """
        
        # Get source field required fields
        required_fields = [field.name for field in arcpy.ListFields(self.feature_class) 
                          if field.required]

        # Get feature service fields
        print("Get feature service fields")
        feature_service_fields = {}

        if self.layer_or_table == "layer":
            for field in self.feature_layer.manager.properties.fields:
                if field.type != 'esriFieldTypeOID' and 'Shape_' not in field.name:
                    feature_service_fields[field.name] = field.type

        elif self.layer_or_table == "table":
            for field in self.feature_layer.properties.fields:
                if field.type != 'esriFieldTypeOID':
                    feature_service_fields[field.name] = field.type

        # Get source fields
        print("Get feature class/table fields")
        feature_class_fields = {}

        for field in arcpy.ListFields(self.feature_class):
            if field.name not in required_fields:
                feature_class_fields[field.name] = field.type

        # Compare fields and update schema
        minus_schema_diff = set(feature_service_fields) - set(feature_class_fields)
        add_schema_diff = set(feature_class_fields) - set(feature_service_fields)

        if len(minus_schema_diff) > 0:
            print("Deleting removed fields")
            for key in minus_schema_diff:
                print(f"\tDeleting field {key}")
                remove_field = {
                    "name": key,
                    "type": feature_service_fields[key]
                }
                update_dict = {"fields": [remove_field]}
                self.feature_layer.manager.delete_from_definition(update_dict)

        field_type_dict = {}
        field_type_dict['Date'] = 'esriFieldTypeDate'
        field_type_dict['Double'] = 'esriFieldTypeDouble'
        field_type_dict['Integer'] = 'esriFieldTypeInteger'
        field_type_dict['String'] = 'esriFieldTypeString'
        if len(add_schema_diff) > 0:
            print("Adding additional fields")
            for key in add_schema_diff:
                print(f"\tAdding field {key}")
                if field_type_dict[feature_class_fields[key]] == 'esriFieldTypeString':
                    new_field = {
                        "name": key,
                        "type": field_type_dict[feature_class_fields[key]],
                        "length": [field.length for field in 
                                  arcpy.ListFields(self.feature_class, key)][0],
                        "visible": True
                    }
                else:
                    new_field = {
                        "name": key,
                        "type": field_type_dict[feature_class_fields[key]],
                        "visible": True
                    }

                update_dict = {"fields": [new_field]}
                self.feature_layer.manager.add_to_definition(update_dict)

    def divide_chunks(self, items_list, chunk_size):
        """
        Generator function that divides a list into chunks of specified size.
        Used for batching delete operations to avoid query limits.
        
        Args:
            items_list (list): List of items to be divided into chunks
            chunk_size (int): Maximum number of items per chunk
        
        Returns:
            generator: Yields lists of items with maximum length of chunk_size
        
        Example:
            chunks = list(self.divide_chunks([1,2,3,4,5,6,7], 3))
            # Returns: [[1,2,3], [4,5,6], [7]]
        """
        for i in range(0, len(items_list), chunk_size):
            yield items_list[i:i + chunk_size]

    def overwrite(self, feature_class, fs_item_id, layer_or_table="layer", 
                  index=0, disable_sync=True, update_schema=True, 
                  upsert=False, unique_field = None):
        """
        Main method to overwrite or update an AGOL feature service with data from a 
        local source. Handles both upsert and truncate/append workflows.
        
        The upsert operation achieves the same end result as truncate/append but is 
        potentially more efficient. It updates existing features and inserts new ones 
        based on a unique field, then removes any features from the service that no 
        longer exist in the source. This can be faster than truncating and re-uploading 
        all data, especially for large datasets with minimal changes. Upsert requires a 
        field with consistent unique values that exists in both source and target such 
        as a PIN or GUID field. ArcGIS OBJECTIDs are not suitable for this purpose as 
        they are not guaranteed to be consistent across different runs of the script.
        
        Args:
            feature_class (str): Path to the source features
            fs_item_id (str): AGOL Feature Service Item ID to update
            layer_or_table (str): Target type - "layer" or "table" (default: "layer")
            index (int): Index of the layer or table within the service (default: 0)
            disable_sync (bool): Whether to disable sync during truncate operations 
                                (default: True)
            update_schema (bool): Whether to synchronize schema changes (default: True)
            upsert (bool): True for upsert operation, False for truncate/append 
                          (default: False)
            unique_field (str): Field name containing unique values for upsert 
                               (default: None)
        
        Returns:
            dict: Result dictionary from the append operation (truncate/append only)
            None: For upsert operations
        
        Example:
            updater.overwrite(
                feature_class=r"C:\data\parcels.shp",
                fs_item_id="abc123def456",
                layer_or_table="layer",
                index=0,
                upsert=True,
                unique_field="PARCEL_ID"
            )
        """
        
        # Validate parameters
        if layer_or_table not in ["layer", "table"]:
            raise ValueError("layer_or_table must be either 'layer' or 'table'")
        
        if upsert and not unique_field:
            raise ValueError("unique_field must be specified for upsert operations")
        
        self.feature_class = feature_class          
        self.fs_item_id = fs_item_id                
        self.layer_or_table = layer_or_table        
        self.index = index                         
        self.disable_sync = disable_sync            
        self.update_schema = update_schema          
        self.upsert = upsert                        
        self.unique_field = unique_field            
        
        # Create Temporary Geodatabase and Upload to AGOL
        # ------------------------------------------------------------------------------
        start_time = time.time()
        gdb_id = str(uuid.uuid1())

        try:
            print("Creating and uploading temporary File Geodatabase")
            self.geodatabase = arcpy.CreateFileGDB_management(
                arcpy.env.scratchFolder, gdb_id)[0]

            feature_class_name = os.path.basename(self.feature_class)
            feature_class_name = feature_class_name.split('.')[-1]
            print(f"Exporting {feature_class_name} to temp FGD")
            if self.layer_or_table == "layer":
                arcpy.conversion.FeatureClassToFeatureClass(
                    self.feature_class, self.geodatabase, feature_class_name)
            elif self.layer_or_table == "table":
                arcpy.conversion.TableToTable(
                    self.feature_class, self.geodatabase, feature_class_name)

            self.zip_dir(self.geodatabase, f"{self.geodatabase}.zip")

            fgd_properties = {
                'title': gdb_id, 
                'tags': 'temp file geodatabase', 
                'type': 'File Geodatabase'
            }

            if arcgis.__version__ < '2.4.0':
                fgd_item = self.gis.content.add(
                    item_properties=fgd_properties, data=f"{self.geodatabase}.zip")
            elif arcgis.__version__ >= '2.4.0':
                root_folder = self.gis.content.folders.get()
                fgd_item = root_folder.add(
                    item_properties=fgd_properties, file=f"{self.geodatabase}.zip").result()

            # Get the feature layer or table from the service
            service_layer = self.gis.content.get(self.fs_item_id)
            if self.layer_or_table == "layer":
                self.feature_layer = service_layer.layers[self.index]
            elif self.layer_or_table == "table":
                self.feature_layer = service_layer.tables[self.index]

            # If using upsert method
            # ------------------------------------------------------------------------------
            if self.upsert == True:
                # unique field index creation for upsert
                unique_field_index_template = {
                    "fields": self.unique_field,
                    "isUnique": True,
                    "description": "Unique field for upsert"
                }

                # if index on specified field exists but is not unique
                # delete the existing index and create a new unique index 
                for index in self.feature_layer.properties["indexes"]:
                    if index['fields'] == self.unique_field:
                        field_has_index = True
                        if index['isUnique'] == False:
                            
                            print(f"{self.unique_field} does not have unique index; creating")
                            self.feature_layer.manager.delete_from_definition({
                                "indexes": [{"fields": self.unique_field}]
                            })

                            self.feature_layer.manager.add_to_definition({
                                "indexes": [unique_field_index_template]
                            })
                        else:
                            break
                
                # if no index found, create a new unique index
                if not field_has_index:
                    print(f"{self.unique_field} does not have unique index; creating")
                    self.feature_layer.manager.add_to_definition({
                        "indexes": [unique_field_index_template]
                    })

                # If schema update is enabled, synchronize the schema
                if self.update_schema == True:
                    self.update_feature_service_schema()

                # Append features to the feature service using the upsert method
                print("Appending features")
                self.result = self.feature_layer.append(
                    item_id=fgd_item.id, 
                    upload_format="filegdb", 
                    upsert=True, 
                    upsert_matching_field=self.unique_field, 
                    field_mappings=[])

                # Delete features in feature service that have been removed 
                # from local source
                source_feature_list = [row[0] for row in 
                                    arcpy.da.SearchCursor(self.feature_class, 
                                                        [self.unique_field])]
                service_feature_list = [row[0] for row in 
                                    arcpy.da.SearchCursor(self.feature_layer.url, 
                                                            [self.unique_field])]
                source_set = set(source_feature_list)
                differences = [x for x in service_feature_list if x not in source_set]

                if len(differences) > 0:
                    print('Deleting differences')
                    if len(differences) == 1:
                        if type(differences[0]) == str:
                            features = self.feature_layer.query(
                                where=f"{self.unique_field} = '{differences[0]}'")
                        else:
                            features = self.feature_layer.query(
                                where=f"{self.unique_field} = {differences[0]}")
                        self.feature_layer.edit_features(deletes=features)
                    else:
                        chunk_list = list(self.divide_chunks(differences, 1000))
                        for chunk in chunk_list:
                            chunk_tuple = tuple(chunk)
                            features = self.feature_layer.query(
                                where=f'{self.unique_field} IN {chunk_tuple}')
                            self.feature_layer.edit_features(deletes=features)

            # If using truncate/append method
            # ------------------------------------------------------------------------------
            else:
                print("Updating feature service using truncate/append method")
                # If schema update is enabled, synchronize the schema
                if self.update_schema == True:
                    self.update_feature_service_schema()

                # If views exist or disableSync = False, use delete_features. 
                # OBJECTIDs will not reset
                feature_layer_collection = arcgis.features.FeatureLayerCollection(
                    service_layer.url, self.gis)
                has_views = False
                try:
                    if feature_layer_collection.properties.hasViews == True:
                        print("Feature Service has view(s)")
                        has_views = True
                except:
                    has_views = False

                if has_views == True or self.disable_sync == False:
                    min_oid = self.feature_layer.query(out_statistics=[
                        {"statisticType": "MIN", 
                        "onStatisticField": "OBJECTID", 
                        "outStatisticFieldName": "MINOID"}])
                    min_objectid = min_oid.features[0].attributes['MINOID']

                    max_oid = self.feature_layer.query(out_statistics=[
                        {"statisticType": "MAX", 
                        "onStatisticField": "OBJECTID", 
                        "outStatisticFieldName": "MAXOID"}])
                    max_objectid = max_oid.features[0].attributes['MAXOID']

                    # Delete in 2000 feature increments to avoid query limits
                    print("Deleting features")
                    if max_objectid != None and min_objectid != None:
                        if (max_objectid - min_objectid) > 2000:
                            start_id = min_objectid
                            end_id = start_id + 1999
                            while start_id < max_objectid:
                                query = f"OBJECTID >= {start_id} AND OBJECTID <= {end_id}"
                                self.feature_layer.delete_features(where=query)
                                start_id += 2000
                                end_id += 2000
                        else:
                            print("Deleting features")
                            self.feature_layer.delete_features(where="1=1")

                # If no views and disableSync = True: disable sync, truncate, 
                # and re-enable sync. OBJECTIDs will reset
                elif has_views == False and self.disable_sync == True:
                    if feature_layer_collection.properties.syncEnabled == True:
                        print("Disabling Sync")
                        properties = feature_layer_collection.properties.capabilities
                        update_dict = {"capabilities": "Query", "syncEnabled": False}
                        feature_layer_collection.manager.update_definition(update_dict)
                        print("Truncating Feature Service")
                        self.feature_layer.manager.truncate()
                        print("Enabling Sync")
                        update_dict = {"capabilities": properties, "syncEnabled": True}
                        feature_layer_collection.manager.update_definition(update_dict)
                    else:
                        print("Truncating Feature Service")
                        self.feature_layer.manager.truncate()

                print("Appending features test")
                self.result = self.feature_layer.append(
                    item_id=fgd_item.id, 
                    upload_format="filegdb")
                
                print(self.result)
                return self.result
        
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        
        finally:
            print("Cleaning up temporary files")
            if 'fgd_item' in locals():
                fgd_item.delete()
            
            if arcpy.Exists(self.geodatabase):
                print("Deleting temporary File Geodatabase")
                arcpy.Delete_management(self.geodatabase)

            if os.path.exists(f"{self.geodatabase}.zip"):
                os.remove(f"{self.geodatabase}.zip")

            end_time = time.time()
            elapsed_time = round((end_time - start_time) / 60, 2)
            print("Script finished in {0} minutes".format(elapsed_time))

