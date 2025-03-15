import os
from django.core.mail import send_mail
from django.db import models
from users.models import User


class Recipient(models.Model):
    email = models.CharField(max_length=50, unique=True, help_text='Введите почту получателя рассылки')
    full_name = models.CharField(max_length=100, verbose_name='ФИО', help_text='Введите полное имя получателя')
    comment = models.TextField('Введите комментарий о получателе')
    avatar = models.ImageField(upload_to='users/photo', blank=True, null=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='owner_recipient',blank=True, null=True )

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email', ]


    def __str__(self):
        return f'{self.full_name} -{self.email}'


class Message(models.Model):
    subject = models.CharField(max_length=100, help_text='Тема сообщения')
    letter = models.TextField('Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_message', blank=True, null=True)

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['subject', ]

    def __str__(self):
        return f'{self.subject}'


class Newsletter(models.Model):
    STATUS_CHOICES = [
        ('завершена', 'Завершена'),
        ('создана', 'Создана'),
        ('запущена', 'Запущена'),
    ]

    first_shipment = models.DateTimeField(help_text='Дата и время первой отправки рассылки')
    last_dispatch = models.DateTimeField(help_text='Дата и время окончания отправки рассылки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='создана')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_newsletters', blank=True, null=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['message', 'status', ]
        permissions = [
            ('can_unpublish', 'Can unpublish '),
        ]

    def send_email_to_recipients(self):
        subject = f"{self.message.subject}"
        message = self.message.letter
        from_email = os.getenv('EMAIL_HOST_USER')

        recipient_list = [recipient.email for recipient in self.recipients.all()]

        send_mail(subject, message, from_email, recipient_list)

    def __str__(self):
        return f"Рассылка: {self.status} - {self.message}"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('успешно', 'Успешно'),
        ('не успешно', 'Не успешно'),
    ]

    date_of_attempt = models.DateTimeField(help_text='Дата и время  попытки  рассылки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='успешно')
    mail_reply = models.TextField('Ответ почтового сервера ')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
