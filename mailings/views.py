import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailings.forms import RecipientForm, MessageForm, NewsletterForm, NewsletterModeratorForm
from mailings.models import Recipient, Message, Newsletter, MailingAttempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache




class HomeView(ListView):
    model = Recipient
    template_name = 'home.html'
    context_object_name = 'recipients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_mailings = Newsletter.objects.count()
        active_mailings = Newsletter.objects.filter(status='запущена').count()
        unique_recipients = MailingAttempt.objects.values('mail_reply').distinct().count()

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_recipients'] = unique_recipients
        return context
    def get_queryset(self):
        queryset = cache.get('recipients_queryset')
        if  not queryset:
            queryset = super().get_queryset()
            cache.set('recipients_queryset',queryset, 60 * 15)
        return queryset


# Списки «Получателей рассылки»,«Сообщений»,«Рассылок»
@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'

@method_decorator(cache_page(60 * 15), name='dispatch')
class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter_list.html'
    context_object_name = 'newsletters'


# контроллеры для «Получателей рассылки»
class CreateRecipientView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'create_recipient.html'
    success_url = reverse_lazy('mailings:home')

@method_decorator(cache_page(60 * 15), name='dispatch')
class DetailRecipientView(DetailView):
    model = Recipient
    template_name = 'detail_recipient.html'


class UpdateRecipientView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'update_recipient.html'
    success_url = reverse_lazy('mailings:recipient_list')




class DeleteRecipientView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'delete_recipient.html'
    success_url = reverse_lazy('mailings:home')


# контроллеры для «Сообщений»
class CreateMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'create_message.html'
    success_url = reverse_lazy('mailings:home')

@method_decorator(cache_page(60 * 15), name='dispatch')
class DetailMessageView(DetailView):
    model = Message
    template_name = 'detail_message.html'


class UpdateMessageView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'update_message.html'
    success_url = reverse_lazy('mailings:home')


class DeleteMessageView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'delete_message.html'
    success_url = reverse_lazy('mailings:home')


# контроллеры для «Рассылок»
class CreateNewsletterView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'create_newsletter.html'
    success_url = reverse_lazy('mailings:home')

@method_decorator(cache_page(60 * 15), name='dispatch')
class DetailNewsletterView(DetailView):
    model = Newsletter
    template_name = 'detail_newsletter.html'
    success_url = reverse_lazy('mailings:home')


class UpdateNewsletterView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'update_newsletter.html'
    success_url = reverse_lazy('mailings:home')

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('mailings.can_unpublish'):
            return NewsletterModeratorForm
        raise PermissionDenied


class DeleteNewsletterView(LoginRequiredMixin, DeleteView):
    model = NewsletterForm
    template_name = 'delete_newsletter.html'
    success_url = reverse_lazy('mailings:home')


class SendNewsletterView(View):
    def post(self, request, pk):
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

        return redirect('mailings:home')

@method_decorator(cache_page(60 * 15), name='dispatch')
class StatisticsMailAttemptView(View):
    def get(self, request):
        attempts = MailingAttempt.objects.all()
        return render(request, 'statistics_mail_attempt.html', {'attempts': attempts})
