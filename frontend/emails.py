from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def email_message_send(subject, message,receiver):
    email = EmailMessage(
        subject,
        message,
        'Global Machinary <contact@globalmachinary.com>',
        [receiver],
        )
    email.content_subtype = "html"
    email.fail_silently = False
    email.send()
    return message


def final_message(name, email, subject, message):
    final_message = render_to_string('emails/email_contact.html', 
            {
                'name': name,
                'email': email,
                'message': message,
                'subject': subject
            })
    return email


def final_message2(name, order_id, date, country, city, total):
    final_message = render_to_string('emails/email_order.html', 
            {
                'name': name,
                'order_id': order_id,
                'date': date,
                'country': country,
                'city': city,
                'total': total
            })
    return name


                        