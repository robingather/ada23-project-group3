# Calculate Ticket price FaaS
This function is used in the workflow orchestration to calculate the ticket price based on data from the schedule. It takes in the departure time of the route and the travel distance. It uses these two variables to calculate a price.

The time is used to check whether the route starts during rush hour. If so, an additional on-peak fare is added to the total price.

To deploy:
- `gcloud functions deploy calc_ticket_price --runtime python310 --region=us-central1 --gen2 --entry-point=calc_ticket_price --trigger-http --env-vars-file .env.yaml --memory 2Gi --allow-unauthenticated`

To use the function:
- type: POST
- url: use the url in Google Cloud Run
- body: {
	"time":8,
  "distance":30
}
