from pyrogram import Client
from pyrogram.errors import FloodWait
from datetime import datetime
import time
import json
import sys
from os import path

_FORMAT_LOG_STRING = "SENDER:{:20}        DATE:{:19}     MESSAGE:{}"
_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_contact(client, target_name=""):

    saved_contact = list()
    channels_dict = dict()
    count = 0

    print("\n[get_contact] Retrieving all matching contacts")
    #iterate over private chats
    for dialog in client.iter_dialogs():
        if dialog.chat.type == 'private':
            user = client.get_users(dialog.chat.id)

            first_name = '' if user["first_name"] is None else str(user["first_name"]).lower()
            last_name = '' if user["last_name"] is None else str(user["last_name"]).lower()
            phone_number = '' if user["phone_number"] is None else str(user["phone_number"]).lower()
            username = '' if user["username"] is None else str(user["username"]).lower()
            

            #if user still exists and the user has specified a name to search or if he wants all users
            if (not user["is_deleted"]) and ((target_name.lower() != "" and target_name.lower() in [first_name, last_name, phone_number, username, title]) or (target_name == "")):
                count += 1

                print("\n[get_contact] Chat match found")
                #add the dictionary to a global variable
                saved_contact.append(user)

        elif dialog.chat.type == 'channel':
            title = dialog.chat.title
            if (target_name.lower() in title.lower()):
                print("\n[get_contact] Channel match found")
                channels_dict[dialog.chat.id] = title

    return saved_contact, channels_dict

def generateContactsNames(client):
    
    contactsUsernames = list()
    tgIdPhoneDictionary = dict()
    # Gets contacts details
    contacts = client.get_contacts()
    for contact in contacts:
        if not contact.username is None:
            contactsUsernames.append(contact.username)
        elif not contact.phone_number is None:
            print("\n[generateContactsNames] Username not found for phone number {}".format(contact.phone_number))
            correspondantId = getChatIdFromPhoneNumber(client, contact.phone_number)
            # Identify the full name of the person who owns the phone number
            formattedName = contact.first_name
            if not contact.last_name is None:
                formattedName = formattedName + " " + contact.last_name
            tgIdPhoneDictionary[correspondantId] = formattedName
            print("[generateContactsNames] Is is owned by {}".format(formattedName))
            # Adds the contact name to the list
            contactsUsernames.append(correspondantId)
        else:
            formattedName = contact.first_name
            if not contact.last_name is None:
                formattedName = formattedName + "_" + contact.last_name
            print("[generateContactsNames] username or phone number not found for {}".format(formattedName))
        
    return contactsUsernames, tgIdPhoneDictionary


# Get the all messages in the chat with a given user
def getChatLogsOfUser(client, useridentifier):
    
    while True:
        try:
            formattedLog = list()
    
            # Create a list with ALL messages exhanged with useridentifier
            chat = list()
            for message in client.iter_history(useridentifier):
                chat.append(message)
            # Iterate over the previously created list
            for msg in chat:

                if not msg.from_user is None:
                    _sender_username = str(msg.from_user.username)
                else :
                    _sender_username = "Channel message"
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
        
        except FloodWait:
            print("[getChatLogsOfUser] FloodWait exception may be fired by Telegram. Waiting 29s")
            time.sleep(29) #this value is specifically provided by Telegram, relating to the particular API calling which caused the exception


def getChatIdFromPhoneNumber(client, phoneNumber):
    
    while True:
        # Gets the details of a chat
        try:
            chat_details = client.get_chat(phoneNumber)
            return chat_details.id
        
        except FloodWait:
            print("[getIdFromNumber] FloodWait exception may be fired by Telegram. Waiting 28s")
            time.sleep(28) #this value is specifically provided by Telegram, relating to the particular API calling which caused the exception


def menu_get_contact(client):
    target_name = input("You can enter one of the following informations: \n- Book name \n- Telegram username \n- Channel name \n- Phone number (in this case remember to indicate also the phone prefix): ")
    users, channels_dict = get_contact(client, target_name)

    if not users and not bool(channels_dict):
        print("No contacts found!")
        sys.exit()

    key = 0
    total_contacts_count = len(users) + len(channels_dict)
    if total_contacts_count > 1:
        print("There are multiple contacts. which one do you want to choose?")
        for user in users:
            chatDataToLog = ""
            if user.username is not None:
                chatDataToLog = chatDataToLog + "Username: {} ".format(user.username)
            if user.first_name is not None:
                chatDataToLog = chatDataToLog + "First Name: {} ".format(user.first_name)
            if user.last_name is not None:
                chatDataToLog = chatDataToLog + "Last Name: {} ".format(user.last_name)
            if user.phone_number is not None:
                chatDataToLog = chatDataToLog + "Telephone number: {} ".format(user.phone_number)

            print(str(key) + " " + chatDataToLog)
            key += 1
        
        print("There are multiple channels. which one do you want to choose?")
        for channel_id in channels_dict:
            print(str(key) + " " + channels_dict[channel_id])
            key += 1

        key = int(input("Select number please: "))

        if(key < 0 or key > len(users) + len(channels_dict)):
            print("Invalid input!!!")
            sys.exit()

    if(key < len(users)):
        # here we are returning a precise contact (from users list) and an empty dictionary (channels_dict)
        return users[key], channels_dict
    else:
        # here we are returning a precise channel (in the form id-name) and an empty list (users)
        return users, {list(channels_dict)[key - len(users)] : channels_dict[list(channels_dict)[key - len(users)]]}
        


def load_app_configuration(configFileName):

    config_file = open(configFileName,"r")
    config_keys = json.load(config_file)
    config_file.close()

    all_contacts_chat_logs_file_path = config_keys["all_contacts_chat_logs_file_path"]
    identifiers_phone_numbers_dump_file = config_keys["identifiers_phone_numbers_dump_path"]
    identifiers_list_dump_file = config_keys["identifiers_list_dump_path"]
    
    return all_contacts_chat_logs_file_path, identifiers_phone_numbers_dump_file, identifiers_list_dump_file


def getContactsData(client, path_identifiers_phone_numbers_file, path_identifiers_list_file):

    # Generates contacts list only the first execution
    if not path.exists(path_identifiers_list_file) or not path.exists(path_identifiers_phone_numbers_file):
        # Retrieve all contacts' names and the corresponance identifier_phoneNumber
        contactNames, tgIdPhoneDictionary = generateContactsNames(client)
        # Dumps tgIdPhoneDictionary dict
        file = open(path_identifiers_phone_numbers_file,"w")
        json.dump(tgIdPhoneDictionary, file)
        file.close()
        print("[getContactsData] correspondance identifier_phoneNumber dumped")
        # Dumps identifiers list
        file = open(path_identifiers_list_file,"w")
        json.dump(contactNames, file)
        file.close()
        print("[getContactsData] contacts' names list dumped")
    else :
        # Loads tgIdPhoneDictionary dict
        dump_file = open(path_identifiers_phone_numbers_file, "r")
        tgIdPhoneDictionary = json.load(dump_file)
        dump_file.close()
        print("[getContactsData] corresponance identifier_phoneNumber loaded")
        # Loads identifiers dict
        dump_file = open(path_identifiers_list_file, "r")
        contactNames = json.load(dump_file)
        dump_file.close()
        print("[getContactsData] contacts' names list loaded")

    return tgIdPhoneDictionary, contactNames


def getChatIdsByDialogs(client):

    chatIdsList = list()
    chatIdUsernamesDict = dict()
    chatIdChannelTitleDict = dict()
    chatIdFullNameDict = dict()
    chatIdPhoneNumberDict = dict()
    deletedChatdIds = list()

    for dialog in client.iter_dialogs():
        if not dialog.chat.username is None:
            #TO AVOID CHANNELS COMMENT NEXT LINE ADD if dialog.chat.title is None:
            chatIdsList.append(dialog.chat.id)
            chatIdUsernamesDict[dialog.chat.id] = dialog.chat.username
            # Tries to get the person phone number retrieving his id
            ids = list()
            ids.append(dialog.chat.id)
            userObjsList = client.get_users(ids)
            if userObjsList and userObjsList[0].phone_number is not None:
                chatIdPhoneNumberDict[dialog.chat.id] = userObjsList[0].phone_number

            print("\n[getChatIdsByDialogs] Retrieved chat with username: {}".format(dialog.chat.username))
        
        if not dialog.chat.title is None:
            #TO AVOID CHANNELS COMMENT NEXT LINE
            chatIdsList.append(dialog.chat.id)
            chatIdChannelTitleDict[dialog.chat.id] = dialog.chat.title
            print("\n[getChatIdsByDialogs] Retrieved chat with title: {}".format(dialog.chat.title))

        if not dialog.chat.first_name is None:
            if not dialog.chat.id in chatIdsList:
                chatIdsList.append(dialog.chat.id)
            # Identify the full name of the person who the chat relates to
            formattedName = dialog.chat.first_name
            if not dialog.chat.last_name is None:
                formattedName = formattedName + " " + dialog.chat.last_name
            chatIdFullNameDict[dialog.chat.id] = formattedName
            # Tries to get the person phone number retrieving his id
            ids = list()
            ids.append(dialog.chat.id)
            userObjsList = client.get_users(ids)
            if userObjsList and userObjsList[0].phone_number is not None:
                chatIdPhoneNumberDict[dialog.chat.id] = userObjsList[0].phone_number

        if dialog.chat.username is None and dialog.chat.title is None and dialog.chat.first_name is None:
            print("\n[getChatIdsByDialogs] No info found for chat {}; it means the other user deleted his account".format(dialog.chat.id))
            deletedChatdIds.append(dialog.chat.id)

    return chatIdsList, chatIdUsernamesDict, chatIdChannelTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict


def writeAllChatsLogsFile(client, all_contacts_chat_logs_file_path, chatIdsList, chatIdUsernamesDict, chatIdChannelTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict):

    # Create logs file for every contact on the phone
    with open(all_contacts_chat_logs_file_path, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
        # Logs about existing chats
        for chatId in chatIdsList:
            chatDataToLog = ""
            if chatId in chatIdUsernamesDict:
                chatDataToLog = chatDataToLog + "Username: {} ".format(chatIdUsernamesDict[chatId])
            if chatId in chatIdChannelTitleDict:
                chatDataToLog = chatDataToLog + "ChannelName: {} ".format(chatIdChannelTitleDict[chatId])
            if chatId in chatIdFullNameDict:
                chatDataToLog = chatDataToLog + "Full Name: {} ".format(chatIdFullNameDict[chatId])
            if chatId in chatIdPhoneNumberDict:
                chatDataToLog = chatDataToLog + "Phone number: {} ".format(chatIdPhoneNumberDict[chatId])

            print("[writeAllChatsLogsFile] Processing chat with {}".format(chatDataToLog))
            file.write("\n -------------------- START {} -------------------- \n".format(chatDataToLog))
            for msgLog in getChatLogsOfUser(client, chatId):
                file.write("\n" + msgLog)
            file.write("\n -------------------- END {} -------------------- \n".format(chatDataToLog))
        # Logs about deleted chats
        file.write("\n\n ///////////////////  DELETED CHATS \\\\\\\\\\\\\\\\\\\\ \n\n")
        for chatId in deletedChatdIds:
            print("[writeAllChatsLogsFile] Processing " + str(chatId) + " deleted chat")
            file.write("\n -------------------- START " + str(chatId) + " -------------------- \n")
            for msgLog in getChatLogsOfUser(client, chatId):
                file.write("\n" + msgLog)
            file.write("\n -------------------- END  " + str(chatId) + " -------------------- \n")


def writeAllContactsChatsLogsFile(client, all_contacts_chat_logs_file_path, contactNames, tgIdPhoneDictionary):

    # Create logs file for every contact on the phone
        with open(all_contacts_chat_logs_file_path, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
            for contact in contactNames:
                stringContact = str(contact)
                # Necessary to log the book name instead of the userId
                if stringContact in tgIdPhoneDictionary:
                    stringContact = tgIdPhoneDictionary[stringContact]
                print("[writeAllContactsChatsLogsFile] Processing " + stringContact + " contact")
                
                file.write("\n -------------------- START " + stringContact + " -------------------- \n")
                for msgLog in getChatLogsOfUser(client, contact):
                    file.write("\n" + msgLog)
                file.write("\n -------------------- END  " + stringContact + " -------------------- \n")


def writeSingleUserChatsLogsFile(client, all_contacts_chat_logs_file_path, userObject):

    # Create logs file for every contact on the phone
    with open(all_contacts_chat_logs_file_path, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
        chatDataToLog = ""
        if userObject.username is not None:
            chatDataToLog = chatDataToLog + "Username: {} ".format(userObject.username)
        if userObject.first_name is not None:
            name = userObject.first_name
            if userObject.last_name is not None:
                name = name + " " + userObject.last_name
            chatDataToLog = chatDataToLog + "Full Name: {} ".format(name)
        if userObject.phone_number is not None:
            chatDataToLog = chatDataToLog + "Phone number: {} ".format(userObject.phone_number)
        
        print("\n[writeSingleUserChatsLogsFile] Processing " + chatDataToLog + " contact")
        file.write("\n -------------------- START {} -------------------- \n".format(chatDataToLog))
        for msgLog in getChatLogsOfUser(client, userObject.id):
            file.write("\n" + msgLog)
        file.write("\n -------------------- END {} -------------------- \n".format(chatDataToLog))


def writeSingleChannelChatsLogsFile(client, all_contacts_chat_logs_file_path, channelDict):

    # Create logs file for every contact on the phone
    with open(all_contacts_chat_logs_file_path, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
        chatDataToLog = print(channelDict)
        chatDataToLog = ""
        chatDataToLog = chatDataToLog + "Title: {} ".format(channelDict[list(channelDict)[0]])
        
        print("\n[writeSingleChannelChatsLogsFile] Processing " + chatDataToLog + " channel")
        file.write("\n -------------------- START {} -------------------- \n".format(chatDataToLog))
        for msgLog in getChatLogsOfUser(client, list(channelDict)[0]):
            file.write("\n" + msgLog)
        file.write("\n -------------------- END {} -------------------- \n".format(chatDataToLog))


if __name__ == "__main__":

    # Load configuration values
    config_file_name = "app_config.json"
    all_contacts_chat_logs_file_path, path_identifiers_phone_numbers_file, path_identifiers_list_file = load_app_configuration(config_file_name)

    # Create an istance of the pyrogram client
    with Client("my_account") as client:

        type_of_extraction = input("Enter: \n1 to search for a single user \n2 to extract all chats: \n")
        if int(type_of_extraction) == 1:
            chatIdNameDict, channelDict = menu_get_contact(client)
            if bool(chatIdNameDict):
                writeSingleUserChatsLogsFile(client, all_contacts_chat_logs_file_path, chatIdNameDict)
            if bool(channelDict):
                writeSingleChannelChatsLogsFile(client, all_contacts_chat_logs_file_path, channelDict)
        else:
            # Get chats details by dialogs
            chatIdsList, chatIdUsernamesDict, chatIdChannelTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict = getChatIdsByDialogs(client)
            writeAllChatsLogsFile(client, all_contacts_chat_logs_file_path, chatIdsList, chatIdUsernamesDict, chatIdChannelTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict)
       
        # Gets the list of contacts saved into user's book
        #tgIdPhoneDictionary, contactNames = getContactsData(client, path_identifiers_phone_numbers_file, path_identifiers_list_file)
        
        # Create the log file with all chats fro every user
        #writeAllContactsChatsLogsFile(client, all_contacts_chat_logs_file_path, contactNames, tgIdPhoneDictionary)
