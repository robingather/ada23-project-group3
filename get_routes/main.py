import functions_framework
from google.cloud import storage
import json
import os
import pandas as pd

@functions_framework.http
def get_routes(request):
  """HTTP Cloud Function.
  Args:
    departure_location: name of departure train station
    arrival_location: name of arrival train station
    deprature_time: time of departure in format HH:mm
  Returns:
    routes: list of routes fitting query

  """
  request_json = request.get_json(silent=True)
  request_args = request.args
  
  # download schedule
  project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
  bucket_name = os.environ.get('BUCKET_NAME', 'Specified environment variable is not set.')
  client = storage.Client(project=project_id)
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob('schedule_data.csv')
  temp_model_filename = os.path.join('/tmp', 'schedule_data.csv')
  blob.download_to_filename(temp_model_filename)
  df_schedule = pd.read_csv(temp_model_filename)
  return "full schedule:%s" % df_schedule.iloc[0]

  df_schedule[df_schedule['start_time'] > departure_time]

  if request_json and 'time' in request_json and 'distance' in request_json:
    time = float(request_json['time'])
    distance = request_json['distance']
  elif request_args and 'time' in request_args and 'distance' in request_args:
    time = float(request_args['time'])
    distance = request_args['distance']
  else:
    time = 0.0
    distance = 0.0

  if(time > 7 and time < 9 or time > 16 and time < 19): # on-peak fare
    return 'Total %.2f' % (distance*0.3 + 10)
  else: # off-peak fare
    return 'Total %.2f' % (distance*0.3)
  # return 'Total {}!'.format(float(arg1) + float(arg2))