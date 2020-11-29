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
        return_string = return_string.append(", TTL(s) = {}".format(self.ttl_seconds)) if self.ttl_seconds != "" \
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
        return_string = return_string.append(", File name = {}".format(self.file_name)) \
            if self.file_name != "" else return_string
        return_string = return_string.append(", Mime type = {}".format(self.mime_type)) \
            if self.mime_type != "" else return_string
        return_string = return_string.append(", Size = {}".format(self.size)) \
            if self.size != "" else return_string
        return_string = return_string.append(", Date = {}".format(self.date)) \
            if self.date != "" else return_string
        return_string = return_string.append(", Performer = {}".format(self.performer)) \
            if self.performer != "" else return_string
        return_string = return_string.append(", Title = {}".format(self.title)) \
            if self.title != "" else return_string

        return return_string
