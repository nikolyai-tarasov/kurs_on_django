from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import HomeView, CreateRecipientView, DetailRecipientView, UpdateRecipientView, DeleteRecipientView, \
    CreateMessageView, DetailMessageView, UpdateMessageView, DeleteMessageView, CreateNewsletterView, \
    DetailNewsletterView, UpdateNewsletterView, DeleteNewsletterView, RecipientListView, MessageListView, \
    NewsletterListView, SendNewsletterView,  StatisticsMailAttemptView

app_name = MailingsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name="home"),

    path('recipient_list/', RecipientListView.as_view(), name='recipient_list'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('newsletter_list/', NewsletterListView.as_view(), name='newsletter_list'),

    path('create_recipient/', CreateRecipientView.as_view(), name='create_recipient'),
    path('detail_recipient/<int:pk>/', DetailRecipientView.as_view(), name='detail_recipient'),
    path('update_recipient/<int:pk>/', UpdateRecipientView.as_view(), name='update_recipient'),
    path('delete_recipient/<int:pk>/', DeleteRecipientView.as_view(), name='delete_recipient'),

    path('create_message/', CreateMessageView.as_view(), name='create_message'),
    path('detail_message/<int:pk>/', DetailMessageView.as_view(), name='detail_message'),
    path('update_message/<int:pk>/', UpdateMessageView.as_view(), name='update_message'),
    path('delete_message/<int:pk>/', DeleteMessageView.as_view(), name='delete_message'),

    path('create_newsletter/', CreateNewsletterView.as_view(), name='create_newsletter'),
    path('detail_newsletter/<int:pk>/', DetailNewsletterView.as_view(), name='detail_newsletter'),
    path('update_newsletter/<int:pk>/', UpdateNewsletterView.as_view(), name='update_newsletter'),
    path('delete_newsletter/<int:pk>/', DeleteNewsletterView.as_view(), name='delete_newsletter'),
    path('newsletter_send/<int:pk>/', SendNewsletterView.as_view(), name='send_newsletter'),
    path('statistics_mail_attempt/', StatisticsMailAttemptView.as_view(), name='statistics_mail_attempt'),


]
