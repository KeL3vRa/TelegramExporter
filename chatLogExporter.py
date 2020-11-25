from pyrogram import Client
from pyrogram.errors import FloodWait
from datetime import datetime
import time
import json
import sys

_FORMAT_LOG_STRING = "SENDER:{:20}        DATE:{:19}     MESSAGE:{}"
_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_contact(api_id, api_hash, filtered_name):

    with Client("my_account", api_id, api_hash) as app:
        contacts = app.get_contacts()
        saved_contact = {}
        count = 0

        for contact in contacts:
            first_name = contact["first_name"] # from a JSON get only first name
            last_name = contact["last_name"]

            if(filtered_name.lower() in first_name.lower()): # get a specific first name from a list of contacts
                count += 1
                if last_name is None:
                    saved_contact[count] = first_name + " " + contact["username"]
                else:
                    saved_contact[count] = first_name + " " + last_name + " " + contact["username"]

        return saved_contact


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
def getChatLogs(api_id, api_hash, username):
    
    formattedLog = list()
    
    with Client("my_account", api_id, api_hash) as app:
        # Create a list with ALL messages exhanged with username
        chat = list()
        for message in app.iter_history(username):
            chat.append(message)
        # Iterate over the previously created list
        for msg in chat:

            _sender_username = str(msg.from_user.username)
            _formatted_message_date = datetime.utcfromtimestamp(msg.date).strftime(_TIME_FORMAT)

            if not msg.text is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, msg.text))
            elif not msg.audio is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Audio message"))
            elif not msg.document is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Document"))
            elif not msg.photo is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Photo"))
            elif not msg.sticker is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Sticker"))
            elif not msg.animation is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Animation"))
            elif not msg.game is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Game"))
            elif not msg.video is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Video"))
            elif not msg.voice is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Voice message"))
            elif not msg.video_note is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Video note"))
            elif not msg.contact is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Contact"))
            elif not msg.location is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Location"))
            elif not msg.venue is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Venue"))
            elif not msg.web_page is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Web page"))
            elif not msg.poll is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Poll"))
            elif not msg.dice is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Dice"))
            elif not msg.service is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Telegram service message"))
            elif not msg.empty is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Message was deleted"))
            elif not msg.caption is None:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Caption"))
            else:
                formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Not possible to find the type of message"))
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

def load_configuration():

    api_id = ""
    api_hash = ""

    with open("credential.json") as json_file:
        data = json.load(json_file)
        api_id = data["api_id"]
        api_hash = data["api_hash"]
    
    return api_id, api_hash


def menu_get_contact():

    # Load api_hash and api_id from JSON file
    api_id, api_hash = load_configuration()

    target_name = input("Enter a target first name: ")
    name = get_contact(api_id, api_hash, target_name)

    if(len(name) == 0):
        print("No contacts found!")
        sys.exit()

    key = 1
    if len(name) > 1:
        print("There are multiple contacts. which one do you want to choose?")
        for key in name:
            print(str(key) + " " + name[key])

        key = int(input("Select number please: "))

        if(key < 0 or key > len(name)):
            print("C'mon duuuude!!!")
            sys.exit()

    # Split for username
    # Eg: First_Name Last_Name Username <--- take username at the end
    username = name[key].split(" ")[-1]
    print(username) 


if __name__ == "__main__":

    # Load api_hash and api_id from JSON file
    api_id, api_hash = load_configuration()

    path_to_log_file = '.\\log.txt'

    # To maintain a correspondence between userIds and phoneNumbers
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
            for msgLog in getChatLogs(api_id, api_hash, contact):
                file.write(msgLog + "\n")
            file.write(" -------------------- END  " + str(readableContactIdentifier) + " -------------------- \n")