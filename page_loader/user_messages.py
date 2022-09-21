from enum import Enum


class Message(Enum):
    CONNECTION_ERROR = "Please, check Internet connection"
    HTTP_ERROR = "You`ve got some problem with HTTP"
    PERMISSION_DENIED = "You can not use this directory"
    UNEXPECTED = "We don`t know, what is wrong"
    TIMEOUT = "We are waiting too long"
