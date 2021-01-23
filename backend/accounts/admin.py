from django.contrib import admin
from .models import *
class AccountAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user_id")
    list_per_page = 25
admin.site.register(Account, AccountAdmin)

class PermissionsAdmin(admin.ModelAdmin):
    # def Account_Codes(self, inst):
    #     return ','.join([username for b in inst.Account_set.all()])
    # list_display = (Account_Codes, "rrm")
    list_display = ("rrm",)
admin.site.register(Permissions, PermissionsAdmin)


# class WhitelistAdmin(admin.ModelAdmin):
#     list_display = ("email", "full_name", "organization")
# admin.site.register(Whitelist, WhitelistAdmin)

class Notification_Admin(admin.ModelAdmin):
    list_display = ("message", "seen", "date_created", "app",)
admin.site.register(Notification, Notification_Admin)


class Species_Expert_Admin(admin.ModelAdmin):
    list_display = ("account", "species", "badge_pending")
admin.site.register(Species_Expert, Species_Expert_Admin)

class Feedback_Admin(admin.ModelAdmin):
    list_display = ("resolved", "fb_text", "name")
admin.site.register(Feedback, Feedback_Admin)

class CuratorAdmin(admin.ModelAdmin):
    list_display = ("account", "notes")
admin.site.register(Curator, CuratorAdmin)
