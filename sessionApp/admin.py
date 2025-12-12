from django.contrib import admin
from .models import Session
from django.utils.html import format_html
from django.contrib import messages

class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'session_day', 'start_time', 'end_time', 'room', 'conference', 'validity_status')
    list_filter = ('conference', 'room', 'session_day')
    search_fields = ('title', 'topic', 'conference__name')
    ordering = ('session_day',)
    actions = ['check_validity']

    def validity_status(self, obj):
        valid = obj.conference.start_date <= obj.session_day <= obj.conference.end_date
        color = "green" if valid else "red"
        text = "✔️ Valide" if valid else "❌ Hors conférence"
        return format_html(f"<b style='color:{color}'>{text}</b>")
    validity_status.short_description = "Validité"

    def check_validity(self, request, queryset):
        invalid_sessions = [s for s in queryset if s.session_day < s.conference.start_date or s.session_day > s.conference.end_date]
        if invalid_sessions:
            messages.warning(request, f"{len(invalid_sessions)} sessions sont hors de la période de leur conférence.")
        else:
            messages.success(request, "Toutes les sessions sont valides.")
    check_validity.short_description = "Vérifier la validité des sessions"

admin.site.register(Session, SessionAdmin)
