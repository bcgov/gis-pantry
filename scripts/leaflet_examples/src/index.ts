import './style.scss';

import * as L from 'leaflet';
import * as esri from 'esri-leaflet';
import { vectorBasemapLayer } from "esri-leaflet-vector";

window.onload = () => simpleLeafletMap();

// ESRI Developer API Token (for Basemap)
const accessToken = "";

let fire_points_url: string = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_ActiveFires_PublicView/FeatureServer/0"
let oa_url: string = "https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services/Evacuation_Orders_and_Alerts/FeatureServer/0"

const default_lat: number = 53.9667;
const default_lng: number = -123.9833;
const default_zoom: number = 5;

let simple_map: L.Map;
let fire_locations: L.esri.FeatureLayer;
let orders_alerts: L.esri.FeatureLayer;

function simpleLeafletMap() {
  // Initialize the map
  simple_map = L.map('map', {
    scrollWheelZoom: true
  });

  // Set the position and zoom level of the map
  simple_map.setView([default_lat, default_lng], default_zoom);
  simple_map.options.scrollWheelZoom = true;

  //BC Basemap without Hillshade
  const basemapEnum = "b1624fea73bd46c681fab55be53d96ae"

  //BC Basemap with Hillshade
  //const basemapEnum = "bbe05270d3a642f5b62203d6c454f457";

  // Set vector basemap
  let basemap: any = vectorBasemapLayer(basemapEnum, { token: accessToken }).addTo(simple_map);

  createFireLocationsLayer()
  createOALayer()
  layerListButton()
}

function createFireLocationsLayer() {
  fire_locations = new esri.FeatureLayer({
    url: fire_points_url,
    where: "FIRE_STATUS <> 'Out'",
    pointToLayer: function (feature: any, latlng: any) {
      return new L.Circle(latlng, {
        color: "red",
        radius: 50,
        weight: 10,
        fillOpacity: 0.85
      })
    }
  }).addTo(simple_map);
}

function createOALayer() {
  function getColor(status: string) {
    return status == "Order" ? '#DE2D26' :
      status == "Alert" ? '#FFAA00' :
        '#595959';
  }

  orders_alerts = new esri.FeatureLayer({
    // URL to the service
    url: oa_url,
    style: function (feature: any) {
      return { color: getColor(feature.properties.ORDER_ALERT_STATUS), weight: 2 };
    },
  }).addTo(simple_map);

  orders_alerts.bindPopup(function (layer: any) {
    var datetime: Date = new Date(layer.feature.properties['DATE_MODIFIED'])
    return L.Util.template(
      `<p><strong>{ORDER_ALERT_NAME}</strong> occured on ${datetime}.`,
      layer.feature.properties
    );
  });
}

function layerListButton() {
  let overlayMaps = {
    "Orders and Alerts": orders_alerts,
    "Fire Locations": fire_locations
  };

  let layerControl: L.Control = L.control.layers(null, overlayMaps).addTo(simple_map);
}