import functions_framework


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