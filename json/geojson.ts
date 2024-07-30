// Define the bounds for Singapore
const minLat = 1.32;
const maxLat = 1.36;
const minLng = 103.88;
const maxLng = 103.93;

// Define the size of each polygon
const latStep = 0.0003; // Smaller latitude step
const lngStep = 0.0001; // Smaller longitude step

// Calculate the incremental change for the slanted line
const latIncrement = (maxLat - minLat) / 2100;
const lngIncrement = (maxLng - minLng) / 2100;

// Define the rotation angle in radians (e.g., 45 degrees for a diagonal slant)
const angle = -Math.PI / 4;

// Function to rotate a point around the origin (0, 0)
function rotatePoint(lng: number, lat: number, angle: number) {
  return {
    lng: lng * Math.cos(angle) - lat * Math.sin(angle),
    lat: lng * Math.sin(angle) + lat * Math.cos(angle),
  };
}

function generateGeojsonData(): void {
  // Default options for the rings
  let polygonStrokeColor = "#8E8E8E";
  let polygonFillColor = "#006064";
  let polygonFillOpacity = 0.35;

  // Create polygons in a diagonal line
  for (let i = 0; i < 2100; i += 1) {
    // Reset the polygon options for each ring
    polygonStrokeColor = "#8E8E8E";
    polygonFillColor = "#006064";
    polygonFillOpacity = 0.6;

    const baseLat = maxLat - (i + 4) * latIncrement;
    const baseLng = maxLng + (i + 4) * lngIncrement;

    const p1 = rotatePoint(lngStep, latStep, angle);
    const p2 = rotatePoint(0, latStep, angle);
    const p3 = rotatePoint(0, 0, angle);
    const p4 = rotatePoint(lngStep, 0, angle);

    const polygon = [
      { lng: baseLng + p1.lng, lat: baseLat + p1.lat },
      { lng: baseLng + p2.lng, lat: baseLat + p2.lat },
      { lng: baseLng + p3.lng, lat: baseLat + p3.lat },
      { lng: baseLng + p4.lng, lat: baseLat + p4.lat },
    ];

    // Highlight different color for the unbuilt rings (WHITE-ish color)
    if (i + 1 > latestRing) {
      polygonFillColor = "#F5F5F5";
    }

    // Highlight different color for the building ring (RED-ish color)
    if (i + 1 === latestRing) {
      polygonFillColor = "#FF0000";
      polygonFillOpacity = 1.0;
    }

    // Highlight different color for the ring where the tbm cutterhead is located (YELLOW-ish color)
    // TODO: Replace the cutterhead ring with the actual cutterhead ring from the API
    if (i + 1 === latestRing + 4) {
      polygonFillColor = "#F0CA67";
      polygonFillOpacity = 1.0;
    }

    // Highlight different color for the predicted ring (CYAN-ish color)
    // TODO: Replace the predicted ring with the actual predicted ring from the API
    if (i + 1 === latestRing + 7) {
      polygonFillColor = "#00BCD4";
      polygonFillOpacity = 1.0;
    }

    // Define mapper polygon property for each ring
    ringsPaths.push({
      name: `Ring ${i + 1}`,
      options: {
        paths: polygon,
        strokeColor: polygonStrokeColor,
        strokeOpacity: 0.8,
        strokeWeight: 1,
        fillColor: polygonFillColor,
        fillOpacity: polygonFillOpacity,
      },
    });
  }
}
