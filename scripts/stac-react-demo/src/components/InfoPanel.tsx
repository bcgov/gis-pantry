import React from "react";

interface InfoPanelProps {
  selectedFeature: any | null;
}

const InfoPanel: React.FC<InfoPanelProps> = ({ selectedFeature }) => {
  if (!selectedFeature) {
    return <><p>Select a feature from the dropdown on the left to see details.</p>
    <p>Click the <strong><i>Reset Map View</i></strong> button to clear the map and return to the default map view</p></>;
  }

  console.log(selectedFeature)
  console.log(Object.keys(selectedFeature.properties))
  console.log(selectedFeature.type)

  // Iterate through assets and generate links
  const assetLinks = selectedFeature.assets
    ? Object.entries(selectedFeature.assets)
        .map(([key, asset]: [string, any]) => <a href={asset.href} target="_blank">{key}</a>)
    : "No assets available";

  var timestamp: number = Date.parse(selectedFeature.properties.datetime);
  var dateObject: Date = new Date(timestamp);
  var dateString: string = dateObject.getUTCFullYear() + "-" + (dateObject.getUTCMonth()+1) + "-" + dateObject.getUTCDate()

  return (
    <div id="feature-info">
      <h3>Feature Details</h3>
      <div id="image-preview">
        <img src={selectedFeature.assets?.rendered_preview.href} alt="Rendered Preview"></img>
      </div>
      <div>
        <p><b>ID:</b> {selectedFeature.id}</p>
        <p><b>Title:</b> {selectedFeature.properties.title}</p>
        <p><b>Datetime:</b> {dateString || "N/A"}</p>
        <p><b>Collection:</b> nrcan-landcover</p>
      </div>
      <div>
        <b>Assets:</b>
        {typeof assetLinks === "string" ? <a>{assetLinks}</a> : assetLinks}
      </div>
    </div>
  );
};

export default InfoPanel;
