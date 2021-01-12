from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.errors import ChatAdminRequired
from datetime import datetime
from classes import classes
import time
import sys
import os
import json
import shutil
import zipfile
import hashlib
from colorama import init

init()
_FORMAT_LOG_STRING = "{:20}§{:19}§{}§{}"
_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
_ALL_CHATS_HEADER_STRING = "SENDER§TIMESTAMP§MESSAGE§DETAILS (OPTIONAL)"
_OS_SEP = os.sep

# DATETIME FOR EXTRACTION
_extraction_date = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

# CURRENT EXTRACTION FOLDER
_EXTRACTION_FOLDER = "extraction" + _OS_SEP + "Extraction_" + _extraction_date

# PATH USED FOR THE EXTRACTION OF CHATS, MEDIA AND MEMBERS
_CHATS = "chats"
_DOWNLOAD_MEDIA_PATH = "media"
_MEMBERS_FILE_SUFFIX = "members"

_CHAT_PATH = _EXTRACTION_FOLDER + _OS_SEP + _CHATS
_MEDIA_PATH = _EXTRACTION_FOLDER + _OS_SEP + _DOWNLOAD_MEDIA_PATH
_MEMBERS_PATH = _EXTRACTION_FOLDER + _OS_SEP + _MEMBERS_FILE_SUFFIX

# EXTRACTION ZIP AND HASH FILE
_EXTRACTION_ZIP = _EXTRACTION_FOLDER + _OS_SEP + "extraction.zip"
_FILE_HASH = _EXTRACTION_FOLDER + _OS_SEP + "extraction_archive_hash.txt"


# Get the all messages in the chat with a given user
def get_chat_logs_by_identifier(client_instance, chat_identifier, directory_name):
    """
    Iterates over all messages retrieved by the chat and generates the related logs;
    if medias are found, it downloads them;
    generates the list with data associated to chat partecipants
    Args:
        client_instance: Pyrogram Client, the main means for interacting with Telegram.
        chat_identifier: the ID of the chat (username or chat_id)
        directory_name: name of the directory into which create the logs and download medias

    Returns:
        formatted_log: list with chat logs (each element of the list is a chat log)
        partecipants_ids: list with the ids associated to the partecipants of the chat
    """
    partecipants_ids = list()

    try:
        for members in client_instance.iter_chat_members(chat_identifier):
            partecipants_ids.append(members.user.id)
    except Exception as e:
        if e.__str__().__contains__("ChatParticipantsForbidden"):
            print(f"[{classes.BColor.FAIL}get_chat_logs_by_identifier{classes.BColor.ENDC}] "
                  f"Members can not be retrieved.")

    # Retrieves the folder into which create the chat's media folder
    json_config = open("configuration.json", "r")
    load_json = json.load(json_config)
    export_media = load_json["export_media"]

    # Identifies the type of chat, to obtain the channel name in case of channel chats
    chat_obj = None
    while chat_obj is None:
        try:
            chat_obj = client_instance.get_chat(chat_identifier)
        except FloodWait:
            print(f"{classes.BColor.FAIL}[get_chat_logs_by_identifier] FloodWait exception may be fired by Telegram. "
                  f"Waiting 22s{classes.BColor.ENDC}")
            time.sleep(22)  # this value is specifically provided by Telegram,
            # relating to the particular API calling which caused the exception
    chat_title = ""
    if chat_obj.type == "channel":
        if chat_obj.username is not None:
            chat_title = chat_obj.username
        else:
            chat_title = chat_obj.title

    while True:
        try:
            formatted_log = list()

            # Create a list with ALL messages exchanged with userIdentifier
            chat = list()
            # DEBUG: for message in client.get_history(chat_identifier, limit=3): instead of for message in client.iter_history(chat_identifier):
            for message in client_instance.iter_history(chat_identifier):
                chat.append(message)
            # Iterate over the previously created list
            for msg in chat:
                # export media if JSON is 1
                if export_media == 1:
                    if msg.media:
                        try:
                            create_directory = _MEDIA_PATH
                            if not os.path.exists(create_directory):
                                os.mkdir(create_directory)

                            create_path = create_directory + _OS_SEP + directory_name + _OS_SEP
                            print(
                                f"[{classes.BColor.OKBLUE}get_chat_logs_by_identifier{classes.BColor.ENDC}] Downloading attached media...")
                            client_instance.download_media(msg, file_name=create_path)
                        except ValueError:
                            print(
                                f"[{classes.BColor.FAIL}get_chat_logs_by_identifier{classes.BColor.ENDC}] This media is not downloadable.")
                        except Exception as e:
                            print('Failed to download. Reason: {}'.format(e))
                # Creates the log first column
                if msg.from_user is not None:
                    _sender_username = classes.User(msg.from_user).to_string()
                    if msg.from_user.id not in partecipants_ids:
                        partecipants_ids.append(msg.from_user.id)
                else:
                    _sender_username = chat_title
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
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date,
                                                                   "Telegram service message", ""))
                elif msg.empty is not None:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date,
                                                                   "Message was deleted", ""))
                elif msg.caption is not None:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date,
                                                                   "Caption", msg.caption))
                else:
                    formatted_log.append(_FORMAT_LOG_STRING.format(_sender_username, _formatted_message_date,
                                                                   "Not possible to find the type of message", ""))

            return formatted_log, partecipants_ids

        except FloodWait:
            print(f"{classes.BColor.FAIL}[get_chat_logs_by_identifier] FloodWait exception may be fired by Telegram. "
                  f"Waiting 29s{classes.BColor.ENDC}")
            time.sleep(29)  # this value is specifically provided by Telegram,
            # relating to the particular API calling which caused the exception


def get_contact(client_instance, targets=None):
    """
    Searches from matching chats with the ids entered by the user
    The function distinguishes between “private”, “bot”, “group”, “supergroup” or “channel”.
    Args:
        client_instance: Pyrogram Client, the main means for interacting with Telegram.
        targets: can be: list of full name, username or phone number for each user
    Returns:
        saved_contact: list of contacts saved into user's phone book
        non_contact_chat_dict: list of non-contact: “bot”, “group”, “supergroup” or “channel”

    """
    if targets is None:
        targets = []
    saved_contact = list()
    non_contact_chat_dict = dict()
    non_contact_type_dict = dict()

    print(f"\n[{classes.BColor.OKBLUE}get_contact{classes.BColor.ENDC}] Retrieving all matching contacts\n")
    # iterate over chats
    for target in targets:
        for dialog in client_instance.iter_dialogs():
            # Users and bot are handled in the same way by Telegram
            if dialog.chat.type == 'private' or dialog.chat.type == 'bot':
                user = client_instance.get_users(dialog.chat.id)

                first_name = '' if user["first_name"] is None else str(user["first_name"]).lower()
                last_name = '' if user["last_name"] is None else str(user["last_name"]).lower()
                phone_number = '' if user["phone_number"] is None else str(user["phone_number"]).lower()
                username = '' if user["username"] is None else str(user["username"]).lower()
                full_name = first_name + " " + last_name

                is_present = True if target in full_name or target in username or target in phone_number else False

                # if user still exists and the user has specified a name to search or if he wants all users
                if (not user["is_deleted"]) and ((target != "" and is_present) or (target == "")):
                    print(f"[{classes.BColor.OKBLUE}get_contact{classes.BColor.ENDC}] "
                          f"Person chat match found{classes.BColor.ENDC}")
                    # add the dictionary to the resulting variable
                    saved_contact.append(user)

            # in this case, if dialog.chat.type is not private
            # else is "group", "supergroup" or "channel"
            else:
                title = dialog.chat.title
                # for target in targets:
                if target in title.lower():
                    print(f"[{classes.BColor.OKBLUE}get_contact{classes.BColor.ENDC}] " +
                          dialog.chat.type +
                          " chat match found")

                    non_contact_chat_dict[dialog.chat.id] = title
                    non_contact_type_dict[dialog.chat.id] = dialog.chat.type

    return saved_contact, non_contact_chat_dict, non_contact_type_dict


def menu_get_contact(client_instance):
    """
        Reads user input for single researches and gives a feedback about the research (chats found or not)
        Args:
            client_instance: Pyrogram Client, the main means for interacting with Telegram.
        Returns:
            the id of the chat, distinguished as user chat or non-user chat
    """
    target_name = input("You can enter one of the following information: "
                        "\n- Phone Book name \n- Telegram username \n- Channel name \n- Group name "
                        "\n- Phone number (in this case remember to indicate also the phone prefix): "
                        "\n- Or press enter if you want to see a list of the chats"
                        "\n Please enter your decision: ")
    # necessary [target_name.lower()] as list for method get_contact
    users, non_user_dict, non_contact_type_dict = get_contact(client_instance, [target_name.lower()])

    if not users and not bool(non_user_dict):
        print(f"{classes.BColor.FAIL}No contacts found!{classes.BColor.ENDC}")
        sys.exit()

    key = 0
    total_contacts_count = len(users) + len(non_user_dict)
    if total_contacts_count > 1:
        print(f"\n[{classes.BColor.OKBLUE}menu_get_contact{classes.BColor.ENDC}]"
              f"{classes.BColor.WARNING} There are multiple matching chats. "
              f"Which one do you want to choose?{classes.BColor.ENDC}\n")
        for user in users:
            chat_data_to_log = ""
            if user.username is not None:
                chat_data_to_log = chat_data_to_log + "Username: {} ".format(user.username)
            if user.first_name is not None:
                chat_data_to_log = chat_data_to_log + "First Name: {} ".format(user.first_name)
            if user.last_name is not None:
                chat_data_to_log = chat_data_to_log + "Last Name: {} ".format(user.last_name)
            if user.phone_number is not None:
                chat_data_to_log = chat_data_to_log + "Telephone number: {} ".format(user.phone_number)

            print(f"[{classes.BColor.OKBLUE}*{classes.BColor.ENDC}] " + str(key) + " " + chat_data_to_log)
            key += 1

        for chat_id in non_user_dict:
            print(f"[{classes.BColor.OKBLUE}*{classes.BColor.ENDC}] " + str(key) + " " + non_user_dict[chat_id] + " (" + str(non_contact_type_dict[chat_id]) + ")")
            key += 1

        print(f"[{classes.BColor.OKBLUE}menu_get_contact{classes.BColor.ENDC}] Select number please: ")
        key = int(input())
        if key < 0 or key >= len(users) + len(non_user_dict):
            print(f"{classes.BColor.WARNING}[menu_get_contact] Invalid input!!!{classes.BColor.ENDC}")
            sys.exit()

    # returns the chatId connected to the user/group/channel/etc.
    if key < len(users):
        return users[key].id
    else:
        return list(non_user_dict)[key - len(users)]


def menu_get_multiple_contact(client_instance):
    """
        Reads user input (for multiple research) and splits it by ";"
        Args:
            client_instance: Pyrogram Client, the main means for interacting with Telegram.
        Returns:
            ids: list with ids of the chats
    """
    target_name = str(input("User separator ';' to select multiple name.\n"
                            "Enter your decision: "))

    non_user_dict = list()
    users = list()
    if target_name.__contains__(";"):
        users_split = target_name.split(";")
        users_split = [usr.lower() for usr in users_split]
        users_split = [usr.strip() for usr in users_split]
        users_split = list(set(users_split))
        users, non_user_dict, non_contact_type_dict = get_contact(client_instance, users_split)
    else:
        print("Please, use ;")

    if not users and not bool(non_user_dict):
        print(f"{classes.BColor.FAIL}No contacts found!{classes.BColor.ENDC}")
        sys.exit()

    key = 0
    ids = []

    for user in users:
        chat_data_to_log = ""
        if user.username is not None:
            chat_data_to_log = chat_data_to_log + "Username: {} ".format(user.username)
        if user.first_name is not None:
            chat_data_to_log = chat_data_to_log + "First Name: {} ".format(user.first_name)
        if user.last_name is not None:
            chat_data_to_log = chat_data_to_log + "Last Name: {} ".format(user.last_name)
        if user.phone_number is not None:
            chat_data_to_log = chat_data_to_log + "Telephone number: {} ".format(user.phone_number)

        print(f"[{classes.BColor.OKBLUE}*{classes.BColor.ENDC}] " + str(key) + " " + chat_data_to_log)
        key += 1
        ids.append(user.id)

    for chat_id in non_user_dict:
        print(f"[{classes.BColor.OKBLUE}*{classes.BColor.ENDC}] " + str(key) + " " + non_user_dict[chat_id] + " (" + str(non_contact_type_dict[chat_id]) + ")")
        key += 1
        ids.append(chat_id)

    return ids


def get_multiple_chat_ids_by_dialogs(client_instance, multiple_ids_chats):
    """
       Analyze the list of chat ids
       Args:
           client_instance: Pyrogram Client, the main means for interacting with Telegram.
           multiple_ids_chats: list of chats ids to analyze.
       Returns:
        chat_ids_list: list of all chat ids to analyze
        chat_id_usernames_dict: dictionary with chat_id as keys and usernames as values
        chat_id_title_dict: dictionary with chat_id as keys and chat title as values
        chat_id_full_name_dict: dictionary with chat_id as keys and full name (first name and last name) as values
        chat_id_phone_number_dict: dictionary with chat_id as keys and phone number as values
    """
    chat_ids_list = list()
    chat_id_usernames_dict = dict()
    chat_id_title_dict = dict()
    chat_id_full_name_dict = dict()
    chat_id_phone_number_dict = dict()

    for ids_chats in multiple_ids_chats:
        for dialog in client_instance.iter_dialogs():
            # If user hasn't specified a particular user to extract or if he wants to extract a particular chat
            if dialog.chat.id == ids_chats:
                # if (single_chat_id is None) or (single_chat_id is not None and dialog.chat.id == sci):
                if dialog.chat.username is not None:
                    chat_ids_list.append(dialog.chat.id)
                    chat_id_usernames_dict[dialog.chat.id] = dialog.chat.username
                    # Tries to get the person phone number retrieving his id;
                    # it's necessary a single-item list for get_users()
                    ids = list()
                    ids.append(dialog.chat.id)
                    user_obj_list = client_instance.get_users(ids)
                    if user_obj_list and user_obj_list[0].phone_number is not None:
                        chat_id_phone_number_dict[dialog.chat.id] = user_obj_list[0].phone_number

                    print(f"\n{classes.BColor.OKBLUE}[get_chat_ids_by_dialogs]{classes.BColor.ENDC}" +
                          " Retrieved chat with username: {}".format(dialog.chat.username))

                if dialog.chat.title is not None:
                    chat_ids_list.append(dialog.chat.id)
                    chat_id_title_dict[dialog.chat.id] = dialog.chat.title
                    print(f"\n{classes.BColor.OKBLUE}[get_chat_ids_by_dialogs]{classes.BColor.ENDC}" +
                          " Retrieved chat with title: {}".format(dialog.chat.title))

                if dialog.chat.first_name is not None:
                    if dialog.chat.id not in chat_ids_list:
                        chat_ids_list.append(dialog.chat.id)
                    # Identify the full name of the person who the chat relates to
                    formatted_name = dialog.chat.first_name
                    if dialog.chat.last_name is not None:
                        formatted_name = formatted_name + " " + dialog.chat.last_name
                    chat_id_full_name_dict[dialog.chat.id] = formatted_name
                    # Tries to get the person phone number retrieving his id
                    ids = list()
                    ids.append(dialog.chat.id)
                    user_obj_list = client_instance.get_users(ids)
                    if user_obj_list and user_obj_list[0].phone_number is not None:
                        chat_id_phone_number_dict[dialog.chat.id] = user_obj_list[0].phone_number

    return chat_ids_list, chat_id_usernames_dict, chat_id_title_dict, chat_id_full_name_dict, chat_id_phone_number_dict


def get_chat_ids_by_dialogs(client_instance, single_chat_id=None):
    """
       One specified chat or all chats
       Args:
           client_instance: Pyrogram Client, the main means for interacting with Telegram.
           single_chat_id: if this param is None, all chats are retrieved; otherwise, only one chat is retrieved.
       Returns:
        chat_ids_list: list of all chat ids to analyze
        chat_id_usernames_dict: dictionary with chat_id as keys and usernames as values
        chat_id_title_dict: dictionary with chat_id as keys and chat title as values
        chat_id_full_name_dict: dictionary with chat_id as keys and full name (first name and last name) as values
        deleted_chat_ids: list of deleted chats' ids
        chat_id_phone_number_dict: dictionary with chat_id as keys and phone number as values
    """
    chat_ids_list = list()
    chat_id_usernames_dict = dict()
    chat_id_title_dict = dict()
    chat_id_full_name_dict = dict()
    chat_id_phone_number_dict = dict()
    deleted_chat_ids = list()

    for dialog in client_instance.iter_dialogs():
        # If user hasn't specified a particular user to extract or if he wants to extract a particular chat
        if (single_chat_id is None) or (single_chat_id is not None and dialog.chat.id == single_chat_id):
            if dialog.chat.username is not None:
                chat_ids_list.append(dialog.chat.id)
                chat_id_usernames_dict[dialog.chat.id] = dialog.chat.username
                # Tries to get the person phone number retrieving his id;
                # it's necessary a single-item list for get_users()
                ids = list()
                ids.append(dialog.chat.id)
                user_obj_list = client_instance.get_users(ids)
                if user_obj_list and user_obj_list[0].phone_number is not None:
                    chat_id_phone_number_dict[dialog.chat.id] = user_obj_list[0].phone_number

                print(f"\n{classes.BColor.OKBLUE}[get_chat_ids_by_dialogs]{classes.BColor.ENDC}" +
                      " Retrieved chat with username: {}".format(dialog.chat.username))

            if dialog.chat.title is not None:
                chat_ids_list.append(dialog.chat.id)
                chat_id_title_dict[dialog.chat.id] = dialog.chat.title
                print(f"\n{classes.BColor.OKBLUE}[get_chat_ids_by_dialogs]{classes.BColor.ENDC}" +
                      " Retrieved chat with title: {}".format(dialog.chat.title))

            if dialog.chat.first_name is not None:
                if dialog.chat.id not in chat_ids_list:
                    chat_ids_list.append(dialog.chat.id)
                # Identify the full name of the person who the chat relates to
                formatted_name = dialog.chat.first_name
                if dialog.chat.last_name is not None:
                    formatted_name = formatted_name + " " + dialog.chat.last_name
                chat_id_full_name_dict[dialog.chat.id] = formatted_name
                # Tries to get the person phone number retrieving his id
                ids = list()
                ids.append(dialog.chat.id)
                user_obj_list = client_instance.get_users(ids)
                if user_obj_list and user_obj_list[0].phone_number is not None:
                    chat_id_phone_number_dict[dialog.chat.id] = user_obj_list[0].phone_number

            if dialog.chat.username is None and dialog.chat.title is None and dialog.chat.first_name is None:
                print("\n[get_chat_ids_by_dialogs] No info found for chat {}; "
                      "it means the other user deleted his account".format(dialog.chat.id))
                deleted_chat_ids.append(dialog.chat.id)

    return chat_ids_list, chat_id_usernames_dict, chat_id_title_dict, \
           chat_id_full_name_dict, deleted_chat_ids, chat_id_phone_number_dict


def write_all_chats_logs_file(client_instance, chat_ids_list, chat_id_usernames_dict, chat_id_title_dict,
                              chat_id_full_name_dict, deleted_chat_ids, chat_id_phone_number_dict):
    """
       Writes the chat logs for all chats (also deleted chats)
       Args:
           client_instance: Pyrogram Client, the main means for interacting with Telegram.
           single_chat_id: if this param is None, all chats are retrieved; otherwise, only one chat is retrieved.
       Returns:
        chat_ids_list: list of all chat ids to analyze
        chat_id_usernames_dict: dictionary with chat_id as keys and usernames as values
        chat_id_title_dict: dictionary with chat_id as keys and chat title as values
        chat_id_full_name_dict: dictionary with chat_id as keys and full name (first name and last name) as values
        deleted_chat_ids: list of deleted chats' ids
        chat_id_phone_number_dict: dictionary with chat_id as keys and phone number as values
    """
    header_string = _ALL_CHATS_HEADER_STRING
    # Create logs file for every contact on the phone
    for chat_id in chat_ids_list:
        chat_data_to_log = ""
        if chat_id in chat_id_usernames_dict:
            chat_data_to_log = chat_data_to_log + "{};".format(chat_id_usernames_dict[chat_id])
        if chat_id in chat_id_full_name_dict:
            chat_data_to_log = chat_data_to_log + "{};".format(chat_id_full_name_dict[chat_id])
        if chat_id in chat_id_phone_number_dict:
            chat_data_to_log = chat_data_to_log + "{};".format(chat_id_phone_number_dict[chat_id])
        if chat_id in chat_id_title_dict:
            chat_data_to_log = chat_data_to_log + "{};".format(chat_id_title_dict[chat_id])

        # creating file name
        file_name_prefix = ""
        if chat_id in chat_id_usernames_dict:
            file_name_prefix = file_name_prefix + "{}_".format(chat_id_usernames_dict[chat_id])
        if chat_id in chat_id_title_dict:
            file_name_prefix = file_name_prefix + "{}_".format(chat_id_title_dict[chat_id])
        if chat_id in chat_id_full_name_dict:
            file_name_prefix = file_name_prefix + "{}_".format(chat_id_full_name_dict[chat_id])
        if chat_id in chat_id_phone_number_dict:
            file_name_prefix = file_name_prefix + "{}_".format(chat_id_phone_number_dict[chat_id])
        # Removing illegal characters from file name name
        file_name_prefix = (file_name_prefix.replace("\\", "_")).replace("/", "_")
        # Creates the directory where to store medias
        directory_name = file_name_prefix
        file_name = file_name_prefix + ".csv"
        file_name = _CHAT_PATH + _OS_SEP + file_name

        # Logs about existing chats
        print(f"[{classes.BColor.OKBLUE}write_all_chats_logs_file{classes.BColor.ENDC}]" +
              " Processing chat with {}".format(chat_data_to_log))
        log_lines, partecipants_ids = get_chat_logs_by_identifier(client_instance, chat_id, directory_name)
        with open(file_name, 'w', encoding='utf-16') as file:  # encoding necessary to correctly represent emojis
            file.write(header_string)
            for msgLog in log_lines:
                file.write("\n" + msgLog)

        # Partecipants file
        if partecipants_ids:
            print(f"[{classes.BColor.OKBLUE}write_all_chats_logs_file{classes.BColor.ENDC}] "
                  f"Processing members chats \n\n")
            header = "MEMBERS"

            directory = _MEMBERS_PATH

            if not os.path.exists(directory):
                os.mkdir(directory)

            saving_file_path = directory + _OS_SEP + file_name_prefix + ".csv"

            with open(saving_file_path, "w", encoding="UTF-16") as file:
                file.write(header + "\n")
                for user in client_instance.get_users(partecipants_ids):
                    file.write(classes.User(user).to_string())
        else:
            print(f"[{classes.BColor.FAIL}write_all_members_channel_logs_file{classes.BColor.ENDC}] "
                  f"No members into chat " + "\n\n")

    # if there are deleted chats
    if len(deleted_chat_ids) != 0:
        # Logs about deleted chats
        print(f"[{classes.BColor.OKBLUE}write_all_chats_logs_file{classes.BColor.ENDC}] Processing deleted chats \n\n")
        for chat_id in deleted_chat_ids:
            header_string = "ID"
            directory_name = str(chat_id) + "_deleted"
            file_name = str(chat_id) + "_deleted.csv"
            file_name = _CHAT_PATH + _OS_SEP + file_name

            print(f"[{classes.BColor.OKBLUE}write_all_chats_logs_file{classes.BColor.ENDC}] Processing "
                  + str(chat_id) + " deleted chat")
            log_lines, partecipants_ids = get_chat_logs_by_identifier(client_instance, chat_id, directory_name)
            with open(file_name, 'w', encoding='utf-16') as file:  # encoding necessary to correctly represent emojis
                file.write(header_string)
                for msgLog in log_lines:
                    file.write("\n" + msgLog)


def write_group_chats_members(client_instance, chat_title_list):
    """
    Writes the log file with the partecipants of a chat.
    Log is in format: FirstName_LastName_ID or Username_ID or FirstName_ID or FirstName_LastName_ID
    Args:
        client_instance: client instance
        chat_title_list: the dictionary contained id and title for channel
    """
    for chat_id in chat_title_list:
        title = chat_title_list[chat_id]
        list_username = list()
        try:
            for member in client_instance.get_chat_members(chat_id):
                list_username.append(classes.User(member.user).to_string())
        except AttributeError:
            print(f"[{classes.BColor.FAIL}write_all_members_channel_logs_file{classes.BColor.ENDC}] "
                  f"This operation is Forbidden \n\n")
        except ChatAdminRequired:
            print(f"[{classes.BColor.FAIL}write_all_members_channel_logs_file{classes.BColor.ENDC}] "
                  f"This operation is allowed only by Admin \n\n")

        if len(list_username) != 0:
            print(f"[{classes.BColor.OKBLUE}write_all_members_channel_logs_file{classes.BColor.ENDC}] "
                  f"Processing members chats \n\n")
            header = "MEMBERS"

            # Removing illegal characters from file name name
            file_name = (title.replace("\\", "_")).replace("/", "_")
            name_file = file_name + ".csv"
            directory = _MEMBERS_PATH

            if not os.path.exists(directory):
                os.mkdir(directory)

            saved_file = directory + _OS_SEP + name_file

            with open(saved_file, "w", encoding="UTF-16") as file:
                file.write(header + "\n")
                for username in list_username:
                    file.write(username)
        else:
            print(f"[{classes.BColor.FAIL}write_all_members_channel_logs_file{classes.BColor.ENDC}] "
                  f"No members into chat " + title + "\n\n")


def clean_extraction_folder():
    """
    Cleans the entire extraction folder, deleting all previous extractions
    """
    folder = "extraction"
    print(f"[{classes.BColor.OKBLUE}clean_extraction_folder{classes.BColor.ENDC}] "
          f"Removing files from folder " + folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print(f"[{classes.BColor.OKBLUE}clean_extraction_folder{classes.BColor.ENDC}] Folder cleaned successfully\n")


def create_extraction_folders():
    """
    Creates the extraction folders used to save extracted chats, media and members
    """
    print(f"[{classes.BColor.OKBLUE}create_extraction_folders{classes.BColor.ENDC}] Creating extraction folders")

    # creating chat path
    if not os.path.exists(_CHAT_PATH):
        os.makedirs(_CHAT_PATH)

    # creating members path
    if not os.path.exists(_MEMBERS_PATH):
        os.makedirs(_MEMBERS_PATH)

    # creating media path
    if not os.path.exists(_MEDIA_PATH):
        os.makedirs(_MEDIA_PATH)

    print(
        f"[{classes.BColor.OKBLUE}create_extraction_folders{classes.BColor.ENDC}] Extraction folders created successfully")


def compress_and_hash_extraction():
    """
    Creates a zip archive with the content of the current extraction
    and a txt file wish the hashes of the archive in MD5 and SHA512
    """

    print(
        f"[{classes.BColor.OKBLUE}compress_and_hash_extraction{classes.BColor.ENDC}] Creating extraction zip archive...")
    try:
        zip_file = zipfile.ZipFile(_EXTRACTION_ZIP, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(_CHAT_PATH):
            for file in files:
                zip_file.write(os.path.join(root, file))

        for root, dirs, files in os.walk(_MEDIA_PATH):
            for file in files:
                zip_file.write(os.path.join(root, file))

        for root, dirs, files in os.walk(_MEMBERS_PATH):
            for file in files:
                zip_file.write(os.path.join(root, file))

        zip_file.close()
        print(
            f"[{classes.BColor.OKBLUE}compress_and_hash_extraction{classes.BColor.ENDC}] Extraction zip archive created successfully")
    except Exception:
        print(f"{classes.BColor.FAIL}Error creating zip archive{classes.BColor.ENDC}")

    try:
        print(f"[{classes.BColor.OKBLUE}compress_and_hash_extraction{classes.BColor.ENDC}] Creating zip hashes...")
        sha512_hash = hashlib.sha512()
        md5_hash = hashlib.md5()

        with open(_EXTRACTION_ZIP, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha512_hash.update(byte_block)
                md5_hash.update(byte_block)

        sha = sha512_hash.hexdigest()
        md5 = md5_hash.hexdigest()

        with open(_FILE_HASH, 'w', encoding='utf-16') as file:
            file.write('MD5: ' + md5)
            file.write('\nSHA512: ' + sha)

        print(
            f"[{classes.BColor.OKBLUE}compress_and_hash_extraction{classes.BColor.ENDC}] Zip hashes created successfully")
    except Exception:
        print(f"{classes.BColor.FAIL}Error creating hash file{classes.BColor.ENDC}")


def show_banner():
    print(" _______   _                                  ______                       _          \n"
          "|__   __| | |                                |  ____|                     | |           \n"
          "   | | ___| | ___  __ _ _ __ __ _ _ __ ___   | |__  __  ___ __   ___  _ __| |_ ___ _ __ \n"
          "   | |/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \  |  __| \ \/ / '_ \ / _ \| '__| __/ _ \ '__|\n"
          "   | |  __/ |  __/ (_| | | | (_| | | | | | | | |____ >  <| |_) | (_) | |  | ||  __/ |   \n"
          "   |_|\___|_|\___|\__, |_|  \__,_|_| |_| |_| |______/_/\_\ .__/ \___/|_|   \__\___|_|   \n"
          "                   __/ |                                 | |                            \n"
          "                  |___/                                  |_|                -By DMD     \n"
          )


if __name__ == "__main__":
    show_banner()
    response = -1
    # Create an instance of the pyrogram client
    while response != 0:
        with Client("my_account", hide_password=True) as client:

            if os.path.exists("extraction"):
                clean_folder = input("Do you want to clean extraction folder from previous extractions files? (y/N): ")
                if clean_folder == 'y':
                    clean_extraction_folder()

            create_extraction_folders()
            try:
                type_of_extraction = int(input("\nEnter: \n[1] to extract the chats for a single user "
                                               "         \n[2] to extract the chats for multiple users"
                                               "         \n[3] to extract all chats"
                                               "         \n[-1] to quit"   
                                               "         \nPlease enter your choice: "))

                if type_of_extraction == 1:
                    # Get chat logs for a user-specified chat
                    chatId = menu_get_contact(client)
                    chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatIds, chatIdPhoneNumberDict = get_chat_ids_by_dialogs(
                        client, chatId)
                    write_all_chats_logs_file(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict,
                                              chatIdFullNameDict, deletedChatIds, chatIdPhoneNumberDict)
                    compress_and_hash_extraction()

                elif type_of_extraction == 2:
                    chatIds = menu_get_multiple_contact(client)
                    chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, chatIdPhoneNumberDict = \
                        get_multiple_chat_ids_by_dialogs(client, chatIds)
                    write_all_chats_logs_file(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict,
                                              chatIdFullNameDict, [], chatIdPhoneNumberDict)
                    compress_and_hash_extraction()

                elif type_of_extraction == 3:
                    # Get chat logs for all chats
                    chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict, deletedChatIds, chatIdPhoneNumberDict = get_chat_ids_by_dialogs(
                        client)
                    write_all_chats_logs_file(client, chatIdsList, chatIdUsernamesDict, chatIdTitleDict, chatIdFullNameDict,
                                              deletedChatIds, chatIdPhoneNumberDict)

                    compress_and_hash_extraction()
                elif type_of_extraction == -1:
                    response = 0
                else:
                    print("Please select a correct number.")
            except ValueError:
                print("Please select a correct number.")
