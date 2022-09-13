from flask import Flask , render_template , request , redirect , url_for , session
from flask_session import Session
from flask_socketio import SocketIO, emit , join_room , leave_room
import sqlite3
import datetime
 


def create_table():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS MESSAGES    
            (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            USER TEXT NOT NULL,
            ROOM TEXT NOT NULL,
            MESSAGE TEXT NOT NULL,
            DATE TIMESTAMP NOT NULL);''')
    cur.close()
    con.close()

def insert_values(user,room,message,date):
    try:
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        qry = ('''INSERT INTO MESSAGES ('USER',ROOM,'MESSAGE','DATE') VALUES (?,?, ?, ?);''')
        data_tuple = (user,room,message,date)
        cur.execute(qry, data_tuple)
        
        con.commit()
        # print("Message Add Successfully \n")
        cur.close()
        con.close()
    except:
        print("Message Not Saved. ")


create_table()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)

@app.route('/',methods=[ 'GET' , 'POST' ])
def index():
    return render_template('index.html')

@app.route('/chat',methods=[ 'GET' , 'POST' ])
def chat():
    if request.method == 'POST':
        username = request.form.get('username')
        room = request.form.get('room')
        session['username'] = username
        session['room'] = room
        return render_template('chatting.html',session=session)
    else:
        if session.get('username'):
            return render_template('chatting.html',session=session)
        else:
            return redirect(url_for('index'))

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    user = session.get('username')
    join_room(room)
    emit('status', {'msg':  user + ' has entered the room'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    user = session.get('username')
    msg = message['msg']
    date = datetime.datetime.now()

    insert_values(user, room, msg, date)

    emit('message', {'msg': user + ' : ' + msg}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)