# Check availability FaaS
This function is used by the workflow orchestration to check seat availability of a particular route with a route_id. The purpose of this step is to make sure that seats are available before a ticket is bought by the user.

To deploy:
- change the bucket id and project id in the .env.yaml file.
- `gcloud functions deploy check_availability --runtime python310 --region=us-central1 --gen2 --entry-point=check_availability --trigger-http --env-vars-file .env.yaml --memory 2Gi --allow-unauthenticated`

To use the function:
- type: POST
- url: use the url in Google Cloud Run
- body: {
	"route_id":"87f67080-d73f-4c86-8f88-15fbf7f5815a"
}
