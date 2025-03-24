from enum import Enum


class MessageType(Enum):
    PRIVATE = 0
    PUBLIC = 1
    LIST_ATTENDEES = 2
    WELCOME = 3
    BYE = 4
    DISCONNECTED = 5
    UNKNOWN = 6
    PUBLIC_FILE = 7
    PRIVATE_FILE = 8
