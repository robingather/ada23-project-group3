import functions_framework
from google.cloud import storage
import json
import os
import pandas as pd


@functions_framework.http
def calc_ticket_price(request):
  """HTTP Cloud Function.
  Args:
    time: departure time in hours
    distance: travel length in kilometers
  Returns:
    price: ticket price in euros

  """
  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and 'time' in request_json and 'route_id' in request_json:
    time = float(request_json['time'])
    route_id = request_json['route_id']
  elif request_args and 'time' in request_args and 'route_id' in request_args:
    time = float(request_args['time'])
    route_id = request_args['route_id']
  else:
    time = 0.0
    route_id = " "

  # download schedule
  project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
  bucket_name = os.environ.get('BUCKET_NAME', 'Specified environment variable is not set.')
  client = storage.Client(project=project_id)
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob('schedule_data.csv')
  temp_filename = os.path.join('/tmp', 'schedule_data.csv')
  blob.download_to_filename(temp_filename)
  df_schedule = pd.read_csv(temp_filename)
  
  distance = df_schedule[df_schedule['route_id']==route_id]['total_distance'].item()

  print("route_id",route_id)
  print("distance", distance)

  if(time > 7 and time < 9 or time > 16 and time < 19): # on-peak fare
    return {"total":distance*0.3 + 10}
  else: # off-peak fare
    return {"total":distance*0.3}