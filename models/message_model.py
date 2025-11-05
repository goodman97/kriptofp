class Message:
    def __init__(self, sender, receiver, content, msg_type="text"):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.msg_type = msg_type
