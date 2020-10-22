'''
    channel.py written by Xingyu Tan.
'''
import jwt
import data.data as data
from base.error import InputError, AccessError
from datetime import timezone, datetime
################################################################################
################################################################################
##
##    Xingyu TAN's work:
##    22 October, 2020
##
##      - some helper functions;
##      - message_send(token, channel_id, message);
##      - message_remove(token, message_id);
##      - message_edit(token, message_id, message);
##      - and all tests for these functions.
##
################################################################################
################################################################################


############################################################
#      Helper Functions
############################################################

def add_one_in_channel(channel_id, user):
    """Adding a member into the channel."""
    for i in data.channels:
        if i['channel_id'] == channel_id:
            i['all_members'].append(user)
            break

def token_into_user_id(token):
    """Transfer the token into the user id."""

    # Adding in a little bit here to improve token handling
    with open('src/data/JWT_SECRET.txt', 'r') as file:
        jwt_secret = file.read()

    try:
        email = jwt.decode(token, jwt_secret, algorithms=['HS256']).get('email')
    except jwt.DecodeError:
        return -1

    au_id = -1
    for i in data.return_users():
        if i['email'] == email:
            au_id = i['u_id']
    return au_id

def find_channel(channel_id):
    """Interate the channels list by its id, return the channel we need."""
    answer = None
    for i in data.channels:
        if i['channel_id'] == channel_id:
            answer = i
            break
    return answer

def find_user(user_id):
    """Find user's info by search one's id."""
    u_id = -1
    for i in data.return_users():
        if i['u_id'] == user_id:
            u_id = i
            break
    return u_id

def find_one_in_channel(channel, u_id):
    """Return a boolean variable to indicate if someone we want in the channel."""
    for i in channel['all_members']:
        if i['u_id'] == u_id:
            return True
    return False


############################################################
#       message_send(token, channel_id, message)
############################################################
def message_send(token, channel_id, message):
    """
    message_send()
    Send a message from authorised_user to the channel specified by channel_id

    Args:
        token: the token of the sender.
        channel_id: the channel which is the target of message.
        message: the message we send.

    RETURNS:
    { message_id }


    THEREFORE, TEST EVERYTHING BELOW:
    1. inputError
    - Message is more than 1000 characters

    2. accessError
    - the authorised user has not joined the channel they are trying to post to
    - cannot find the channel_id

    """
    data.init_channels()                                # Global variables.

    auth_id = token_into_user_id(token)                 # InputError 1: invalid token.
    if auth_id == -1:
        raise InputError(description='invalid token.')


    if len(message) > 1000:                              # InputError 2: Message is more than 1000 characters.
        raise InputError(description='Message is more than 1000 characters.')

    channel_got = find_channel(channel_id)              # AccessError 3: invalid channel_id.
    if channel_got is None:
        raise AccessError(description='invalid channel_id.')

    if not find_one_in_channel(channel_got, auth_id):   # AccessError 4: if the auth not in channel.
        raise AccessError(description='auth not in channel')


    new_msg_id = len(['message']) + 1                   # Case 5: no error, add the message

    # record the time rightnow
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    return_message = {                                  # create the message struct
        'message_id': new_msg_id,
        'u_id': auth_id,
        'message': message,
        'time_created': timestamp,
    }

    channel_got['message'].insert(0, return_message)    # insert the message in the top of messages in the channel.

    return {
        'message_id': new_msg_id,
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }