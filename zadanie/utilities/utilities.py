from django.utils import timezone


def hundred_years_from_now():
    now = timezone.now()
    hundred_years = timezone.timedelta(days=100*365)
    hundred_years_from_now =  now + hundred_years
    return hundred_years_from_now

def yesterday():
    now = timezone.now()
    one_day = timezone.timedelta(days = 1)
    yesterday =  now - one_day
    return yesterday
