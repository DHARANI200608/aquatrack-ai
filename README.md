# AquaTrack-AI 🌊

AI-powered early warning system that monitors water quality and predicts 
water-borne disease outbreaks in rural Northeast India, sending real-time 
alerts to communities and health authorities.

## Problem Statement
 Smart Community Health Monitoring and Early Warning System for 
Water-Borne Diseases in Rural Northeast India

## Features
- 🤖 ML-based disease outbreak risk prediction
- 🗺️ Real-time risk mapping
- 📱 SMS alerts to communities
- 📊 Health monitoring dashboard

## Tech Stack
- Python (ML model)
- Streamlit (Dashboard)
- Folium (Maps)
- Twilio (SMS alerts)
- Frontend
Developed using HTML, CSS, JavaScript, and Bootstrap.
Provides interfaces for citizen reporting, dashboard visualization, water quality monitoring, and outbreak alerts.
## Backend
Developed using Python Flask and MySQL.
Handles data collection, storage, disease risk prediction, alert generation, and dashboard management.
## AIML Module
Uses machine learning algorithms to analyze symptoms and water quality data.
Predicts the risk of water-borne disease outbreaks and supports early warning notifications.
## Requirement Gathering

## Functional Requirements

Collect citizen health reports and water quality data.
Predict water-borne disease risk using machine learning.
Generate early warning alerts for high-risk areas.
Provide dashboards for monitoring cases and trends.

## Non-Functional Requirements

User-friendly interface.
Secure and reliable data management.
Fast and accurate prediction system.
## Objective 

To develop a Smart Community Health Monitoring and Early Warning System that collects health and water quality data, predicts the risk of water-borne diseases using machine learning, and provides early alerts to help prevent disease outbreaks and protect public health.
## User Identification
Citizens – Submit health reports and view alerts.
Health Officials/Admin – Monitor reports, analyze trends, and manage alerts.
## Module Identification
Data Collection Module – Collects health and water quality data.
Disease Prediction Module – Predicts disease risk using machine learning.
Alert Management Module – Generates and sends early warnings.
Dashboard Module – Displays reports, statistics, and trends.
Database Management Module – Stores and manages system data.
## USER CASE DIAGRAM
+-------------------+
|      Citizen      |
+-------------------+
          |
  -----------------------
  |          |          |
Submit    View       View Water
Report    Alerts      Quality
          |
          v
+------------------------+
|         System         |
+------------------------+
| Predict Disease Risk   |
| Store Data             |
| Generate Alerts        |
+------------------------+
          ^
          |
  -----------------------
  |          |          |
Monitor   Manage      View
Reports   Alerts      Dashboard
          |
+------------------------+
| Admin / Health Official |
+------------------------+
## Database Requirement Analysis

The database is used to store and manage health reports, water quality data, disease predictions, and alert information.


## TABLES
Citizen Reports – Stores user details, symptoms, location, and report date.
Water Quality Data – Stores water quality parameters and status.
Disease Predictions – Stores predicted risk levels and results.
Alerts – Stores outbreak warnings and alert messages.
Admin Details – Stores administrator information for system management.

