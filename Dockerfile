# app/Dockerfile

FROM python:3.10-slim

WORKDIR /air-quality-streamlit

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/stlbnmaria/air-quality-streamlit .

RUN pip3 install -r requirements.txt

RUN mkdir ./data/ \
    && curl https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-yearly/download?datasetVersionNumber=2 --output data/aqi_yearly_1980_to_2021.csv \
    && curl https://www.kaggle.com/datasets/threnjen/40-years-of-air-quality-index-from-the-epa-daily/download?datasetVersionNumber=3 --output data/aqi_daily_1980_to_2021.csv

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "air_index.py", "--server.port=8501", "--server.address=0.0.0.0"]