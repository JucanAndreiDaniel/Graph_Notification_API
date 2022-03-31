from login_api.settings import EMAIL_NOTI_HTML, EMAIL_NOTI_PLAIN
import django
import os
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_api.settings')


django.setup()

try:
    #from django_email_verification import send_email
    #from django.contrib.auth.models import User
    from caca.models import Profile as ProfileModels
    from caca.models import Notification as NotificationModels
    from django.contrib.auth.models import User, auth
    from django.template.loader import render_to_string
    from django.core.mail import send_mail

    users = ProfileModels.objects.all()

    for user in users:
        #a = ProfileModels.objects.get(user__id = user.user_id)
        notifications = user.notification.all()
        for noti in notifications:
            if noti.enabled == True:
                if noti.via_mail == True:
                    user_email = User.objects.get(id = user.user_id)
                    cName = noti.coin.name
                    cVal = noti.final_value
                    msg_plain = render_to_string(EMAIL_NOTI_PLAIN, {'user': user_email.username, 'cName':cName,'cVal':cVal, 'link':'http://stockcrypto.ddns.net/'})
                    msg_html = render_to_string(EMAIL_NOTI_HTML, {'user': user_email.username, 'cName':cName,'cVal':cVal, 'link':'http://stockcrypto.ddns.net/'})
                    send_mail(
                        'NotifyMe Price Alert!',
                        msg_plain,
                        os.environ.get('EMAIL_HOST_USER'),
                        [user_email.email],
                        html_message=msg_html,
                        fail_silently=False,
                    )
                    noti.enabled = False
                    noti.save()

except:
    traceback.print_exc()



