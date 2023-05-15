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
- {
	"email_address": "peter@gmail.com",
	"password": "goldband123"
}

## Verify existing user
This is a utility endpoint to internally check if the authentication token is tied to a verified user. It will also return relevant data of that user, like the email address which is used as a foreign key to create Tickets.

- type: POST
- url: http:{VM_ID}:5000/login
- {
	"email_address": "peter@gmail.com",
	"password": "goldband123"
}
