from pyrogram import Client
from pyrogram.errors import FloodWait
from datetime import datetime
from classes import classes
import time
import sys
import os
import json


_FORMAT_LOG_STRING = "{:20};{:19};{};{}"
_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
_ALL_CHATS_HEADER_STRING = "SENDER;TIMESTAMP;MESSAGE;DETAILS (OPTIONAL)"
_OS_SEP = os.sep

# CHATS LOG FILE DESTINATION FOLDER NAME
_LOG_PATH = "extraction"
_DOWNLOAD_MEDIA_PATH = "media"


# Get the all messages in the chat with a given user
def getChatLogsByIdentifier(client, useridentifier, directory_name):
    json_config = open("configuration.json", "r")
    load_json = json.load(json_config)
    export_media = load_json["export_media"]

    while True:
        try:
            formatted_log = list()

            # Create a list with ALL messages exchanged with userIdentifier
            chat = list()
            # DEBUG: for message in client.get_history(useridentifier, limit=3): instead of for message in client.iter_history(useridentifier):
            for message in client.get_history(useridentifier, limit=3):
            #for message in client.iter_history(useridentifier):
                chat.append(message)
            # Iterate over the previously created list
            for msg in chat:
                # export media if JSON is 1
                if export_media == 1:
                    if msg.media:
                        try:
                            create_path = _LOG_PATH + _OS_SEP + _DOWNLOAD_MEDIA_PATH + _OS_SEP + directory_name + _OS_SEP
                            print("Media are downloaded...")
                            client.download_media(msg, file_name=create_path)
                        except ValueError:
                            print("This media is not downloadable.")
                # Creates the log first column
                if msg.from_user is not None:
                    _sender_username = str(msg.from_user.username)
                else:
                    _sender_username = "Channel message"
                _formatted_message_date = datetime.utcfromtimestamp(msg.date).strftime(_TIME_FORMAT)

                if msg.text is not None:
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date,
                                                         msg.text.replace('\r', ' ').replace('\n', ' '), "")
                    formatted_log.append(log_line)
                elif msg.audio is not None:
                    audio_obj = classes.Audio(msg.audio)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Audio",
                                                         audio_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.document is not None:
                    doc_obj = classes.Document(msg.document)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Document",
                                                         doc_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.photo is not None:
                    photo_obj = classes.Photo(msg.photo)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Photo",
                                                         photo_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.sticker is not None:
                    sticker_obj = classes.Sticker(msg.sticker)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Sticker",
                                                         sticker_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.animation is not None:
                    animation_obj = classes.Animation(msg.animation)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Animation",
                                                         animation_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.game is not None:
                    game_obj = classes.Game(msg.game)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Game",
                                                         game_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.video is not None:
                    video_obj = classes.Video(msg.video)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Video",
                                                         video_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.voice is not None:
                    voice_obj = classes.Voice(msg.voice)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Voice message",
                                                         voice_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.video_note is not None:
                    videonote_obj = classes.Videonote(msg.video_note)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Video note",
                                                         videonote_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.contact is not None:
                    contact_obj = classes.Contact(msg.contact)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Contact",
                                                         contact_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.location is not None:
                    location_obj = classes.Location(msg.location)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Location",
                                                         location_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.venue is not None:
                    venue_obj = classes.Venue(msg.venue)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Venue",
                                                         venue_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.web_page is not None:
                    web_page_obj = classes.WebPage(msg.web_page)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Web page",
                                                         web_page_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.poll is not None:
                    poll_obj = classes.Poll(msg.poll)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Poll",
                                                         poll_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.dice is not None:
                    dice_obj = classes.Dice(msg.dice)
                    log_line = _FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Dice",
                                                         dice_obj.to_string())
                    formatted_log.append(log_line)
                elif msg.service is not None:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Telegram service message", ""))
                elif msg.empty is not None:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Message was deleted", ""))
                elif msg.caption is not None:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Caption", msg.caption))
                else:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date, "Not possible to find the type of message", ""))
            return formatted_log

        except FloodWait:
            print("[getChatLogsOfUser] FloodWait exception may be fired by Telegram. Waiting 29s")
            time.sleep(29) # this value is specifically provided by Telegram, relating to the particular API calling which caused the exception


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

            print(str(key) + " " + chatDataToLog)
            key += 1

        for chat_id in non_user_dict:
            print(str(key) + " " + non_user_dict[chat_id])
            key += 1

        key = int(input("[menu_get_contact] Select number please: "))
        if key < 0 or key > len(users) + len(non_user_dict):
            print("[menu_get_contact] Invalid input!!!")
            sys.exit()

    #returns the chatId connected to the user/gruop/channel/etc.
    if key < len(users):
        return users[key].id
    else:
        return list(non_user_dict)[key - len(users)]


def getChatIdsByDialogs(client, singleChatId = None):

    chatIdsList = list()
    chatIdUsernamesDict = dict()
    chatIdTitleDict = dict()
    chatIdFullNameDict = dict()
    chatIdPhoneNumberDict = dict()
    deletedChatdIds = list()

    for dialog in client.iter_dialogs():
        #If user hasn't specified a particular user to extrat or if he wants to extract a particular chat
        if (singleChatId is None) or (singleChatId is not None and dialog.chat.id == singleChatId):
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
        # directory_name = ""
        if chatId in chatIdUsernamesDict:
            file_name = file_name + "{}_".format(chatIdUsernamesDict[chatId])
        if chatId in chatIdTitleDict:
            file_name = file_name + "{}_".format(chatIdTitleDict[chatId])
        if chatId in chatIdFullNameDict:
            file_name = file_name + "{}_".format(chatIdFullNameDict[chatId])
            directory_name = chatIdFullNameDict[chatId]
        if chatId in chatIdPhoneNumberDict:
            file_name = file_name + "{}_".format(chatIdPhoneNumberDict[chatId])
        # Removing illegal characters from file name
        file_name = (file_name.replace("\\", "_")).replace("/", "_")
        directory_name = file_name
        file_name = file_name + ".csv"
        file_name = _LOG_PATH + _OS_SEP + file_name

        # Logs about existing chats
        print("[writeAllChatsLogsFile] Processing chat with {}".format(chat_data_to_log))
        with open(file_name, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
            file.write(header_string)
            for msgLog in getChatLogsByIdentifier(client, chatId, directory_name):
                file.write("\n" + msgLog)

    #if there are deleted chats
    if len(deletedChatdIds) != 0:
        # Logs about deleted chats
        print("[writeAllChatsLogsFile] Processing deleted chats \n\n")
        for chatId in deletedChatdIds:
            header_string = "ID"
            directory_name = str(chatId) + "_deleted"
            file_name = str(chatId) + "_deleted.csv"
            file_name = _LOG_PATH + _OS_SEP + file_name

            print("[writeAllChatsLogsFile] Processing " + str(chatId) + " deleted chat")
            with open(file_name, 'w', encoding='utf-8') as file:  # encoding necessary to correctly represent emojis
                file.write(header_string)
                for msgLog in getChatLogsByIdentifier(client, chatId, directory_name):
                    file.write("\n" + msgLog)


if __name__ == "__main__":

    # creating log path
    if not os.path.exists(_LOG_PATH):
        os.makedirs(_LOG_PATH)

    # Create an istance of the pyrogram client
    with Client("my_account") as client:

        type_of_extraction = input("Enter: \n1 to search for a single user "
                                   "        \n2 to extract all chats"
                                   "        \nPlease enter your choice: ")

        if int(type_of_extraction) == 1:
            # Get a particular chat decide by the user
            chatId = menu_get_contact(client)
            chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict = getChatIdsByDialogs(client, chatId)
            writeAllChatsLogsFile(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict)

        elif int(type_of_extraction) == 2:
            # Get chats details by dialogs
            chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict = getChatIdsByDialogs(client)
            writeAllChatsLogsFile(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatdIds, chatIdPhoneNumberDict)

        else:
            print("Please select a correct number.")
