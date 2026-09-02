
class ApplicationModel:
    def __init__(self, id, name, api_key, is_active):
        self.id = id
        self.name = name
        self.api_key = api_key
        self.is_active = is_active


class NotificationTemplateModel:
    def __init__(self,id, application_id, code, subject, template_path, sender_name, sender_email, reply_to, is_active):
        self.id = id
        self.application_id = application_id
        self.code = code
        self.subject = subject
        self.template_path = template_path
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.reply_to = reply_to
        self.is_active = is_active


class NotificationModel:
    def __init__(self,id, application_id, template_id, recipient, channel, payload, status, retry_count, max_retries, error_message):
        self.id = id
        self.application_id = application_id
        self.template_id = template_id
        self.recipient = recipient
        self.channel = channel
        self.payload = payload
        self.status = status
        self.retry_count = retry_count
        self.max_retries = max_retries
        self.error_message = error_message              