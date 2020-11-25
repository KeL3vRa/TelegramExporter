from pyrogram import Client
from pyrogram.errors import FloodWait
from datetime import datetime
import time

def getContactNames(api_id, api_hash, idPhoneDictionary):
    
    with Client("my_account", api_id, api_hash) as app:
        
        contactsUsernames = list()
        # Gets contacts details
        contacts = app.get_contacts()
        for contact in contacts:
            if not contact.username is None:
                contactsUsernames.append(contact.username)
            elif not contact.phone_number is None:
                print("\nUsername not found for phone number {}".format(contact.phone_number))
                correspondantId = getIdFromNumber(app, api_id, api_hash, contact.phone_number)
                print("\nCorrespondant chat ID is:{}".format(correspondantId))
                idPhoneDictionary[correspondantId] = contact.phone_number
                contactsUsernames.append(correspondantId)
            else:
                formattedName = contact.first_name
                if not contact.last_name is None:
                    formattedName = formattedName + "_" + contact.last_name
                print("username or phone number not found for {}".format(formattedName))
        
        return contactsUsernames


# Get the last N messages of a chat
def getChatLogs(api_id, api_hash, username, n_messages):
    
    formattedLog = list()
    
    with Client("my_account", api_id, api_hash) as app:
        #TODO: substitute with iter_history()
        chat = app.get_history(username, limit=n_messages)
        for msg in chat:
            #print("SENDER:{:20}".format(msg.from_user.username))
            #print("DATE:{:19}".format(datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S')))
            #print("MESSAGE:{}".format(str(msg.text)))
            if not msg.text is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), msg.text))
            elif not msg.audio is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Audio message"))
            elif not msg.document is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Document"))
            elif not msg.photo is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Photo"))
            elif not msg.sticker is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Sticker"))
            elif not msg.animation is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Animation"))
            elif not msg.game is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Game"))
            elif not msg.video is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Video"))
            elif not msg.voice is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Voice message"))
            elif not msg.video_note is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Video note"))
            elif not msg.contact is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Contact"))
            elif not msg.location is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Location"))
            elif not msg.venue is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Venue"))
            elif not msg.web_page is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Web page"))
            elif not msg.poll is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Poll"))
            elif not msg.dice is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Dice"))
            elif not msg.service is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Telegram service message"))
            elif not msg.empty is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Message was deleted"))
            elif not msg.caption is None:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(msg.from_user.username, datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Caption"))
            else:
                formattedLog.append("SENDER:{:20}        DATE:{:19}     MESSAGE:{}".format(str(msg.from_user.username), datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'), "Not possible to find the type of message"))
        return formattedLog


def getChatDetails(api_id, api_hash, username):
    
    with Client("my_account", api_id, api_hash) as app:
        
        # Gets the details of a chat
        chat_details = app.get_chat(username)
        
        return chat_details


def getIdFromNumber(client, api_id, api_hash, phoneNumber):
    
    while True:
        # Gets the details of a chat
        try:
            chat_details = client.get_chat(phoneNumber)
            return chat_details.id
        
        except FloodWait as exception:
            time.sleep(28) #this value is specifically provided by Telegram, relating to the particular API calling which caused the exception



api_id = INSERT_API_NUMBER
api_hash = "INSERT_API_HASH"
num_of_messages_to_retrieve = 5
path_to_log_file = '.\\log.txt'

# To mantai a correspondence beteen userIds and phoneNumbers
usernamesPhoneDictionary = dict()
# Retrieve all contacts' name
contactNames = getContactNames(api_id, api_hash, usernamesPhoneDictionary)
print(contactNames)

# Create logs file
with open(path_to_log_file, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
    for contact in contactNames:
        readableContactIdentifier = contact
        # Necessary to log the phone number instead of the userId
        if contact in usernamesPhoneDictionary:
            readableContactIdentifier = usernamesPhoneDictionary[contact]
            
        file.write("\n -------------------- START " + str(readableContactIdentifier) + " -------------------- \n")
        for msgLog in getChatLogs(api_id, api_hash, contact, num_of_messages_to_retrieve):
            file.write(msgLog + "\n")
        file.write(" -------------------- END  " + str(readableContactIdentifier) + " -------------------- \n")