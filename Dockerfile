FROM python:3.8.6-buster

COPY requirements.txt /requirements.txt
COPY TaxiFareModel /TaxiFareModel
COPY api /api
COPY model.joblib /model.joblib
# COPY '/home/lamtrinh259/le-wagon-final-project-service-key-614a08b34f85.json' \
      # /credentials.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
