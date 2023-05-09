import json
import os

from google.cloud import storage

import functions_framework
import base64
import pandas as pd
from pub_sub_util import publish_message

@functions_framework.cloud_event
def notify_schedule_change(cloud_event):
  """Background Cloud Function to be triggered by Pub/Sub
  """

  print(cloud_event)
  data = cloud_event.data

  event_id = cloud_event["id"]
  event_type = cloud_event["type"]

  bucket_name = data["bucket"]
  file_name = data["name"]
  metageneration = data["metageneration"]
  timeCreated = data["timeCreated"]
  updated = data["updated"]

  print(f"Event ID: {event_id}")
  print(f"Event type: {event_type}")
  print(f"Bucket: {bucket_name}")
  print(f"File: {file_name}")
  print(f"Metageneration: {metageneration}")
  print(f"Created: {timeCreated}")
  print(f"Updated: {updated}")

  # data = cloud_event.data
  # event_id = cloud_event["id"]
  # event_type = cloud_event["type"]
  # print('Event ID: {}'.format(event_id))
  # print('Event type: {}'.format(event_type))
  print(data)
  # decodedStr = base64.b64decode(data["message"]["data"]).decode()
  # print('Message data : {}'.format(decodedStr))

  # schedule_input = json.loads(decodedStr)

  project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
  # bucket_name = os.environ.get('BUCKET_NAME', 'Specified environment variable is not set.')
  print('Project Id: {}'.format(project_id))

  # Open a channel to read the file from GCS


  # Download schedule
  client = storage.Client(project=project_id)
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(file_name)
  temp_filename = os.path.join('/tmp', file_name)
  blob.download_to_filename(temp_filename)
  df_schedule = pd.read_csv(temp_filename)

  df_delayed = df_schedule[['delayed' in x for x in list(df_schedule['status'])]]

  print('Result : {}'.format(df_delayed))

  # Publish the result to the topic diabetes_req. Note, here, we assume the topic already exists.
  # data = {'result': df_delayed.to_json()}
  data = json.dumps(df_delayed.to_json()).encode("utf-8")  # always need to send base64 binary data
  publish_message(project=project_id, topic="schedule_notifications", message=data)