# Emergency-Response-System
A decentralized AI-powered crisis response system for the hospitality industry using Google Gemini and Firebase
# About the project
Emergency-Response-System is a decentralized emergency response platform designed for large-scale hospitality venues. It bridges the gap between local incident detection and professional emergency dispatch using real-time AI triage.
# Tech Stack
Edge Node:        Python (CustomTkinter) for local floor-map and zone management.   
Database:         Firebase Realtime Database for instant synchronization between hardware and the cloud.   
AI Engine:        Google Gemini 1.5 Flash for automated crisis analysis and evacuation planning   
Command Center:   JavaScript (HTML5/CSS3) dashboard with integrated Google Maps data for responder tracking   
Hosting:          Firebase Hosting.
# Setup and Installation
1. Web Dashboard  
The Command Center is live and accessible at:  

						URL: https://smart-help-9eec0.web.app

2. Local Python Node
To run the tactical reporting node:
1. Clone the repository.
2. Install dependencies:

						pip install -r requirements.txt

Authentication:
1. Place your Firebase service-key.json in the root directory.
2. Update the databaseURL in hotel_node.py to match your Firebase project.

Run the app:

						python hotel_node.py
