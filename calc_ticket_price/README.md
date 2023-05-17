# Calculate Ticket price FaaS
This function is used in the workflow orchestration to calculate the ticket price based on data from the schedule. It takes in the departure time of the route and the travel distance. It uses these two variables to calculate a price.

The time is used to check whether the route starts during rush hour. If so, an additional on-peak fare is added to the total price.

To deploy:
- `gcloud functions deploy calc-ticket-price --gen2 --region=us-central1 --runtime python310 --entry-point=calc-ticket-price --trigger-http --allow-unauthenticated`

To use the function:
- type: POST
- url: use the url in Google Cloud Run
- body: {
	"route_id": "4c593a93-5e0f-4b93-b266-a5716b07acb2",
  "time": 8
}