# How To Extract Data Submitted To CHEFS Forms
[CHEFS API documentation](https://submit.digital.gov.bc.ca/app/api/v1/docs#tag/Submission/operation/exportWithFields)

## Input parameters:
1. CHEFS API Key
2. CHEFS Form ID
3. CHEFS Version ID
4. Input fields

### Set Up CHEFS API key
You will need to enable the API for your CHEFS form. Once logged in to CHEFS:
1. Navigate to **My Forms**, find the form for which you want to enable the API key. Select **Manage**
2. Expand the **Api Key** heading and select **Generate API Key**
3. Check the box to allow the API key to access submitted files

### Find CHEFS Form ID and Version ID
Once you've saved your form, you can find the form ID and the version ID:
1. Navigate to **My Forms**, find the form for which you want to enable the API key. Select **Manage**
2. Click on the desired form version
3. You can find the IDs in the url:
    submit.digital.gov.bc.ca/app/form/preview?f=**{Form ID will be here}**&d=**{Version ID will be here}**

### Find Field Names
When editing your form: 
1. Hover open a component and click the **gear** icon to open the component editing window
2. Choose the **API** tab
3. The field name is displayed within the **Property Name** box. You can edit the field name as required
Add the field names as a comma-seperated list within the script. Ex: "field1, field2, field3"
