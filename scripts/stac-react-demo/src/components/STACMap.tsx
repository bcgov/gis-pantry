import React, { useEffect, useRef } from "react";
import L from "leaflet";
import { createSTACLayerForFeature } from "../utils/stacUtils";

const southWest: L.LatLng = L.latLng(40, -150);
const northEast: L.LatLng = L.latLng(65, -100);
const bounds: L.LatLngBounds = L.latLngBounds(southWest, northEast);

const maxZoomNum: number = 15;
const minZoomNum: number = 5;

interface STACMapProps {
  selectedFeature: any | null;
  mapRef: React.RefObject<L.Map | null>;
}

const STACMap: React.FC<STACMapProps> = ({ selectedFeature, mapRef }) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (mapRef.current || !mapContainerRef.current) return;

    const mapInstance = L.map(mapContainerRef.current,
      {
        maxBounds: bounds,
        maxZoom: maxZoomNum,
        minZoom: minZoomNum
      }
    )
    mapInstance.setView([54, -125], 5);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(mapInstance);

    mapRef.current = mapInstance;
  }, []);

  useEffect(() => {
    if (!mapRef.current || !selectedFeature) return;

    const map = mapRef.current;
    const assets = selectedFeature.assets;
    const corner1 = L.latLng(selectedFeature.bbox[1], selectedFeature.bbox[0]);
    const corner2 = L.latLng(selectedFeature.bbox[3], selectedFeature.bbox[2]);
    const featBounds = L.latLngBounds(corner1, corner2);

    map.eachLayer((layer: L.Layer) => {
      if (layer instanceof L.ImageOverlay || layer instanceof L.GeoJSON) {
        map.removeLayer(layer);
      }
    });

    const stacLayer = createSTACLayerForFeature(selectedFeature);
    stacLayer.addTo(map);

    if (assets?.rendered_preview) {
      const tileUrl = assets.rendered_preview.href;
      L.imageOverlay(tileUrl, featBounds).addTo(map);
    }

    map.fitBounds(featBounds);
  }, [selectedFeature]);

  return <div ref={mapContainerRef} style={{ width: "100%", height: "100%" }} />;
};

export default STACMap;
