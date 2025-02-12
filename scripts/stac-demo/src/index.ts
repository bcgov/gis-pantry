import './style.scss';

import * as L from 'leaflet';

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

// Function to create a Leaflet layer from STAC GeoJSON
type STACFeature = {
    id: string | number;
    properties: any;
    geometry: any;
};

function createSTACLayer(stacData: any): L.GeoJSON {
    return L.geoJSON(stacData, {
        onEachFeature: (feature: any, layer: L.Layer) => {
            const props = feature.properties;
            const id = feature.id?.toString() || "Unknown";
            const collection = "nrcan-landcover";
            const tileurl = feature.assets.rendered_preview.href

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
function addSTACImagery(map: L.Map, stacData: any) {
    stacData.features.forEach((feature: any) => {
        const assets = feature.assets;

        const corner1 = L.latLng(feature.bbox[1], feature.bbox[0]);
        const corner2 = L.latLng(feature.bbox[3], feature.bbox[2]);
        const feat_bounds = L.latLngBounds(corner1, corner2);

        console.log(feat_bounds)
        if (assets) {
            const tileUrl = assets.rendered_preview.href;
            L.tileLayer(tileUrl, {
                bounds: feat_bounds,
                attribution: "&copy; NRCan Landcover via Microsoft Planetary Computer"
            }).addTo(map);
        }
    });
}


// Function to add STAC data to Leaflet map
async function addSTACLayer(map: L.Map) {
    try {
        const stacData = await fetchSTACItems(1);

        if (stacData.features.length === 0) {
            console.warn("No STAC items found in this region.");
            return;
        }

        const stacLayer = createSTACLayer(stacData);
        stacLayer.addTo(map);

        addSTACImagery(map, stacData);
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
addSTACLayer(map);
