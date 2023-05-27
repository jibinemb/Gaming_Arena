from django.contrib import admin

# Register your models here.
from .models import *

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'location', 'phone_number', 'address', 'email')
    search_fields = ('name', 'email')
    list_filter = ('location', 'age')
    list_per_page = 20

from django.contrib import admin
from django.utils.html import format_html
from .models import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon', 'description', 'timestamp')
    readonly_fields = ('display_icon',)

    def display_icon(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return "(No image)"

    display_icon.short_description = 'Icon'

admin.site.register(Game, GameAdmin)

from django.contrib import admin
from .models import arena

class ArenaAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(arena, ArenaAdmin)
from django.contrib import admin
from .models import Slot

class SlotAdmin(admin.ModelAdmin):
    list_display = ('arena', 'start_time', 'end_time', 'price')
    list_filter = ('arena', 'start_time')
    search_fields = ('arena__title', 'start_time')

admin.site.register(Slot, SlotAdmin)


from django.contrib import admin
from .models import Booking

from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_name', 'game')
    list_filter = ('user', 'game', 'event')
    search_fields = ('user__username', 'game__name', 'event__name')

    def get_user_name(self, obj):
        return obj.user.name

    get_user_name.short_description = 'User Name'

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'cname', 'amount', 'cardno')
    list_filter = ('bookid__user', 'amount')
    search_fields = ('bookid__user__username', 'cname', 'cardno')

    def get_bookid_user(self, obj):
        return obj.bookid.user.username

    get_bookid_user.short_description = 'User'

admin.site.register(Result)

class SelectAdmin(admin.ModelAdmin):
    list_display = ('event', 'winner')

admin.site.register(Winner, SelectAdmin)
admin.site.register(Event)