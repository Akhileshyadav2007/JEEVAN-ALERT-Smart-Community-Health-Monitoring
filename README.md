# 🚨 JEEVAN-ALERT
## AI + IoT Based Water Quality and Community Health Monitoring Platform

JEEVAN-ALERT is an AI-powered community health monitoring and early warning system designed to identify potential water-borne disease risks in rural and vulnerable communities.

The platform combines **Artificial Intelligence, IoT-based water quality monitoring, environmental data analysis, and automated health alerts** to support early detection and preventive action.

---

## 🎯 Problem Statement

Water contamination, poor sanitation, flooding, and changing environmental conditions can increase the risk of water-borne diseases.

Traditional monitoring systems may not provide timely and personalized warnings.

JEEVAN-ALERT aims to provide an intelligent system that can:

- Monitor water quality
- Analyze environmental conditions
- Predict disease risk
- Identify high-risk villages/areas
- Generate personalized alerts
- Support early preventive action

---

## 💡 Key Features

### 🤖 AI-Based Disease Risk Prediction
Machine Learning models analyze environmental and historical health data to estimate disease risk.

### 💧 Water Quality Monitoring
The system is designed to monitor water-quality parameters using IoT/sensor-based data.

### 🌧️ Environmental Monitoring
The platform considers factors such as:

- Rainfall
- Temperature
- Humidity
- Flood status
- Sanitation
- Water quality

### 🏘️ Community Health Monitoring
Village and household-level information can be analyzed to identify high-risk areas.

### 🚨 Early Warning Alerts
The system can generate alerts when risk levels increase.

### 👨‍👩‍👧 Household Monitoring
Household profiles, water history, alerts, and IoT device information are maintained for monitoring.

---

## 🧠 Machine Learning

The project uses Machine Learning for disease-risk prediction.

Important input features include:

- Population
- Rainfall
- Temperature
- Humidity
- Water Quality
- Previous Disease Cases
- Sanitation Score
- Flood Status
- Location

The trained model is stored in the `ml/` directory.

---

## 🛠️ Technologies Used

- Python
- Machine Learning
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- IoT / Sensor Data
- CSV / JSON
- Data Visualization

---

## 📂 Project Structure

```text
JEEVAN-ALERT/
│
├── app.py
├── launcher.py
├── train_model.py
├── run_app.bat
│
├── data/
│   ├── alert_history.csv
│   ├── family_alert_history.csv
│   ├── household_contacts.csv
│   ├── household_profiles.csv
│   ├── household_water_history.csv
│   ├── iot_devices.csv
│   ├── notification_history.csv
│   ├── users.json
│   └── village_data.csv
│
├── ml/
│   ├── disease_risk_model.pkl
│   └── train_model.py
│
├── .gitignore
└── README.md
