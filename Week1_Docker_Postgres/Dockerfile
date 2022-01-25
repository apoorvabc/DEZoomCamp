FROM python:3.9.1

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY yellow_tripdata_2021-01.csv yellow_tripdata_2021-01.csv
COPY taxi+_zone_lookup.csv taxi+_zone_lookup.csv
COPY postgres_data.py postgres_data.py

ENTRYPOINT [ "python", "postgres_data.py" ]