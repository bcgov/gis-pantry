import L from "leaflet";

// Fetch STAC items from Planetary Computer
export async function fetchSTACItems(limit: number = 10) {
  const url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/nrcan-landcover/items";

  const params = new URLSearchParams({
    limit: limit.toString(),
    bbox: "-139.1,48.3,-114.0,60.0", // BC Bounding Box
  });

  const response = await fetch(`${url}?${params.toString()}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch STAC data: ${response.statusText}`);
  }

  return await response.json();
}

// Create a Leaflet layer for a selected STAC feature
export function createSTACLayerForFeature(feature: any): L.GeoJSON {
  if (!feature || !feature.geometry || !feature.properties) {
    throw new Error("Invalid feature data");
  }

  const props = feature.properties;
  const id = feature.id?.toString() || "Unknown";
  const collection = "nrcan-landcover";
  const tileurl = feature.assets?.landcover?.href || "#";

  return L.geoJSON(feature, {
    onEachFeature: (feature: any, layer: L.Layer) => {
      layer.bindPopup(`
        <b>ID:</b> ${id}<br>
        <b>Collection:</b> ${collection}<br>
        <b>Datetime:</b> ${props?.["datetime"] || "N/A"}<br>
        <a href="${tileurl}" target="_blank">Tile URL</a>
      `);
    },
  });
}
