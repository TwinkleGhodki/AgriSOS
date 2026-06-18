# AgriSOS — Early Farmer Distress Prediction System

## Overview

AgriSOS is an AI-powered Early Farmer Distress Prediction System that uses weather data, market trends, and machine learning to identify farmers at risk and provide proactive recommendations. The system also supports SMS alerts, district-level monitoring dashboards and multilingual recommendations.

Tech Stack:
- Python
- Streamlit
- Scikit-Learn
- Pandas
- Open-Meteo API
- Twilio

## Quick Start (Run in this exact order)

### 1. Install dependencies
```bash
pip install streamlit pandas numpy scikit-learn requests plotly twilio python-dotenv
```

### 2. Generate training data
```bash
python generate_data.py
```

### 3. Train the ML model
```bash
python train_model.py
```

### 4. Launch the dashboard
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

---

## SMS Alerts Setup 

1. Sign up free at https://twilio.com
2. Get your Account SID, Auth Token, and phone number
3. Edit `.env` file:
```
TWILIO_SID=ACxxxxxxxxxxxxxxxxx
TWILIO_TOKEN=your_token_here
TWILIO_PHONE=+1your_number
```

---

## Project Structure

```
AgriSOS/
├── app.py              → Main Streamlit dashboard (4 tabs)
├── model.py            → ML prediction logic
├── data_fetch.py       → Open-Meteo weather API + market data
├── alerts.py           → Twilio SMS alert sender
├── generate_data.py    → Creates synthetic training dataset
├── train_model.py      → Trains and saves Random Forest model
├── farmer_data.csv     → Generated training data (600 records)
├── model.pkl           → Saved trained model
```

---


## Highlights

- Developed an ML-based farmer distress prediction system using Random Forest.
- Integrated real-time weather and market data.
- Implemented SMS notifications using Twilio.
- Built an interactive Streamlit dashboard with multiple analytics views.
- Supports multilingual recommendations.

---

## Features

- Real-time weather data via Open-Meteo API (no key needed)
- ML-based distress risk prediction (Random Forest)
- Risk score 0–100 with gauge visualization
- Personalized agronomic recommendations
- District-level risk dashboard
- Market price trend charts
- SMS alerts via Twilio
- Model explainability (feature importance)
