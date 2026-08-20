from typing import Literal
from shared.trimmed_base_model import TrimmedBaseModel


class NotificationSchema(TrimmedBaseModel):
    """ Notification Schema """
    tenant_id: str
    recipient: str
    message: str
    type: Literal['email', 'push'] = "email"
