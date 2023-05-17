# Advanced Data Architectures - Group 3

### Assignment 2

Authors:
* Diana Spahieva
* Kheiry Sohooli
* Livia Popper
* Robin Gather

Our FaaS functions are:
* get_routes: get a schedule of routes based on start and end station, and selected time.
* check_availability: it is meant to check if there are enough seats in a train for user to purchase.
* calc_ticket_price: if enought seats are available, then calculate the price of a ticket based on distance and departure time.
* notify_schedule_change: event-driven function to update users on delays.

Our API endpoints:
* register: create a new user account.
* login: sign-in a user.
* verify: retrieve account information based on authentication token.
* create_ticket: assign a new ticket to a signed-in user.
* delete_account: delete a user account.
* update_account: update the information of a user.
* delete_ticket: cancel a ticket.
* get_tickets: retrieve a list of tickets for a user account.

How to run our code:
* For every FaaS, we designed a README file per folder;
* For the API, first go to `cd secured_account_api/` and then run `sudo docker-compose up --build -d`.