import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from configs.celery import app

from core.dataclasses.user_dataclass import UserDataClass
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def test_email(cls):
        cls.__send_email('ytoxos@gmail.com', 'test_email.html', {}, 'Hello')

    @classmethod
    def register_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(user.email, 'register.html', {
            'name': user.profile.name,
            'url': url
        }, 'Register')

    @classmethod
    def recovery_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email(user.email, 'recovery_password.html', {
            'name': user.profile.name,
            'url': url
        }, 'Recovery Password')

    @staticmethod
    @app.task
    def spam():
        for user in UserModel.objects.all():
            EmailService.__send_email(user.email, 'spam.html', {}, 'SPAM')

