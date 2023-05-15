# Secured Account and Ticketing API

This folder contains a Dockerized API which you can run on your local computer or a VM that has both Docker and Docker Compose installed. To run it use `docker-compose up -d --build`.

It includes the following service operations:

## Register a new user
This registers a new user with their name, email address, and password. User type can also be defined.

- type: POST
- url: http:{VM_ID}:5000/register
- body: {
	"first_name": "John",
	"last_name": "Johnson",
	"email_address": "j.johnson@gmail.com",
	"password": "password123",
	"user_type": "private"
}

## Login as existing user
Login with email and password of existing user. You will receive a JWT authentication token that will be used to access further parts of the API

- type: POST
- url: http:{VM_ID}:5000/login
- body: {
	"email_address": "peter@gmail.com",
	"password": "goldband123"
}
- returns auth token for that user

## Verify existing user
This is a utility endpoint to internally check if the authentication token is tied to a verified user. It will also return relevant data of that user, like the email address which is used as a foreign key to create Tickets.

- type: GET
- url: http:{VM_ID}:5000/verify
- auth bearer token required
- return account data for that user.

## Create new Ticket
This API endpoint is not directly called, but is part of the ticketing workflow orchestration implementation. For testing purposes, you can still call it. It requires a route id and a price. The route id can be found in the output of the `get_routes` FaaS function. The price is calculated by the `calc_ticket_price` function.

- type: POST
- url: http:{VM_ID}:5000/ticket
- body: {
	"route_id":"87f67080-d73f-4c86-8f88-15fbf7f5815a",
	"price":17
}
- auth bearer token required
- returns ticket id

## List all tickets for user
This endpoint allows users to fetch the tickets that they have purchased using the workflow. It uses the auth token to get the user's email from the database, finds all tickets that match the user's unique email address, and returns them as jsonified output.

- type: GET
- url: http:{VM_ID}:5000/ticketlist
- auth bearer token required
- returns list of all tickets tied to the user account associated with the given bearer token