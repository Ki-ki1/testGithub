from django.contrib import admin
from .models import User
from django.utils.html import format_html
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.db.models import Count

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'colored_name', 'email', 'role', 'affiliation', 'nationality')
    list_filter = ('role', 'nationality')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('role',)
    actions = ['export_pdf', 'show_statistics']

    # Couleur personnalisée du nom
    def colored_name(self, obj):
        color = "green" if obj.role == "participant" else "orange"
        return format_html(f"<b style='color:{color}'>{obj.first_name} {obj.last_name}</b>")
    colored_name.short_description = "Full Name"

    # Exportation PDF avec design amélioré
    def export_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'title',
            parent=styles['Title'],
            fontSize=20,
            alignment=1,
            textColor=colors.darkblue,
            spaceAfter=20
        )
        header_style = ParagraphStyle(
            'header',
            parent=styles['Heading4'],
            alignment=1,
            textColor=colors.whitesmoke
        )

        # Titre
        elements.append(Paragraph("Liste des utilisateurs", title_style))
        elements.append(Spacer(1, 12))

        # Table des utilisateurs
        data = [["ID", "Nom Complet", "Email", "Rôle", "Affiliation", "Nationalité"]]
        for user in queryset:
            full_name = f"{user.first_name} {user.last_name}"
            data.append([user.user_id, full_name, user.email, user.role, user.affiliation, user.nationality])

        table = Table(data, colWidths=[50, 120, 150, 80, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        return response

    export_pdf.short_description = "Exporter les utilisateurs en PDF"

    # Action pour afficher des statistiques simples avec design HTML
    def show_statistics(self, request, queryset):
        total = queryset.count()
        roles = queryset.values('role').order_by('role').annotate(count=Count('role'))
        nationalities = queryset.values('nationality').order_by('nationality').annotate(count=Count('nationality'))

        # HTML avec style amélioré
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; }}
                .container {{ max-width: 800px; margin: 20px auto; padding: 20px; border-radius: 8px; background-color: #ffffff; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
                h2 {{ color: #4CAF50; }}
                .stats {{ margin: 20px 0; }}
                .stat {{ padding: 10px; margin: 10px 0; border-radius: 5px; background-color: #e7f3fe; border-left: 6px solid #2196F3; }}
                .total {{ font-weight: bold; font-size: 1.2em; }}
                .role, .nationality {{ font-size: 1em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Statistiques des utilisateurs sélectionnés</h2>
                <div class="stats">
                    <div class="stat total">Total utilisateurs : {total}</div>
                    <h3>Par rôle</h3>
                    <div class="stats">
        """
        for r in roles:
            html += f"<div class='stat role'>{r['role']} : {r['count']}</div>"

        html += """
                    </div>
                    <h3>Par nationalité</h3>
                    <div class="stats">
        """
        for n in nationalities:
            html += f"<div class='stat nationality'>{n['nationality']} : {n['count']}</div>"

        html += """
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return HttpResponse(html)

admin.site.register(User, UserAdmin)