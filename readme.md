# Milestone 1: Rocket Launch Data Pipeline

## Project Overview
This project is an automated data pipeline built with Apache Airflow. [cite_start]It solves a hypothetical scenario for a rocket enthusiast named John, who wants to aggregate news and images of upcoming rocket launches[cite: 7, 8, 9]. 

[cite_start]The pipeline automatically fetches upcoming launch data from the Launch Library 2 API [cite: 12, 14][cite_start], extracts the relevant image URLs, and downloads the rocket images to a local storage directory[cite: 58].

## Pipeline Architecture
The workflow consists of three main tasks orchestrated by an Airflow DAG:
1. [cite_start]**`fetch_launch_data`**: Connects to the Launch Library 2 API (`https://ll.thespacedevs.com/2.0.0/launch/upcoming`)[cite: 14], retrieves the JSON payload, and saves it locally.
2. [cite_start]**`download_rocket_images`**: Parses the saved JSON file, extracts the URLs from the `image` keys, and downloads each `.jpg` or `.png` file into a dedicated images folder[cite: 58].
3. **`notify_user`**: A simple bash operator that acts as a notification system, confirming the pipeline executed successfully and alerting the user that the files are ready.

[cite_start]**Schedule:** The pipeline is configured to run automatically every Monday, Wednesday, and Friday at 06:00 AM (`schedule='0 6 * * 1,3,5'`)[cite: 57].

## Folder Structure
```text
milestone1_1/
├── milestone_rocket.py                 # The Airflow DAG script
├── launches.json           # Raw data fetched from the API
├── images/                 # Downloaded rocket images
│   ├── <launch_id>.jpg
│   └── ...
└── README.md