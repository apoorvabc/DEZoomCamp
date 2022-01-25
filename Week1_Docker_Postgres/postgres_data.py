import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    csv_names = ["yellow_tripdata_2021-01.csv","taxi+_zone_lookup.csv"]
    table_names = ["yellow_taxi_trips","taxi_zones"]

    for i in range(len(csv_names)):

      print(f'Reading from {csv_names[i]}')
      df_iter = pd.read_csv(csv_names[i], iterator=True, chunksize=100000)

      df = next(df_iter)
      
      if(i==0):
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

      df.head(n=0).to_sql(name=table_names[i], con=engine, if_exists='replace')

      df.to_sql(name=table_names[i], con=engine, if_exists='append')


      while True: 
          t_start = time()
          
          try:
            df = next(df_iter)
          except:
              break
        
          if(i==0):
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

          df.to_sql(name=table_names[i], con=engine, if_exists='append')

          t_end = time()

          print('inserted another chunk, took %.3f second' % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')

    args = parser.parse_args()

    main(args)
    
