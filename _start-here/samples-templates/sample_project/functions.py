
# --------------------------------------------------------------------------------------------------
# Functions for main.py script
# --------------------------------------------------------------------------------------------------

import arcpy
import pandas as pd

def get_data_from_rest(url, out_name, query=""):
    """
    This function gets data from an arcgis REST service and exports to current workspace. The query 
    parameter is optional and can be used to filter the data. Rest sevice must be public.

    Args:
        url (string): URL of the REST service
        out_name (string): name of the output feature class
        query (string, optional): SQL query to filter the data, default is ""  

    Returns:, 
        string: path to the output feature class         
    """
    current_workspace = arcpy.env.workspace
    arcpy.conversion.FeatureClassToFeatureClass(url, current_workspace,
                                                out_name, query)
    out_path = f"{working_gbd}\\{out_name}"
    return out_path


def feature_class_to_dataframe(input_fc, input_fields=None, query=""):
    """
    Converts a feature class to a pandas dataframe. Includes all fields by default or specified 
    ones through input_fields. Features can be filtered with a query.

    Useful for data exploration in Python without ArcGIS Pro, and for leveraging pandas for 
    field value analyses.

    Args:
        input_fc (string): Path to the input feature class.
        input_fields (list, optional): Fields to include in the dataframe. Defaults to None.
        query (str, optional): Query to filter features. Defaults to "".

    Returns:
        Pandas Dataframe: A dataframe representing the feature class.
    """

    # Get list of fields if desired fields specified
    OIDFieldName = arcpy.Describe(input_fc).OIDFieldName
    if input_fields:
        final_fields = [OIDFieldName] + input_fields

    # Use all fields if no fields specified
    else:
        final_fields = [field.name for field in arcpy.ListFields(input_fc)]

    # Build dataframe row by row using search cursor
    data = [
        row for row in arcpy.da.SearchCursor(
            input_fc, final_fields, where_clause=query)
    ]
    fc_dataframe = pd.DataFrame(data, columns=final_fields)

    # Set index to object id
    fc_dataframe = fc_dataframe.set_index(OIDFieldName, drop=True)

    return fc_dataframe
