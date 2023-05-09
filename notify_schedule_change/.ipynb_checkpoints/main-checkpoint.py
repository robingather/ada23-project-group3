import json
import os

from google.cloud import storage

import functions_framework
import base64
import pandas as pd
from pub_sub_util import publish_message

@functions_framework.http
def notify_schedule_change(cloud_event):
  """Background Cloud Function to be triggered by Pub/Sub
  """

  data = cloud_event.data
  event_id = cloud_event["id"]
  event_type = cloud_event["type"]
  print('Event ID: {}'.format(event_id))
  print('Event type: {}'.format(event_type))

  decodedStr = base64.b64decode(data["message"]["data"]).decode()
  print('Message data : {}'.format(decodedStr))

  schedule_input = json.loads(decodedStr)

  project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
  # bucket_name = os.environ.get('BUCKET_NAME', 'Specified environment variable is not set.')
  print('Project Id: {}'.format(project_id))

  # Open a channel to read the file from GCS
  df_schedule = pd.read_json(json.dumps(schedule_input), orient='records')

  # Download schedule
  # client = storage.Client(project=project_id)
  # bucket = client.get_bucket(model_bucket_name)
  # blob = bucket.blob('schedule_data.csv')
  # temp_filename = os.path.join('/tmp', 'schedule_data.csv')
  # blob.download_to_filename(temp_filename)
  # df_schedule = pd.read_csv(temp_filename)

  # print('Result : {}'.format(df_schedule))

  # Publish the result to the topic diabetes_req. Note, here, we assume the topic already exists.
  data = {'result': str(status[0])}
  data = json.dumps(data).encode("utf-8")  # always need to send base64 binary data
  publish_message(project=project_id, topic="diabetes_res", message=data)

  # Do clean up
  os.remove(temp_model_filename)





  request_json = request.get_json(silent=True)
  request_args = request.args

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