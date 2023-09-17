# Air Quality Index from the EPA (1980-2021)
Author: Maria Stoelben

This project uses EPA air quality index data from the US to exemplify how to build a simple Streamlit dashboard and run it locally or build a docker image and run the container.

## Data
The data used consists of two public Kaggle datasets. These include [daily](https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-daily) / [yearly](https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-yearly) reports of the air quality index from various US Metro areas, as well as geographic data for the collection locations.  

Download the data from Kaggle and put the two files in a `data/` folder.

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
:warning: Consider using the flag `--no-cache` to build the image from scratch (e.g., include latest changes from git).

Run the container:
```docker
docker run -p 8501:8501 streamlit
```

You can also find the container image on [Docker Hub](https://hub.docker.com/repository/docker/mstoelben/air-quality-streamlit/general).
