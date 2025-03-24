import re
from customtypes import MessageType


def extract_length(message: str):
    reg = re.compile(r"length=(\d+)")
    try:
        return int(reg.findall(message)[0])
    except Exception:
        return 0


def extract_type_from_message(message: str) -> MessageType:
    if message.startswith('Public file'):
        return MessageType.PUBLIC_FILE
    if message.startswith('Private file'):
        return MessageType.PRIVATE_FILE
    if message.startswith('Public'):
        return MessageType.PUBLIC
    elif message.startswith('Private'):
        return MessageType.PRIVATE
    elif message.startswith('Here are the list of attendees'):
        return MessageType.LIST_ATTENDEES
    elif message.endswith("left the chat room."):
        return MessageType.BYE
    elif message.endswith("disconnected from the server."):
        return MessageType.DISCONNECTED
    else:
        return MessageType.UNKNOWN


def extract_receivers(message: str) -> list:
    reg = re.compile(r"to ([\w,]+)")
    matches = reg.findall(message)
    if len(matches) == 0:
        return []
    return matches[0].split(',')


def extract_sender(message: str) -> str:
    reg = re.compile(r"from (\w+)")
    matches = reg.findall(message)
    if len(matches) == 0:
        return ''

    return matches[0]


def extract_filename(header):
    reg = re.compile(r"filename=([^,\s]+)")
    matches = reg.findall(header)
    if len(matches) == 0:
        return ''

    return matches[0]
