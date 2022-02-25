from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from TaxiFareModel.trainer import *
from TaxiFareModel.data import get_data_from_gcp, clean_data
from datetime import datetime
import pytz
import pandas as pd
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, \
            dropoff_latitude, passenger_count):
    # compute `wait_prediction` from `day_of_week` and `time`
    # Convert to time type
    pickup_datetime = datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S')
    X_test = pd.DataFrame({'key': 'whatever',
                "pickup_datetime": pickup_datetime,
                "pickup_longitude": float(pickup_longitude),
                "pickup_latitude": float(pickup_latitude),
                "dropoff_longitude": float(dropoff_longitude),
                "dropoff_latitude": float(dropoff_latitude),
                "passenger_count": int(passenger_count)}, index=[0])

    # Conver to local timezone
    X_test['pickup_datetime'] = X_test['pickup_datetime'].dt.tz_localize('America/New_York')

    # localize the user datetime with NYC timezone
    # eastern = pytz.timezone("US/Eastern")
    # X_test['pickup_datetime'] = eastern.localize(X_test['pickup_datetime'], is_dst=None)

    # localize the datetime to UTC
    # X_test['utc_pickup_datetime'] = X_test['localized_pickup_datetime'].astimezone(pytz.utc)

    # Convert datetime to format expected by the pipeline
    # X_test['formatted_pickup_datetime'] = X_test['utc_pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S UTC")

    # df = get_data_from_gcp(nrows=1000, optimize=True)
    # Clean data
    # df = clean_data(df)

    # Get the model
    model = joblib.load('model.joblib')
    # y_train = df["fare_amount"]
    # X_train = df.drop("fare_amount", axis=1)
    # trainer = Trainer(X_train, y_train)
    # trainer.set_experiment_name('Linear API test')
    # Fit and train the model
    # trainer.run()

    # Predict the fare and save results to a json file
    y_pred = model.predict(X_test)
    # print(y_pred)
    # results = dict({'fare': y_pred})
    # json_response = json.dumps(results, indent=1)
    return {'fare': y_pred[0]} #json_response

# For testing
# predict("2013-07-06 17:18:00", -73.950655, 40.783282, -73.984365, \
        # 40.769802, 1)
