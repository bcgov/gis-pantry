import React, { useState, useEffect, useRef } from "react";
import L from 'leaflet';
import STACMap from "./components/STACMap";
import InfoPanel from "./components/InfoPanel";
import FeatureSelector from "./components/FeatureSelector";
import { fetchSTACItems } from "./utils/stacUtils";

const App: React.FC = () => {
  const [features, setFeatures] = useState<any[]>([]);
  const [selectedFeature, setSelectedFeature] = useState<any | null>(null);
  const mapRef = useRef<L.Map | null>(null);

  useEffect(() => {
    const loadFeatures = async () => {
      try {
        const data = await fetchSTACItems(500);
        setFeatures(data.features || []);
      } catch (error) {
        console.error(error);
      }
    };

    loadFeatures();
  }, []);

  // Reset map view to default position and clear feature overlays
  const resetMapView = () => {
    if (mapRef.current) {
      const map = mapRef.current;
      map.eachLayer((layer: L.Layer) => {
        if (layer instanceof L.ImageOverlay || layer instanceof L.GeoJSON) {
          map.removeLayer(layer); // Remove polygons and image overlays
        }
      });
      map.setView([54, -125], 5); // Reset to initial view
      setSelectedFeature(null); // Clear selected feature
    }
  };

  return (
    <div id="app-container">
      {/* Left Panel: Feature Selector */}
      <div id="selector-panel">
        <h2>Feature Selector</h2>
        <FeatureSelector features={features} onSelectFeature={setSelectedFeature} onResetView={resetMapView} />
      </div>

      {/* Center: Always Visible Map */}
      <div id="map-container">
        <STACMap selectedFeature={selectedFeature} mapRef={mapRef} />
      </div>

      {/* Right Panel: Selected Feature Info */}
      <div id="info-panel">
        <h2>Feature Information</h2>
        <InfoPanel selectedFeature={selectedFeature} />
      </div>
    </div>
  );
};

export default App;
