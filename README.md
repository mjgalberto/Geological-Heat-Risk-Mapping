# Geological-Heat-Risk-Mapping
A Flask web app for visualizing heat index and humidity risks across Philippine regions. Users upload CSV data, compute 12-month risk percentages, and explore results on an interactive GeoJSON map. Features include dynamic color mapping, sortable risk rankings, and tabular data for climate resilience insights.

## 📖 Overview
This project is a **Flask-based web application** that visualizes the **heat index risk** across different regions of the Philippines.  
It allows users to:
- Upload a CSV dataset of temperature, humidity, and heat index values.
- Compute **risk percentage** for each region based on 12-month fluctuations.
- Display results on a **GeoJSON-based interactive map** (green → red gradient).
- View a **table of uploaded data** with computed risks.
- Rank regions by their risk percentage using a sorting algorithm.

This project demonstrates how **climate data, geospatial mapping, and web technologies** can work together to provide decision-support tools for communities and policymakers.

---

## 🚀 Features
- 📂 **CSV Upload** – Input data with columns:  
  `location, month, temp_c, humidity_level, heat_index`
- 🔢 **Risk Computation** – Based on the fluctuation (standard deviation) of heat index and humidity over 12 months.
- 🌍 **GeoJSON Mapping** – Philippine regions visualized with dynamic color gradients (green → red).
- 📊 **Data Table** – Displays all uploaded dataset entries.
- 🏆 **Risk Ranking** – Regions sorted from highest to lowest risk.
- 📈 **NOAA Heat Index Formula** integrated for accurate computation.

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript (Leaflet.js for mapping)  
- **Data Handling:** Pandas, NumPy  
- **GeoJSON Mapping:** Philippine regions JSON (`ph_regions.json`)  

---

## 📂 File Structure
thermal-mapping-app/
│── app.py # Main Flask application
│── ph_regions.json # GeoJSON file of Philippine regions
│── templates/
│ ├── index.html # Frontend (map + table + ranking)
│── static/
│ ├── style.css # Styling
│ ├── script.js # Map rendering & interactivity
│── sample_heat_risk_data.csv # Example dataset
│── requirements.txt # Dependencies
│── README.md # Project documentation

## 📊 Sample CSV Format
```csv
location,month,temp_c,humidity_level,heat_index
Metro Manila,Jan,33.2,68,37.5
Metro Manila,Feb,34.0,65,38.1
Central Luzon,Jan,32.8,72,36.9
Central Luzon,Feb,33.5,70,37.4
...
