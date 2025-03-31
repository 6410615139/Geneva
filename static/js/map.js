document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map', {
        preferCanvas: true // Recommended when loading large layers.
    });
    map.setView([13.736717, 100.523186], 6); // Center on Thailand

    var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        opacity: 0.90
    });
    OpenTopoMap.addTo(map);

    // Define a style for the KMZ layers (Border + Fill)
    function kmzLayerStyle(feature) {
        return {
            color: "red",   // Border color
            weight: 2,      // Border width
            opacity: 1,     // Border opacity
            fillColor: "blue", // Fill color
            fillOpacity: 0.4 // Transparency
        };
    }

    var kmzLayer = new L.KMZLayer();

    // Define control layers before use
    var control = L.control.layers(null, null, { collapsed: false }).addTo(map);

    kmzLayer.on('load', function (e) {
        var layer = e.layer;
        layer.setStyle(kmzLayerStyle); // Apply the border style

        layer.eachLayer(function (subLayer) {
            if (subLayer.feature && subLayer.feature.properties) {
                var properties = subLayer.feature.properties;
                var descriptionText = properties.description || ""; // Get description field
                
                console.log("Raw Description:", descriptionText); // Debug the content

                var sectorName = "Unknown";

                // Try parsing MBASIN_E from description using regex
                var match = descriptionText.match(/MBASIN_E\s*<\/td>\s*<td.*?>(.*?)<\/td>/i);
                if (match) {
                    sectorName = match[1].trim(); // Extract "Wang" from MBASIN_E
                }

                // Generate HTML table for all properties
                var detailsHtml = "<table class='table table-sm'><tbody>";
                for (var key in properties) {
                    if (properties.hasOwnProperty(key)) {
                        detailsHtml += `<tr><td><b>${key}</b></td><td>${properties[key]}</td></tr>`;
                    }
                }
                detailsHtml += "</tbody></table>";

                // Create popup content with extracted sector name
                var popupContent = `
                    <b>Sector: ${sectorName}</b><br>
                    ${detailsHtml}
                    <button onclick="redirectToSector('${sectorName}')" class="btn btn-primary btn-sm mt-2">View Details</button>
                `;

                // Bind Popup with Click Event
                subLayer.bindPopup(popupContent);

                // Show popup on first click
                subLayer.on('click', function () {
                    subLayer.openPopup();
                });
            }
        });

        control.addOverlay(layer, e.name);
        layer.addTo(map);
    });

    // Load KMZ file
    kmzLayer.load('/static/kmz/Thaibasin.kmz');
});

// Redirect function triggered by the button in the popup
function redirectToSector(sectorName) {
    if (sectorName !== "Unknown") {
        window.location.href = `/sector_map/${sectorName}/`;
    } else {
        alert("Sector name not available.");
    }
}
