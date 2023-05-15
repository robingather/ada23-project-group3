# Get Routes FaaS
This is a function as a service that allows any user to query the schedule database for a list of possible routes based on the time of departure, start station, and end station. The user will receive a selection of routes to choose from, along with their unique route_ids. The route_ids can be used to buy a ticket associated with the route.

Because this is a limited implementation of our full design, the schedule exists as a .csv file in a Google Bucket. This function downloads that file and processes it with pandas to give the user a list of routes.

To deploy:
- change the bucket id and project id in the .env.yaml file.
- `gcloud functions deploy get_routes --runtime python310 --region=us-central1 --gen2 --entry-point=get_routes --trigger-http --env-vars-file .env.yaml --memory 2Gi --allow-unauthenticated`

To use the function:
- type: POST
- url: use the url in Google Cloud Run
- body: {
	"start_station":"Eindhoven Centraal",
	"end_station":"Den Bosch",
	"start_time":"09:00"
}
