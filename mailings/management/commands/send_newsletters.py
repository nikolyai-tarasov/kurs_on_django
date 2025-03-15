from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from mailings.models import Newsletter, MailingAttempt
import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        pk = kwargs['pk']
        newsletter = get_object_or_404(Newsletter, id=pk)
        recipients = newsletter.recipients.all()

        statistics = {
            'successful_attempts': 0,
            'failed_attempts': 0,
            'attempts': []
        }

        for recipient in recipients:
            attempt = MailingAttempt(date_of_attempt=timezone.now(), newsletter=newsletter)

            try:
                subject = newsletter.message.subject
                message = newsletter.message.letter
                from_email = os.getenv('EMAIL_HOST_USER')
                send_mail(subject, message, from_email, [recipient.email])
                attempt.status = 'успешно'
                statistics['successful_attempts'] += 1

            except Exception as e:
                attempt.status = 'не успешно'
                attempt.mail_reply = str(e)
                statistics['failed_attempts'] += 1

            attempt.save()

            statistics['attempts'].append({
                'recipient': recipient.email,
                'status': attempt.status,
                'reply': attempt.mail_reply,
            })

        self.stdout.write(self.style.SUCCESS(
            f'Рассылка завершена. Успешные попытки: {statistics["successful_attempts"]}, Неуспешные попытки: {statistics["failed_attempts"]}'))
