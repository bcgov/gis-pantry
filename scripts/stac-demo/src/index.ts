import './style.scss';

import L from 'leaflet';

// Function to fetch STAC items from Planetary Computer
async function fetchSTACItems(limit: number = 10) {
    const url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/nrcan-landcover/items";

    const params = new URLSearchParams({
        limit: limit.toString(),
        bbox: "-139.1,48.3,-114.0,60.0" // BC Bounding Box
    });

    const response = await fetch(`${url}?${params.toString()}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch STAC data: ${response.statusText}`);
    }

    return await response.json();
}

// Function to create a Leaflet layer for a single selected STAC feature
function createSTACLayerForFeature(feature: any): L.GeoJSON {
    // Check if the feature has the necessary properties before proceeding
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
        }
    });
}

// Function to add STAC imagery to Leaflet map
function addSTACImageryLayer(map: L.Map, feature: any) {
    const assets = feature.assets;
    const corner1 = L.latLng(feature.bbox[1], feature.bbox[0]);
    const corner2 = L.latLng(feature.bbox[3], feature.bbox[2]);
    const feat_bounds = L.latLngBounds(corner1, corner2);

    if (assets && assets.rendered_preview) {
        const tileUrl = assets.rendered_preview.href;
        L.imageOverlay(tileUrl, feat_bounds).addTo(map);
    }
}

// Function to handle feature selection from dropdown
function handleFeatureSelection(map: L.Map, selectedFeatureId: string, stacData: any) {
    const selectedFeature = stacData.features.find((feature: any) => feature.id === selectedFeatureId);
    
    if (selectedFeature) {
        const assets = selectedFeature.assets;
        const corner1 = L.latLng(selectedFeature.bbox[1], selectedFeature.bbox[0]);
        const corner2 = L.latLng(selectedFeature.bbox[3], selectedFeature.bbox[2]);
        const feat_bounds = L.latLngBounds(corner1, corner2);

        // Clear existing imagery overlays
        map.eachLayer((layer) => {
            if (layer instanceof L.ImageOverlay) {
                map.removeLayer(layer);
            }
        });

        // Clear existing polygons
        map.eachLayer((layer) => {
            if (layer instanceof L.GeoJSON) {
                map.removeLayer(layer);
            }
        });

        const stacLayer = createSTACLayerForFeature(selectedFeature);
        stacLayer.addTo(map);

        addSTACImageryLayer(map,selectedFeature)

        // if (assets && assets.rendered_preview) {
        //     const tileUrl = assets.rendered_preview.href;
        //     L.imageOverlay(tileUrl, feat_bounds).addTo(map);
        // }

        map.fitBounds(feat_bounds); // Zoom to the selected feature
    }
}

// Function to populate the dropdown with STAC feature options
function populateDropdown(stacData: any) {
    const dropdown = document.getElementById('stac-dropdown') as HTMLSelectElement;

    stacData.features.forEach((feature: any) => {
        const option = document.createElement('option');
        option.value = feature.id;
        option.textContent = `${feature.id} - ${feature.properties?.datetime || 'N/A'}`;
        dropdown.appendChild(option);
    });

    // Add event listener for dropdown selection
    dropdown.addEventListener('change', (event) => {
        const selectedFeatureId = (event.target as HTMLSelectElement).value;
        handleFeatureSelection(map, selectedFeatureId, stacData);
    });
}

// Function to add STAC data to Leaflet map
async function addSTACDataToMap(map: L.Map) {
    try {
        const stacData = await fetchSTACItems(500);
        console.log(stacData);

        if (stacData.features.length === 0) {
            console.warn("No STAC items found in this region.");
            return;
        }

        // Populate the dropdown with features after adding them to the map
        populateDropdown(stacData);
    } catch (error) {
        console.error(error);
    }
}

// Initialize Leaflet Map
const map = L.map('map').setView([54, -125], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Add NRCAN Landcover STAC Data
addSTACDataToMap(map);
