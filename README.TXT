# app with meme maker

I created a chatting app with a meme maker that is integrated in the website. I used a database to store the messages and have a system to defenciate the messages and the date that is inputed in the app. 

## How to test

Run the app.py to get to the messaging part of the code and the meme maker part to see what is integrated in the code. Also the main reason for the code is to run the inputs that are in the code and make it run smoothly and correctly. Run the main program `app.py`, which is a Flask app that listens for HTTP connections at the default address and port number that Flask selects (typically, localhost:5000). Make sure that you have internet connected to the computer. When the app is starting an authentication form is appeared, there you have to put the Username and the room name and start chat button. After Putting the details, you have to press the button to enter in the room.
The main program requires the SQLite database `database.db` which is created if it is missing. The conversation of the users inside the room is store in the database.db. The script `resetdb.py` can be used to create the database if it is missing, or to clear the contents of an existing one.

