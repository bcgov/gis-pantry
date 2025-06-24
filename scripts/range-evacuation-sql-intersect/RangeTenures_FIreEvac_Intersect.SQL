/* This SQL query returns a table of all of the active range tenures in the Northeast (Forest File ID and Client Number) 
  which intersect with EMBC Orders and Alerts. This can be input into an Excel sheet with a live BCGW database connection
  to create an Excel sheet that can be easily opened and refreshed once the user configures the database connection.

  Written by North Ross 2023 for Tanya Sharko (Northeast Region Range, FOR)
*/
SELECT r.forest_file_id, r.client_name, r.client_number, fire.EVENT_NAME, fire.ORDER_ALERT_STATUS
  FROM WHSE_HUMAN_CULTURAL_ECONOMIC.EMRG_ORDER_AND_ALERT_AREAS_SP fire, WHSE_FOREST_TENURE.FTEN_RANGE_POLY_SVW r
  WHERE fire.ORDER_ALERT_STATUS in ('Order', 'Alert')
  AND r.LIFE_CYCLE_STATUS_CODE = 'ACTIVE'
  AND r.ADMIN_DISTRICT_CODE in ('DPC', 'DFN')
  AND SDO_RELATE(fire.shape, r.geometry,
                   'mask=ANYINTERACT') = 'TRUE'
  ORDER BY fire.ORDER_ALERT_STATUS desc;