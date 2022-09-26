# Desk Booking Tool

## Purpose/solution

This application allow users to remotly book desks remotely, so that they can guarantee they will have a seat when they go into the office. It allows users to manage their desk bookings, and grants admins the privilage of removing user bookings where they see fit.

## Technical details

The backend of the project is made using python, and uses flask to manage the api, and sqlite3 to manage the database. The frontend of the application is made using html, and has no futher dependencies. Development of this project was done on Visual Studio Code, and the version control tool git has been used to aid development. When running localy, the python module `http.server` is used to serve the html localy. The python modle `schedule` was also used to schedule removal of exired sessions from the database.

The API has backend routes that call methods that interact with the database, however, these routes only perform such operations if data sent in via requests is valid.

When a user logins in to the application successfully, a session is created, which correlates a email address to a token, and expiry time. When the front end makes requests to the API, the token is passed along with any other required fields. When the API recieves a request it correlates the token with a user, and then checks if the user if authorised to access the endpoint. Tokens expired after 8 hours for security purposes, meaning users will allways have to sign back in after 8 hours.

## Setup local deployment
### Backend
1. clone the project: `git clone https://github.com/patricksmcr/publicDeskBookingTool.git` and `cd` into it.
2. `cd` into the `api` directory.
3. run `pip3 install -r requirements.txt`.
3. run `python3 db/utils/dbCreation.py` to create and populate the database with dummy data.
4. run `python3 application.py` to run the api.
5. in a seperate terminal, `cd` back into `deskBookingTool/api` and run `python3 db/utils/sessionSchedule.py`.
 
### Frontend
1. in a new terminal, `cd` into the `publicDeskBookingTool/ui` folder.
2. run `python3 -m http.server`.
3. in a browser, navigate to: `localhost:5000`

##References

References used within this application are as follows: 

Manwg (2010) [online] Javascript implementation of Java’s String.hashCode() method, Available from: https://werxltd.com/wp/2010/05/13/javascript-implementation-of-javas-string-hashcode-method/ [Accessed 26/09/22]
