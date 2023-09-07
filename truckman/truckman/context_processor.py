from trip.models import  Notification

#-- custome context processor notifications --
def get_user_notifications(request):
    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        notifications = Notification.objects.filter(recipient=user, is_read=False).order_by('-timestamp')[:3]
        return {"notifications" :notifications}
    return {}
