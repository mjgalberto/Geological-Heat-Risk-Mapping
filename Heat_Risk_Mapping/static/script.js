document.getElementById("uploadForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let formData = new FormData(this);

    // Show loading modal
    let loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        drawMap(data.geojson);
        drawTableAndRanking(data.rankings);
        drawTableData(data.tableData);
    })
    .finally(() => {
        // Hide loading modal
        loadingModal.hide();
    });
});

let map = L.map("map").setView([13.41, 122.56], 6);  // Center on Philippines
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

function getColor(risk) {
    // New color coding: blue (low), green (moderate), yellow (elevated), orange (high), red (extreme)
    return risk >= 80 ? "#d73027" :    // extreme risk - red
           risk >= 60 ? "#fc8d59" :    // high risk - orange
           risk >= 40 ? "#fee08b" :    // elevated risk - yellow
           risk >= 20 ? "#91cf60" :    // moderate risk - green
                        "#4575b4";    // low risk - blue
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.risk_percentage),
        weight: 2,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7
    };
}


function drawMap(geojsonData) {
    L.geoJSON(geojsonData, {
        style: style,
        onEachFeature: function (feature, layer) {
            layer.bindPopup(`${feature.properties.name}<br>Heat Index: ${feature.properties.heat_index}`);
        }
    }).addTo(map);
}

function drawTableAndRanking(rankedList) {
    // Remove previous ranking if exists
    let old = document.getElementById("ranking-container");
    if (old) old.remove();

    const container = document.createElement("div");
    container.id = "ranking-container";
    container.className = "container my-4";
    container.innerHTML = `<h3 class='mb-3'>Risk Rankings</h3>`;

    const table = document.createElement("table");
    table.className = "table table-bordered table-striped table-hover align-middle";
    table.innerHTML = `<thead class='table-dark'><tr><th>Rank</th><th>Region</th><th>Risk %</th></tr></thead><tbody></tbody>`;

    rankedList.forEach(([region, risk], index) => {
        let row = document.createElement('tr');
        row.innerHTML = `<td>${index + 1}</td><td>${region}</td><td>${risk}%</td>`;
        table.querySelector('tbody').appendChild(row);
    });

    container.appendChild(table);
    // Insert after map
    let mapDiv = document.getElementById('map');
    mapDiv.parentNode.parentNode.insertBefore(container, mapDiv.parentNode.nextSibling);
}

function drawTableData(tableData) {
    // Update the Heat and Humidity Data table
    const tbody = document.querySelector('.data-table-container tbody');
    tbody.innerHTML = '';
    if (tableData && tableData.length > 0) {
        tableData.forEach(row => {
            const tr = document.createElement('tr');
            // Use temperature if available, fallback to heat_index for backward compatibility
            const temp = (row.temperature !== undefined && row.temperature !== null) ? row.temperature : (row.heat_index !== undefined ? row.heat_index : '');
            tr.innerHTML = `<td>${row.location}</td><td>${row.month}</td><td>${temp}</td><td>${row.humidity_level}</td>`;
            tbody.appendChild(tr);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4"><em>No data available. Please upload a CSV file to see the data.</em></td></tr>`;
    }
}

