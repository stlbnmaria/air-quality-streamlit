# Air Quality Index from the EPA (1980-2021)
Author: Maria Stoelben

## Data
The data used consists of two public Kaggle datasets. These include [daily](https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-daily) / [yearly](https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-yearly) reports of the air quality index from various US Metro areas, as well as geographic data for the collection locations.  

Download the data with the following command:

```setup
mkdir
curl https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-yearly/download?datasetVersionNumber=2 --output data/aqi_yearly_1980_to_2021.csv
curl https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-daily/download?datasetVersionNumber=3 data/aqi_daily_1980_to_2021.csv
```

## Requirements
Create a virtual environment:

```setup
python3 -m venv .venv
source .venv/bin/activate
```

To install requirements:

```setup
pip install -r requirements.txt
```

## Run the App

Run the app locally:

```run
streamlit run air_index.py
```

## Run the App on Docker 
Build the image:

```docker
docker build -t streamlit .
```

Run the container:
```docker
docker run -p 8501:8501 streamlit
```

You can also find the container image on [Docker Hub](https://hub.docker.com/repository/docker/mstoelben/air-quality-streamlit/general).
