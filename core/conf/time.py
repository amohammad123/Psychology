from django.utils import timezone


def time_now():
    return int(timezone.now().timestamp())
