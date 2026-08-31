
class Application:
    def __init__(self, name, api_key, is_active):
        self.name = name
        self.api_key = api_key
        self.is_active = is_active


class NotificationTemplate:
    def __init__(self, code, subject, template_path, sender_name, sender_email, reply_to, is_active):
        self.code = code
        self.subject = subject
        self.template_path = template_path
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.reply_to = reply_to
        self.is_active = is_active


class Notification:
    def __init__(self, recipient, channel, payload, status, retry_count, max_retries, error_message):
        self.recipient = recipient
        self.channel = channel
        self.payload = payload
        self.status = status
        self.retry_count = retry_count
        self.max_retries = max_retries
        self.error_message = error_message              