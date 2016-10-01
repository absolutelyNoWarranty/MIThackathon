from flask import session
from flask_socketio import emit, join_room, leave_room

from bot import medbot
from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    emit('status', {'msg': medbot.greet()}, room=room)
    

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room)
    emit('status', {'msg': 'Med Bot : '+ medbot.speak(message['msg'])}, room=room)
    if message['msg'] == 'map':
        emit('showmap',{'msg':session.get('name')}, room=room)



@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

