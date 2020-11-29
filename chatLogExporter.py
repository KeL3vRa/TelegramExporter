from pyrogram import Client
from pyrogram.errors import FloodWait
from datetime import datetime
import time
import sys
import os
from classes import classes


_FORMAT_LOG_STRING = "{:20};{:19};{};{}"
_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
_ALL_CHATS_HEADER_STRING = "SENDER;TIMESTAMP;MESSAGE;DETAILS (OPTIONAL)"
_OS_SEP = os.sep

# CHATS LOG FILE DESTINATION FOLDER NAME
_LOG_PATH = "extraction"
_DOWNLOAD_MEDIA_PATH = "media"


# Get the all messages in the chat with a given user
def getChatLogsByIdentifier(client, useridentifier):

    while True:
        try:
            formattedLog = list()

            # Create a list with ALL messages exchanged with userIdentifier
            chat = list()
            # DEBUG: for message in client.get_history(useridentifier, limit=3): instead of for message in client.iter_history(useridentifier):
            for message in client.get_history(useridentifier, limit=3):
            #for message in client.iter_history(useridentifier):
                chat.append(message)
            # Iterate over the previously created list
            for msg in chat:

                if not msg.from_user is None:
                    _sender_username = str(msg.from_user.username)
                else:
                    _sender_username = "Channel message"
                _formatted_message_date = datetime.utcfromtimestamp(msg.date).strftime(_TIME_FORMAT)

                if msg.text is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, msg.text.replace('\r', ' ').replace('\n', ' '), ""))
                elif not msg.audio is None:
                    audio_obj = classes.Audio(msg.audio)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Audio",
                                                         audio_obj.to_string())
                    formattedLog.append(log_line)
                elif not msg.document is None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Document", ""))
                elif msg.photo is not None:
                    photo_obj = classes.Photo(msg.photo)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Photo", photo_obj.to_string())
                    formattedLog.append(log_line)
                elif msg.sticker is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Sticker", ""))
                elif msg.animation is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Animation", ""))
                elif msg.game is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Game", ""))
                elif msg.video is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Video", ""))
                elif msg.voice is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Voice message", ""))
                elif msg.video_note is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Video note", ""))
                elif msg.contact is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Contact", ""))
                elif msg.location is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Location", ""))
                elif msg.venue is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Venue", ""))
                elif msg.web_page is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Web page", ""))
                elif msg.poll is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Poll", ""))
                elif msg.dice is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Dice", ""))
                elif msg.service is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Telegram service message", ""))
                elif msg.empty is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Message was deleted", ""))
                elif msg.caption is not None:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Caption", ""))
                else:
                    formattedLog.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Not possible to find the type of message", ""))
            return formattedLog

        except FloodWait:
            print("[getChatLogsOfUser] FloodWait exception may be fired by Telegram. Waiting 29s")
            time.sleep(29) # this value is specifically provided by Telegram, relating to the particular API calling which caused the exception


def media_download(client, chat, type_chat=""):
    """
    Download the media from the chat.
    If the type_chat is no "private" the function download media
    from "bot", "channel", "group" or "supergroup"
    Args:
        client: Pyrogram Client, the main means for interacting with Telegram.
        chat: message from a chat
        type_chat: "private" if message if from private chat or nothing for "bot", "channel", "group" or "supergroup"
    """

    finish_path = ""
    if type_chat == "private":
        if type(chat) is list:
            unique_id_target_chat = chat[0].id
            get_username_or_tile = chat[0].username
        else:
            unique_id_target_chat = chat.id
            get_username_or_tile = chat.username

        create_path = _DOWNLOAD_MEDIA_PATH + _OS_SEP + get_username_or_tile + _OS_SEP
    else:
        get_username_or_tile = chat[list(chat)[0]]
        unique_id_target_chat = list(chat.keys())[0]
        create_path = _DOWNLOAD_MEDIA_PATH + _OS_SEP + get_username_or_tile.replace(" ", "") + _OS_SEP

    # DEBUG: messages = client.get_history(unique_id_target_chat) <--- set this for NO LIMIT messages
    messages = client.get_history(unique_id_target_chat, limit=20)

    for message in messages:
        if message.media:
            print("Media is in download...")
            finish_path = client.download_media(message, file_name=create_path)

    if finish_path == "":
        print("No media downloaded!")
    else:
        print("Media are downloaded into: {}".format(finish_path))


def get_contact(client, target=""):
    """
    Get the contact from a target or get all contact.
    The function distinguishes between “private”, “bot”, “group”, “supergroup” or “channel”.
    Args:
        client: Pyrogram Client, the main means for interacting with Telegram.
        target: can be: full name or username or phone

    Returns:
        saved_contact: contact saved. Can be contain multiple contacts
        non_contact_chat_dict: contact from “bot”, “group”, “supergroup” or “channel”

    """
    saved_contact = list()
    non_contact_chat_dict = dict()

    print("\n[get_contact] Retrieving all matching contacts\n")
    # iterate over private chats
    for dialog in client.iter_dialogs():
        # Users and bot are handled in the same way by Telegram
        if dialog.chat.type == 'private' or dialog.chat.type == 'bot':
            user = client.get_users(dialog.chat.id)

            first_name = '' if user["first_name"] is None else str(user["first_name"]).lower()
            last_name = '' if user["last_name"] is None else str(user["last_name"]).lower()
            phone_number = '' if user["phone_number"] is None else str(user["phone_number"]).lower()
            username = '' if user["username"] is None else str(user["username"]).lower()
            full_name = first_name + " " + last_name
            is_present = True if target in full_name or target in username or target in phone_number else False

            # if user still exists and the user has specified a name to search or if he wants all users
            if (not user["is_deleted"]) and ((target != "" and is_present) or (target == "")):

                print("[get_contact] Person chat match found")
                # add the dictionary to the resulting variable
                saved_contact.append(user)

        # in this case, if dialog.chat.type is not private
        # else is "group", "supergroup" or "channel"
        else:
            title = dialog.chat.title
            if target in title.lower():
                print("[get_contact] " + dialog.chat.type + " chat match found")
                non_contact_chat_dict[dialog.chat.id] = title

    return saved_contact, non_contact_chat_dict


def menu_get_contact(client):
    target_name = input("You can enter one of the following information: "
                        "\n- Book name \n- Telegram username \n- Channel name \n- Group name "
                        "\n- Phone number (in this case remember to indicate also the phone prefix): "
                        "\n- Or press enter if you want to see a list of the chats"
                        "\n Please enter your decision: ")
    users, non_user_dict = get_contact(client, target_name.lower())

    if not users and not bool(non_user_dict):
        print("No contacts found!")
        sys.exit()

    key = 0
    total_contacts_count = len(users) + len(non_user_dict)
    if total_contacts_count > 1:
        print("\n[menu_get_contact] There are multiple matching chats. Which one do you want to choose?\n")
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

            print(str(key) + " " + chatDataToLog + "\n")
            key += 1

        for chat_id in non_user_dict:
            print(str(key) + " " + non_user_dict[chat_id])
            key += 1

        key = int(input("[menu_get_contact] Select number please: "))

        if key <= 0 or key > len(users) + len(non_user_dict):
            print("[menu_get_contact] Invalid input!!!")
            sys.exit()

    if key < len(users):
        # here we are returning a precise contact (from users list) and an empty dictionary (non_user_dict)
        return users[key], None
    else:
        # here we are returning a precise non-person chat (in the form id-name) and an empty list (users)
        return None, {list(non_user_dict)[key - len(users)] : non_user_dict[list(non_user_dict)[key - len(users)]]}


def getChatIdsByDialogs(client):

    chatIdsList = list()
    chatIdUsernamesDict = dict()
    chatIdTitleDict = dict()
    chatIdFullNameDict = dict()
    chatIdPhoneNumberDict = dict()
    deletedChatdIds = list()

    for dialog in client.iter_dialogs():
        if not dialog.chat.username is None:
            #DEBUG: TO AVOID CHANNELS COMMENT NEXT LINE ADD if dialog.chat.title is None:
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
            #DEBUG: TO AVOID CHANNELS COMMENT NEXT LINE
            chatIdsList.append(dialog.chat.id)
            chatIdTitleDict[dialog.chat.id] = dialog.chat.title
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

    return chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict


"""
Metodo che si occupa della scrittura su file di tutte le chat comprese quelle eliminate
Viene generato un file per ogni chat in modo dinamico
"""
def writeAllChatsLogsFile(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict):

    # Create logs file for every contact on the phone
    for chatId in chatIdsList:
        chat_data_to_log = ""
        header_string = _ALL_CHATS_HEADER_STRING
        if chatId in chatIdUsernamesDict:
            chat_data_to_log = chat_data_to_log + "{};".format(chatIdUsernamesDict[chatId])
        if chatId in chatIdFullNameDict:
            chat_data_to_log = chat_data_to_log + "{};".format(chatIdFullNameDict[chatId])
        if chatId in chatIdPhoneNumberDict:
            chat_data_to_log = chat_data_to_log + "{};".format(chatIdPhoneNumberDict[chatId])
        if chatId in chatIdTitleDict:
            chat_data_to_log = chat_data_to_log + "{};".format(chatIdTitleDict[chatId])

        # creating file name
        file_name = ""
        if chatId in chatIdUsernamesDict:
            file_name = file_name + "{}_".format(chatIdUsernamesDict[chatId])
        if chatId in chatIdTitleDict:
            file_name = file_name + "{}_".format(chatIdTitleDict[chatId])
        if chatId in chatIdFullNameDict:
            file_name = file_name + "{}_".format(chatIdFullNameDict[chatId])
        if chatId in chatIdPhoneNumberDict:
            file_name = file_name + "{}_".format(chatIdPhoneNumberDict[chatId])
        # Removing illegal characters from file name
        file_name = (file_name.replace("\\", "_")).replace("/", "_")
        file_name = file_name + ".csv"
        file_name = _LOG_PATH + _OS_SEP + file_name

        # Logs about existing chats
        print("[writeAllChatsLogsFile] Processing chat with {}".format(chat_data_to_log))
        with open(file_name, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
            file.write(header_string)
            for msgLog in getChatLogsByIdentifier(client, chatId):
                file.write("\n" + msgLog)

    # Logs about deleted chats
    print("[writeAllChatsLogsFile] Processing deleted chats \n\n")
    for chatId in deletedChatdIds:
        header_string = "ID"
        file_name = str(chatId) + "_deleted.csv"
        file_name = _LOG_PATH + _OS_SEP + file_name

        print("[writeAllChatsLogsFile] Processing " + str(chatId) + " deleted chat")
        with open(file_name, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
            file.write(header_string)
            for msgLog in getChatLogsByIdentifier(client, chatId):
                file.write("\n" + msgLog)


"""
Metodo che si occupa di scrivere su file le chat con UN determinato utente
"""
def writeSingleUserChatsLogsFile(client, userObject):

    # Create logs file for every contact on the phone
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

    # creating file name
    fileName = ""
    if userObject.username is not None:
        fileName = fileName + "{}_".format(userObject.username)
    if userObject.first_name is not None:
        name = userObject.first_name
        if userObject.last_name is not None:
            name = name + " " + userObject.last_name
        fileName = fileName + "{}_".format(name)
    if userObject.phone_number is not None:
        fileName = fileName + "{}_".format(userObject.phone_number)
    fileName = fileName + ".txt"
    fileName = _LOG_PATH + _OS_SEP + fileName

    print("\n[writeSingleUserChatsLogsFile] Processing " + chatDataToLog + " contact")
    with open(fileName, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
        file.write("\n -------------------- START {} -------------------- \n".format(chatDataToLog))
        for msgLog in getChatLogsByIdentifier(client, userObject.id):
            file.write("\n" + msgLog)
        file.write("\n\n -------------------- END {} -------------------- \n".format(chatDataToLog))

"""
Metodo che si occupa della scrittura su file delle chat con canali/gruppi
Il nome file viene generato dinamicamente
"""
def writeSingleNonPersonChatLogsFile(client, nonPersonDict):

    # gets the key of the unique value in the dictionary
    dictKey = list(nonPersonDict)[0]
    # Create logs file for every contact on the phone
    chatDataToLog = ""
    chatDataToLog = chatDataToLog + "Title: {} ".format(nonPersonDict[dictKey])

    fileName = ""
    fileName = fileName + "{}_".format(nonPersonDict[dictKey])
    fileName = fileName + ".txt"
    fileName = _LOG_PATH + _OS_SEP + fileName

    print("\n[writeSingleNonPersonChatLogsFile] Processing " + chatDataToLog + " chat")
    with open(fileName, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
        file.write("\n -------------------- START {} -------------------- \n".format(chatDataToLog))
        for msgLog in getChatLogsByIdentifier(client, dictKey):
            file.write("\n" + msgLog)
        file.write("\n\n -------------------- END {} -------------------- \n".format(chatDataToLog))


if __name__ == "__main__":

    # creating log path
    if not os.path.exists(_LOG_PATH):
        os.makedirs(_LOG_PATH)

    # Create an istance of the pyrogram client
    with Client("my_account") as client:

        type_of_extraction = input("Enter: \n1 to search for a single user "
                                   "        \n2 to extract all chats "
                                   "        \n3 to download media \n")
        if int(type_of_extraction) == 1:
            chatIdNameDict, nonPersonChatDict = menu_get_contact(client)
            if bool(chatIdNameDict):
                writeSingleUserChatsLogsFile(client, chatIdNameDict)
            if bool(nonPersonChatDict):
                writeSingleNonPersonChatLogsFile(client, nonPersonChatDict)
        elif int(type_of_extraction) == 2:
            # Get chats details by dialogs
            chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict = getChatIdsByDialogs(client)
            writeAllChatsLogsFile(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict)
        elif int(type_of_extraction) == 3:
            chatIdNameDict, nonPersonChatDict = menu_get_contact(client)
            if bool(chatIdNameDict):
                media_download(client, chatIdNameDict, type_chat="private")
            if bool(nonPersonChatDict):
                media_download(client, nonPersonChatDict)
        else:
            print("Please select a correct number.")
