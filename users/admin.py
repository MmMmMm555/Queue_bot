from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from dtb.settings import DEBUG

from users.models import Location
from users.models import User
from users.forms import BroadcastForm

from users.tasks import broadcast_message
from tgbot.handlers.broadcast_message.utils import send_one_message

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_help_text = "Search users by username or user ID."
    list_display = [
        'user_id', 'username', 'first_name', 'last_name', 'phone_number', 'order',
    ]


admin.site.register(User, UserAdmin)


# actions = ['broadcast']

# def broadcast(self, request, queryset):
#     """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
#     user_ids = queryset.values_list('user_id', flat=True).distinct().iterator()
#     if 'apply' in request.POST:
#         broadcast_message_text = request.POST["broadcast_text"]

#         if DEBUG:  # for test / debug purposes - run in same thread
#             for user_id in user_ids:
#                 send_one_message(
#                     user_id=user_id,
#                     text=broadcast_message_text,
#                 )
#             self.message_user(request, f"Just broadcasted to {len(queryset)} users")
#         else:
#             broadcast_message.delay(text=broadcast_message_text, user_ids=list(user_ids))
#             self.message_user(request, f"Broadcasting of {len(queryset)} messages has been started")

#         return HttpResponseRedirect(request.get_full_path())
#     else:
#         form = BroadcastForm(initial={'_selected_action': user_ids})
#         return render(
#             request, "admin/broadcast_message.html", {'form': form, 'title': u'Broadcast message'}
#         )
