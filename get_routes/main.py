import functions_framework
from google.cloud import storage
import json
import os
import pandas as pd

@functions_framework.http
def get_routes(request):
  """HTTP Cloud Function.
  Args:
    start_station: name of departure train station
    end_station: name of arrival train station
    start_time: time of departure in format HH:mm
  Returns:
    routes: list of routes fitting query

  """
  
  
  def get_distance(df, start_loc, end_loc):
    for _, row in df.iterrows():
        if row['start_station'] == start_loc and row['end_station'] == end_loc:
            total_distance = row['total_distance']
    return total_distance

  # functions to process schedule
  def get_schedule(df, begin_time, start_loc, end_loc):
    df_selected_schedule = pd.DataFrame({
                              'route_id': pd.Series(dtype='str'),
                              'start_time': pd.Series(dtype='str'),
                              'end_time': pd.Series(dtype='str'),
                              'start_station': pd.Series(dtype='str'),
                              'end_station': pd.Series(dtype='str'),
                              'total_duration': pd.Series(dtype='int')})
    begin_time_temp = begin_time.split(":")
    begin_time = begin_time_temp[0]
    
    for _, row in df.iterrows():
        row_start_time = row['start_time'].split(":")
        start_time = row_start_time[0]
        
        if int(start_time) >= int(begin_time) and row['start_station'] == start_loc and row['end_station'] == end_loc:
            new_row = {'route_id':row['route_id'], 'start_time':row['start_time'], 'end_time':row['end_time'], 'start_station':row['start_station'], 'end_station':row['end_station'], 'total_duration': row['total_duration']}
            # df_selected_schedule = df_selected_schedule.append(new_row, ignore_index=True)
            # df_selected_schedule = pd.concat([df_selected_schedule, new_row], axis=0)
            df_selected_schedule.loc[len(df_selected_schedule)] = new_row
            
    return df_selected_schedule

  # download schedule
  project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
  bucket_name = os.environ.get('BUCKET_NAME', 'Specified environment variable is not set.')
  client = storage.Client(project=project_id)
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob('schedule_data.csv')
  temp_filename = os.path.join('/tmp', 'schedule_data.csv')
  blob.download_to_filename(temp_filename)
  df_schedule = pd.read_csv(temp_filename)

  # get arguments
  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and 'start_station' in request_json and 'end_station' in request_json and 'start_time' in request_json:
    start_station = request_json['start_station']
    end_station = request_json['end_station']
    start_time = request_json['start_time']
  elif request_args and 'start_station' in request_args and 'end_station' in request_json and 'start_time' in request_args:
    start_station = request_args['start_station']
    end_station = request_args['end_station']
    start_time = request_json['start_time']
  else:
    start_station = ""
    end_station = ""
    start_time =""

  # process schedule
  df_routes = get_schedule(df_schedule, start_time, start_station, end_station)
  return df_routes.to_json(orient='index')

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