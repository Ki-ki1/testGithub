from django.contrib import admin
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import Conference, Submission, OrganizingCommittee
from django.utils.html import format_html

admin.site.site_header = " Management Dashboard"
admin.site.site_title = "Conference Admin"
admin.site.index_title = "Welcome to the Administration Panel"

def export_to_csv(modeladmin, request, queryset):
    """
    Action générique pour exporter les objets sélectionnés vers un fichier CSV avec chaque attribut dans une colonne séparée.
    """
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name_plural}.csv'
    writer = csv.writer(response)

    # Définir les en-têtes comme des colonnes séparées
    fields = ['name', 'theme', 'location', 'start_date', 'end_date', 'description']
    writer.writerow(fields)

    # Écrire les données avec chaque attribut dans sa propre colonne
    for obj in queryset:
        row = [
            getattr(obj, 'name', ''),
            getattr(obj, 'theme', ''),
            getattr(obj, 'location', ''),
            getattr(obj, 'start_date', ''),
            getattr(obj, 'end_date', ''),
            getattr(obj, 'description', '')
        ]
        writer.writerow(row)

    return response

export_to_csv.short_description = "Exporter la sélection en CSV"

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'location', 'start_date', 'end_date')
    search_fields = ('name', 'theme', 'location')
    list_filter = ('theme', 'location', 'start_date')
    ordering = ('-start_date',)
    list_per_page = 5
    actions = [export_to_csv]

    fieldsets = (
        ("Informations générales", {'fields': ('name', 'theme', 'description')}),
        ("Localisation et Dates", {'fields': ('location', 'start_date', 'end_date')}),
    )

    def colored_theme(self, obj):
        colors = {
            'CS_AI': 'purple',
            'SE': 'blue',
            'SSE': 'green',
            'IT': 'orange',
        }
        color = colors.get(obj.theme, 'black')
        return format_html(f"<b style='color:{color}'>{obj.get_theme_display()}</b>")
    colored_theme.short_description = "Theme"

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'payed', 'submission_date', 'conference', 'user')
    list_filter = ('status', 'payed', 'conference')
    search_fields = ('title', 'keywords')
    ordering = ('-submission_date',)
    list_per_page = 5
    actions = [export_to_csv]

class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'committee_role', 'conference', 'date_joined')
    list_filter = ('committee_role', 'conference')
    search_fields = ('user__username',)
    ordering = ('-date_joined',)
    list_per_page = 5
    actions = [export_to_csv]

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(OrganizingCommittee, OrganizingCommitteeAdmin)