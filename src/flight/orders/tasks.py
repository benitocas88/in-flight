from typing import Dict

from flight.orders.schemas import NotifyPaymentStatus
from flight.utils.http import webhook_dispatcher
from flight.utils.tasks import celery_task_with_retry
from flight.utils.validator import schema_validator


@celery_task_with_retry("orders.notify_payment_status")
@schema_validator(NotifyPaymentStatus)
def notify_payment_paid(**kwargs: Dict):
    return webhook_dispatcher(**kwargs)
