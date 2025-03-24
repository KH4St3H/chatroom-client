from utils import extract_length, extract_type_from_message, extract_receivers, extract_sender, extract_filename
from customtypes import MessageType


class Message:
    def __init__(self, message_type: MessageType, message: str, sender="", receivers=None) -> None:
        self.type = message_type
        self.message = message
        self.receivers: list = receivers or []
        self.sender = sender
        self.metadata = {}
        print(repr(self))

    def __repr__(self) -> str:
        return f'type={self.type},message={self.message}'

    @classmethod
    def from_data(cls, data: bytes):
        message = data[data.find(b'\n\r')+2:]
        header = data[:data.find(b'\n')].decode()
        type_ = extract_type_from_message(header)
        length = extract_length(header)
        receivers = extract_receivers(header)
        sender = extract_sender(header)

        if len(message) == 0:
            return cls(type_, header, sender, receivers)

        if type_ in {MessageType.PUBLIC_FILE, MessageType.PRIVATE_FILE}:
            filename = extract_filename(header)
            if not filename:
                return None
            with open(filename, 'wb') as f:
                f.write(message)

            obj = cls(type_, str("sent a file"), sender, None)
            obj.metadata['filename'] = filename
            return obj

        message = message.decode()

        if type_ in {MessageType.PUBLIC, MessageType.PRIVATE}:
            message = message[:length][1:]

        return cls(type_, str(message), sender, receivers)

    def __str__(self):
        match self.type:
            case MessageType.PRIVATE:
                return f'{self.sender} (to {', '.join(self.receivers)}): {self.message}'
            case MessageType.PUBLIC:
                return f'{self.sender}: {self.message}'
            case MessageType.WELCOME:
                return "Welcome to the chat room"
            case MessageType.LIST_ATTENDEES:
                return f'List of members present in chat: {self.message}'
            case MessageType.PRIVATE_FILE | MessageType.PUBLIC_FILE:
                return f'{self.sender}: sent a file: "{self.metadata["filename"]}"'
            case _:
                return self.message
