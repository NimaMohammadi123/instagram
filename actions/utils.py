from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone


def create_action(user,act,target=None):
    now = timezone.now()
    last_action = now - datetime.timedelta(seconds=60)
    simillar_actions = Action.objects.filter(user=user , act=act ,created__gte=last_action)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        simillar_actions = simillar_actions.filter(target_ct=target_ct , target_id = target.id)
    if not simillar_actions:
        action = Action(user=user , act=act , target=target)
        action.save()
        return True

    return False