from datetime import datetime


class Photo:

    def __init__(self, pyrogram_photo_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_photo_obj.file_id
        self.width = pyrogram_photo_obj.width
        self.height = pyrogram_photo_obj.height
        self.size = pyrogram_photo_obj.file_size
        self.date = datetime.utcfromtimestamp(pyrogram_photo_obj.date).strftime(_TIME_FORMAT)
        self.ttl_seconds = "" if pyrogram_photo_obj.ttl_seconds is None else str(pyrogram_photo_obj.ttl_seconds)

    def to_string(self):
        return_string = "id = {}, width = {}, height = {}, size = {}, date = {}".format(self.id, self.width,
                                                                                        self.height, self.size,
                                                                                        self.date)
        return_string = return_string + ", TTL(s) = {}".format(self.ttl_seconds) if self.ttl_seconds != "" \
            else return_string

        return return_string


class Audio:
    def __init__(self, pyrogram_audio_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_audio_obj.file_id
        self.duration = pyrogram_audio_obj.duration
        self.file_name = "" if pyrogram_audio_obj.file_name is None else pyrogram_audio_obj.file_name
        self.mime_type = "" if pyrogram_audio_obj.mime_type is None else pyrogram_audio_obj.mime_type
        self.size = "" if pyrogram_audio_obj.file_size is None else str(pyrogram_audio_obj.file_size)
        self.date = "" if pyrogram_audio_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_audio_obj.date).strftime(_TIME_FORMAT))
        self.performer = "" if pyrogram_audio_obj.performer is None else pyrogram_audio_obj.performer
        self.title = "" if pyrogram_audio_obj.title is None else pyrogram_audio_obj.title

    def to_string(self):
        return_string = "id = {}, duration = {}".format(self.id, self.duration)
        # Optional fields
        return_string = return_string + ", File name = {}".format(self.file_name) \
            if self.file_name != "" else return_string
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string
        return_string = return_string + ", Performer = {}".format(self.performer) \
            if self.performer != "" else return_string
        return_string = return_string + ", Title = {}".format(self.title) \
            if self.title != "" else return_string

        return return_string


class Document:
    def __init__(self, pyrogram_doc_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_doc_obj.file_id
        self.file_name = "" if pyrogram_doc_obj.file_name is None else pyrogram_doc_obj.file_name
        self.mime_type = "" if pyrogram_doc_obj.mime_type is None else pyrogram_doc_obj.mime_type
        self.size = "" if pyrogram_doc_obj.file_size is None else str(pyrogram_doc_obj.file_size)
        self.date = "" if pyrogram_doc_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_doc_obj.date).strftime(_TIME_FORMAT))

    def to_string(self):
        return_string = "id = {}".format(self.id)
        # Optional fields
        return_string = return_string + ", File name = {}".format(self.file_name) \
            if self.file_name != "" else return_string
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string

        return return_string


class Sticker:
    def __init__(self, pyrogram_sticker_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_sticker_obj.file_id
        self.width = pyrogram_sticker_obj.width
        self.height = pyrogram_sticker_obj.height
        self.is_animated = pyrogram_sticker_obj.is_animated
        self.file_name = "" if pyrogram_sticker_obj.file_name is None else pyrogram_sticker_obj.file_name
        self.mime_type = "" if pyrogram_sticker_obj.mime_type is None else pyrogram_sticker_obj.mime_type
        self.size = "" if pyrogram_sticker_obj.file_size is None else str(pyrogram_sticker_obj.file_size)
        self.date = "" if pyrogram_sticker_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_sticker_obj.date).strftime(_TIME_FORMAT))
        self.emoji = "" if pyrogram_sticker_obj.emoji is None else pyrogram_sticker_obj.emoji
        self.set_name = "" if pyrogram_sticker_obj.set_name is None else pyrogram_sticker_obj.set_name

    def to_string(self):
        return_string = "id = {}, width = {}, height = {}, is animated = {}".format(self.id, self.width,
                                                                                    self.height, self.is_animated)
        # Optional fields
        return_string = return_string + ", File name = {}".format(self.file_name) \
            if self.file_name != "" else return_string
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string
        return_string = return_string + ", Correspondent emoji = {}".format(self.emoji) \
            if self.emoji != "" else return_string
        return_string = return_string + ", Sticker set's name = {}".format(self.set_name) \
            if self.set_name != "" else return_string

        return return_string


class Animation:
    def __init__(self, pyrogram_animation_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_animation_obj.file_id
        self.width = pyrogram_animation_obj.width
        self.height = pyrogram_animation_obj.height
        self.duration = pyrogram_animation_obj.duration
        self.file_name = "" if pyrogram_animation_obj.file_name is None else pyrogram_animation_obj.file_name
        self.mime_type = "" if pyrogram_animation_obj.mime_type is None else pyrogram_animation_obj.mime_type
        self.size = "" if pyrogram_animation_obj.file_size is None else str(pyrogram_animation_obj.file_size)
        self.date = "" if pyrogram_animation_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_animation_obj.date).strftime(_TIME_FORMAT))

    def to_string(self):
        return_string = "id = {}, width = {}, height = {}, duration = {}".format(self.id, self.width,
                                                                                 self.height, self.duration)
        # Optional fields
        return_string = return_string + ", File name = {}".format(self.file_name) \
            if self.file_name != "" else return_string
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string

        return return_string


class Game:
    def __init__(self, pyrogram_game_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_game_obj.file_id
        self.title = pyrogram_game_obj.title
        self.short_name = pyrogram_game_obj.short_name
        self.description = pyrogram_game_obj.description
        self.photo = pyrogram_game_obj.photo
        self.animation = "" if pyrogram_game_obj.animation is None else pyrogram_game_obj.animation

    def to_string(self):
        return_string = "id = {}, title = {}, short name = {}, " \
                        "description = {}, photo meta-data = {}".format(self.id, self.title, self.short_name,
                                                                        self.description, Photo(self.photo).to_string())
        # Optional fields
        return_string = return_string + ", Animation = {}".format(Animation(self.animation).to_string()) \
            if self.animation != "" else return_string

        return return_string


class Video:
    def __init__(self, pyrogram_video_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_video_obj.file_id
        self.width = pyrogram_video_obj.width
        self.height = pyrogram_video_obj.height
        self.duration = pyrogram_video_obj.duration
        self.file_name = "" if pyrogram_video_obj.file_name is None else pyrogram_video_obj.file_name
        self.mime_type = "" if pyrogram_video_obj.mime_type is None else pyrogram_video_obj.mime_type
        self.supports_streaming = "" if pyrogram_video_obj.supports_streaming is None \
            else pyrogram_video_obj.supports_streaming
        self.size = "" if pyrogram_video_obj.file_size is None else str(pyrogram_video_obj.file_size)
        self.date = "" if pyrogram_video_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_video_obj.date).strftime(_TIME_FORMAT))
        self.ttl_seconds = "" if pyrogram_video_obj.ttl_seconds is None else pyrogram_video_obj.ttl_seconds

    def to_string(self):
        return_string = "id = {}, width = {}, height = {}, duration = {}".format(self.id, self.width,
                                                                                 self.height, self.duration)
        # Optional fields
        return_string = return_string + ", File name = {}".format(self.file_name) \
            if self.file_name != "" else return_string
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Supports streaming = {}".format(self.supports_streaming) \
            if self.supports_streaming != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string
        return_string = return_string + ", TTL(s)= {}".format(self.ttl_seconds) \
            if self.ttl_seconds != "" else return_string

        return return_string


class Voice:
    def __init__(self, pyrogram_voice_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_voice_obj.file_id
        self.duration = pyrogram_voice_obj.duration
        self.mime_type = "" if pyrogram_voice_obj.mime_type is None else pyrogram_voice_obj.mime_type
        self.size = "" if pyrogram_voice_obj.file_size is None else str(pyrogram_voice_obj.file_size)
        self.date = "" if pyrogram_voice_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_voice_obj.date).strftime(_TIME_FORMAT))

    def to_string(self):
        return_string = "id = {}, duration = {}".format(self.id, self.duration)
        # Optional fields
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string

        return return_string


class Videonote:
    def __init__(self, pyrogram_videonote_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_videonote_obj.file_id
        self.length = pyrogram_videonote_obj.length
        self.duration = pyrogram_videonote_obj.duration
        self.mime_type = "" if pyrogram_videonote_obj.mime_type is None else pyrogram_videonote_obj.mime_type
        self.size = "" if pyrogram_videonote_obj.file_size is None else str(pyrogram_videonote_obj.file_size)
        self.date = "" if pyrogram_videonote_obj.date is None else \
            str(datetime.utcfromtimestamp(pyrogram_videonote_obj.date).strftime(_TIME_FORMAT))

    def to_string(self):
        return_string = "id = {}, length = {}, duration = {}".format(self.id, self.length, self.duration)
        # Optional fields
        return_string = return_string + ", Mime type = {}".format(self.mime_type) \
            if self.mime_type != "" else return_string
        return_string = return_string + ", Size = {}".format(self.size) \
            if self.size != "" else return_string
        return_string = return_string + ", Date = {}".format(self.date) \
            if self.date != "" else return_string

        return return_string


class Contact:
    def __init__(self, pyrogram_contact_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.phone_number = pyrogram_contact_obj.phone_number
        self.first_name = pyrogram_contact_obj.first_name
        self.last_name = "" if pyrogram_contact_obj.last_name is None else pyrogram_contact_obj.last_name
        self.user_id = "" if pyrogram_contact_obj.user_id is None else str(pyrogram_contact_obj.user_id)
        self.vcard = "" if pyrogram_contact_obj.vcard is None else pyrogram_contact_obj.vcard

    def to_string(self):
        return_string = "Phone Number = {}, First name = {}".format(self.phone_number, self.first_name)
        # Optional fields
        return_string = return_string + ", Last name = {}".format(self.last_name) \
            if self.last_name != "" else return_string
        return_string = return_string + ", User Id = {}".format(self.user_id) \
            if self.user_id != "" else return_string
        return_string = return_string + ", Vcard = {}".format(self.vcard) \
            if self.vcard != "" else return_string

        return return_string


class Location:
    def __init__(self, pyrogram_location_obj):

        self.longitude = pyrogram_location_obj.longitude
        self.latitude = pyrogram_location_obj.latitude

    def to_string(self):
        return_string = "Longitude = {}, Latitude = {}".format(self.longitude, self.latitude)
        return return_string


class Venue:
    def __init__(self, pyrogram_venue_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.longitude = pyrogram_venue_obj.longitude
        self.title = pyrogram_venue_obj.title
        self.address = pyrogram_venue_obj.address
        self.foursquare_id = "" if pyrogram_venue_obj.foursquare_id is None else pyrogram_venue_obj.foursquare_id
        self.foursquare_type = "" if pyrogram_venue_obj.foursquare_type is None else pyrogram_venue_obj.foursquare_type

    def to_string(self):
        return_string = "Longitude = {}, Title = {}, Address = {}".format(self.longitude, self.title, self.address,
                                                                          self.is_animated)
        # Optional fields
        return_string = return_string + ", Foursquare id = {}".format(self.foursquare_id) \
            if self.foursquare_id != "" else return_string
        return_string = return_string + ", Foursquare type = {}".format(self.foursquare_type) \
            if self.foursquare_type != "" else return_string

        return return_string


class WebPage:
    def __init__(self, pyrogram_web_page_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_web_page_obj.file_id
        self.url = pyrogram_web_page_obj.url
        self.display_url = pyrogram_web_page_obj.display_url
        self.type = "" if pyrogram_web_page_obj.type is None else pyrogram_web_page_obj.type
        self.site_name = "" if pyrogram_web_page_obj.site_name is None else pyrogram_web_page_obj.site_name
        self.title = "" if pyrogram_web_page_obj.title is None else pyrogram_web_page_obj.title
        self.description = "" if pyrogram_web_page_obj.description is None else pyrogram_web_page_obj.description
        self.audio = "" if pyrogram_web_page_obj.audio is None else pyrogram_web_page_obj.audio
        self.document = "" if pyrogram_web_page_obj.document is None else pyrogram_web_page_obj.document
        self.photo = "" if pyrogram_web_page_obj.photo is None else pyrogram_web_page_obj.photo
        self.animation = "" if pyrogram_web_page_obj.animation is None else pyrogram_web_page_obj.animation
        self.video = "" if pyrogram_web_page_obj.video is None else pyrogram_web_page_obj.video
        self.embed_url = "" if pyrogram_web_page_obj.embed_url is None else pyrogram_web_page_obj.embed_url
        self.embed_type = "" if pyrogram_web_page_obj.embed_type is None else pyrogram_web_page_obj.embed_type
        self.embed_width = "" if pyrogram_web_page_obj.embed_width is None else str(pyrogram_web_page_obj.embed_width)
        self.embed_height = "" if pyrogram_web_page_obj.embed_height is None else str(pyrogram_web_page_obj.embed_height)
        self.duration = "" if pyrogram_web_page_obj.duration is None else str(pyrogram_web_page_obj.duration)
        self.author = "" if pyrogram_web_page_obj.author is None else pyrogram_web_page_obj.author

    def to_string(self):
        return_string = "id = {}, URL = {}, Displayed URL = {}".format(self.id, self.url, self.display_url)
        # Optional fields
        return_string = return_string + ", Type = {}".format(self.type) \
            if self.type != "" else return_string
        return_string = return_string + ", Site name = {}".format(self.site_name) \
            if self.site_name != "" else return_string
        return_string = return_string + ", Title = {}".format(self.title) \
            if self.title != "" else return_string
        return_string = return_string + ", Description = {}".format(self.description) \
            if self.description != "" else return_string
        return_string = return_string + ", Audio meta-data = {}".format(Audio(self.audio).to_string()) \
            if self.audio != "" else return_string
        return_string = return_string + ", Document meta-data = {}".format(Document(self.document).to_string()) \
            if self.document != "" else return_string
        return_string = return_string + ", Photo meta-data = {}".format(Photo(self.photo).to_string()) \
            if self.photo != "" else return_string
        return_string = return_string + ", Animation meta-data = {}".format(Animation(self.animation).to_string()) \
            if self.animation != "" else return_string
        return_string = return_string + ", Video meta-data = {}".format(Video(self.video).to_string()) \
            if self.video != "" else return_string
        return_string = return_string + ", Embedded URL = {}".format(self.embed_url) \
            if self.embed_url != "" else return_string
        return_string = return_string + ", Embedded type = {}".format(self.embed_type) \
            if self.embed_type != "" else return_string
        return_string = return_string + ", Embedded width = {}".format(self.embed_width) \
            if self.embed_width != "" else return_string
        return_string = return_string + ", Embedded height = {}".format(self.embed_height) \
            if self.embed_height != "" else return_string
        return_string = return_string + ", Duration = {}".format(self.duration) \
            if self.duration != "" else return_string
        return_string = return_string + ", Author = {}".format(self.author) \
            if self.author != "" else return_string

        return return_string


class Poll:
    def __init__(self, pyrogram_poll_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.id = pyrogram_poll_obj.file_id
        self.question = pyrogram_poll_obj.question
        self.options = pyrogram_poll_obj.options
        self.total_voter_count = pyrogram_poll_obj.total_voter_count
        self.is_closed = pyrogram_poll_obj.is_closed
        self.type = "" if pyrogram_poll_obj.type is None else pyrogram_poll_obj.type
        self.is_anonymous = "" if pyrogram_poll_obj.is_anonymous is None else str(pyrogram_poll_obj.is_anonymous)
        self.allows_multiple_answers = "" if pyrogram_poll_obj.allows_multiple_answers is None \
            else str(pyrogram_poll_obj.allows_multiple_answers)
        self.chosen_option = "" if pyrogram_poll_obj.chosen_option is None else str(pyrogram_poll_obj.chosen_option)

    def to_string(self):
        return_string = "Id = {}, Question = {}, Options = {}, " \
                        "Num of voters = {}, Is closed = {}".format(self.id, self.question, self.options,
                                                                    self.total_voter_count, self.is_closed)
        # Optional fields
        return_string = return_string + ", Type = {}".format(self.type) \
            if self.type != "" else return_string
        return_string = return_string + ", Is anonymous = {}".format(self.is_anonymous) \
            if self.is_anonymous != "" else return_string
        return_string = return_string + ", Allows multiple answers = {}".format(self.allows_multiple_answers) \
            if self.allows_multiple_answers != "" else return_string
        return_string = return_string + ", Chosen option = {}".format(self.chosen_option) \
            if self.chosen_option != "" else return_string

        return return_string


class Dice:
    def __init__(self, pyrogram_dice_obj):
        _TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

        self.emoji = pyrogram_dice_obj.emoji
        self.value = pyrogram_dice_obj.value

    def to_string(self):
        return_string = "Emoji = {}, Value = {}".format(self.emoji, self.value)

        return return_string


class BColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

