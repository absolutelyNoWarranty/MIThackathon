import json
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
    emit('status', {'msg': '<div class= "mdl-card__title-text"><span style="right: 1em;float:right;font-size:1em;">Med Bot :</span>'
        + medbot.greet()+'</div>\n'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    
    room = session.get('room')
    patient_msg = message['msg']
    bot_msg = medbot.speak(message['msg'])
    
    emit('message', {'msg': '<span style="font-size:1em;">'
        + session.get('name')+ ': </span> ' 
        + patient_msg}, room=room)
    emit('status', {'msg': '<span style="font-size:1em;">Med Bot: </span> '
        + bot_msg +'</br>'}, room=room)

@socketio.on('geolocation', namespace='/chat')
def geolocation(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    medbot.user_location = (message['lat'], message['lng'])

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

