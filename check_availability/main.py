import functions_framework
from google.cloud import storage
import json
import os
import pandas as pd

@functions_framework.http
def check_availability(request):
  """HTTP Cloud Function.
  Args:
    route_id: id of the route to check
  Returns:
    n_seats_available: number of seats available

  """
  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and 'route_id' in request_json:
    route_id = request_json['route_id']
  elif request_args and 'route_id' in request_args:
    route_id = request_args['route_id']
  else:

    route_id = ''

  # download schedule
  project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
  bucket_name = os.environ.get('BUCKET_NAME', 'Specified environment variable is not set.')
  client = storage.Client(project=project_id)
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob('schedule_data.csv')
  temp_filename = os.path.join('/tmp', 'schedule_data.csv')
  blob.download_to_filename(temp_filename)
  df_schedule = pd.read_csv(temp_filename)
  
  print("route_id",route_id)
  print("seat_availability", df_schedule[df_schedule['route_id']==route_id]['seat_availability'])

  return {"result":df_schedule[df_schedule['route_id']==route_id]['seat_availability'].item()}