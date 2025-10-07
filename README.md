# 🏠 Digital Twin for Energy Consumption Prediction

## 📌 Overview
This project implements a **digital twin** of a residential building to **predict 24-hour energy consumption** using advanced deep learning models (**GRU** and **LSTM-Transformer**).  
The digital twin integrates **sensor data** from the **PLEGMA dataset** along with **weather conditions** to simulate and forecast building energy usage.  

The system is deployed and monitored through **Home Assistant**, enabling visualization, automation, and real-time control.

---

## 🔧 Features
- **Digital Twin Simulation**: Virtual replica of a residential building for energy monitoring and forecasting.  
- **Deep Learning Models**:  
  - **GRU** for sequential time-series prediction.  
  - **LSTM-Transformer** for capturing both short- and long-term dependencies in energy usage.  
- **Data Integration**:  
  - **PLEGMA dataset** for appliance-level energy measurements.  
  - **Weather conditions** (temperature, humidity) as external factors.  
- **Home Assistant Integration**:  
  - Real-time monitoring of predicted vs. actual consumption.  
  - Automation suggestions for energy optimization.
  - 3D digital twin Consturction and Integration in Home assistant with dynamic heatmaps.

---

## 📂 Dataset
- **PLEGMA Dataset**: Contains IoT sensor data for appliance consumption in residential .  
- **Weather Data**: Sourced from the plegma dataset itself.  

---

## 🧠 Models & Methodology
1. **Data Preprocessing**:  
   - Cleaning, normalization, and feature engineering from energy and weather data.  
2. **Model Architecture**:  
   - **GRU**: Handles sequential dependencies for short-term forecasting.  
   - **LSTM-Transformer**: Combines LSTM’s temporal understanding with Transformer’s attention mechanism for improved long-term prediction.  
3. **Training & Evaluation**:  
   - Trained on historical PLEGMA data and aligned weather records.  
   - Evaluated with RMSE and MAE metrics.  

---

## 🖥️ Home Assistant Setup
- Built and configured a **digital twin** of the building in **Home Assistant**.
- **Home Assistant** was used as OS on VMware® Workstation 17 Pro.
- Data was sent through APIs.  
- Created dashboards for **real-time monitoring** and comparison of actual vs. predicted energy usage.  

---

