from django.utils import timezone

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24

def formatDate(date):
    now = timezone.now()
    dif = (now - date).total_seconds()
    if dif < HOUR:
        return "Just now"
    elif dif < DAY:
        return date.strftime("%I:%M%p")
    elif dif < DAY * 7:
        if dif < DAY * 2:
            return "Yesteday"
        else:
            return str(dif.total_seconds() / DAY)+" days ago"
    else:
        return date.strftime("%d/%m/%Y")
