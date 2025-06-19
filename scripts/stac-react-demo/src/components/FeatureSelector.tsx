import React, { useState } from "react";

interface FeatureSelectorProps {
  features: any[];
  onSelectFeature: (feature: any) => void;
  onResetView: () => void;
}

const FeatureSelector: React.FC<FeatureSelectorProps> = ({ features, onSelectFeature, onResetView }) => {
  const [selectedFeatureId, setSelectedFeatureId] = useState("");

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedId = e.target.value;
    setSelectedFeatureId(selectedId);
    const selectedFeature = features.find(f => f.id === selectedId);
    onSelectFeature(selectedFeature || null);
  };

  const handleReset = () => {
    setSelectedFeatureId(""); // Reset dropdown selection
    onSelectFeature(null); // Notify parent that selection is reset
    onResetView(); // Call the original reset function
  };

  return (
    <div>
      <select
        value={selectedFeatureId}
        onChange={handleSelectChange}
        style={{ width: "100%", padding: "5px" }}
      >
        <option value="">Select a feature</option>
        {features.map((feature) => (
          <option key={feature.id} value={feature.id}>
            {feature.id}
          </option>
        ))}
      </select>

      {/* Reset Button */}
      <button
        onClick={handleReset}
      >
        Reset Map View
      </button>
    </div>
  );
};

export default FeatureSelector;
