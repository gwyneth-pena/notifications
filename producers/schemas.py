from shared.trimmed_base_model import TrimmedBaseModel
from typing import Literal


class NotificationSchema(TrimmedBaseModel):
    """ Notification Schema """
    template_code: str
    recipient: str
    payload: dict
    type: Literal['email', 'push'] = "email"
