# Advanced Data Architectures - Group 3

## Assignment 2

#### Authors:
* Diana Spahieva
* Kheiry Sohooli
* Livia Popper
* Robin Gather

#### Our FaaS functions are:
* **_get\_routes_**: get a schedule of routes based on start and end station, and selected time.
* **_check\_availability_**: it is meant to check if there are enough seats in a train for user to purchase.
* **_calc\_ticket\_price_**: if enought seats are available, then calculate the price of a ticket based on distance and departure time.
* **_notify\_schedule\_change_**: event-driven function to update users on delays.

#### Our API endpoints:
* **_register_**: create a new user account.
* **_login_**: sign-in a user.
* **_verify_**: retrieve account information based on authentication token.
* **_create\_ticket_**: assign a new ticket to a signed-in user.
* **_delete\_account_**: delete a user account.
* **_update\_account_**: update the information of a user.
* **_delete\_ticket_**: cancel a ticket.
* **_get\_tickets_**: retrieve a list of tickets for a user account.

#### How to run our code:
* For every FaaS, we designed a README file per folder;
* For the API, first go to `cd secured_account_api/` and then run `sudo docker-compose up --build -d`.

#### Our workflow architecture:
![alt text](https://github.com/robingather/ada23-project-group3/blob/main/workflow_architecture.png "Group 3 workflow architecture")