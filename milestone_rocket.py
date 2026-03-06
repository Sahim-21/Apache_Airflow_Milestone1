import json
import os
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

DAG_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(DAG_DIR, 'milestone1_output')
JSON_FILE = os.path.join(OUTPUT_DIR, 'launches.json')
IMAGES_DIR = os.path.join(OUTPUT_DIR, 'images')

def fetch_launch_data():
    """Fetches upcoming launch data and saves it as a JSON file."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    url = "https://ll.thespacedevs.com/2.0.0/launch/upcoming"
    response = requests.get(url)
    response.raise_for_status() 
    
    with open(JSON_FILE, 'w') as f:
        json.dump(response.json(), f, indent=4)
    print(f"Data successfully saved to {JSON_FILE}")

def download_rocket_images():
    """Reads the JSON file, extracts URLs, and downloads images."""
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    
    results = data.get('results', [])
    for launch in results:
        image_url = launch.get('image')
        launch_id = launch.get('id')
        
        if image_url:
            try:
                img_data = requests.get(image_url).content
                img_path = os.path.join(IMAGES_DIR, f"{launch_id}.jpg")
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Downloaded image for launch {launch_id}")
            except Exception as e:
                print(f"Failed to download image {image_url}: {e}")

default_args = {
    'owner': 'john',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'rocket_launch_pipeline',
    default_args=default_args,
    schedule='0 6 * * 1,3,5', 
    catchup=False,
    description='Pipeline to fetch rocket launches and download images'
) as dag:

    fetch_data_task = PythonOperator(
        task_id='fetch_launch_data',
        python_callable=fetch_launch_data
    )

    download_images_task = PythonOperator(
        task_id='download_rocket_images',
        python_callable=download_rocket_images
    )

    notify_task = BashOperator(
        task_id='notify_user',
        bash_command='echo "Pipeline complete! Check the dags/rocket_output folder for the latest files."'
    )

    fetch_data_task >> download_images_task >> notify_task