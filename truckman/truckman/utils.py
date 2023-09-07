from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 

#utilies functions


#get request user company
def get_user_company(request):
    if request.user.is_authenticated:
        try:
            company = request.user.company
        except:
            company = None
        return company

#send email 
def send_email(context, template_path, from_name, from_email, subject, recipient_email, replyto_email):
    from_name_email = f'{from_name} <{from_email}>'
    template = render_to_string(template_path, context)
    e_mail = EmailMessage(
        subject,
        template,
        from_name_email, #'John Doe <john.doe@example.com>'
        [recipient_email],
        reply_to=[replyto_email,from_email],
    )
    e_mail.send(fail_silently=False)
#--end
    
        