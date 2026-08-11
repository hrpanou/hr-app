from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    dashboard, pontaj_intrare, pontaj_iesire,
    hr_dashboard, hr_angajati, hr_pontaje, hr_concedii, hr_concediu_actiune,
    cerere_concediu_creare, editare_profil, hr_angajat_detaliu, hr_angajat_toggle_activ,
    hr_calendar_concedii, hr_export_lunar, hr_export_excel,
    hr_angajat_creare, schimbare_parola,
)

urlpatterns = [
    path('hr/angajati/<int:user_id>/', hr_angajat_detaliu, name='hr_angajat_detaliu'),
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('pontaj/intrare/', pontaj_intrare, name='pontaj_intrare'),
    path('pontaj/iesire/', pontaj_iesire, name='pontaj_iesire'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login')),
    path('hr/', hr_dashboard, name='hr_dashboard'),
    path('hr/angajati/', hr_angajati, name='hr_angajati'),
    path('hr/pontaje/', hr_pontaje, name='hr_pontaje'),
    path('hr/concedii/', hr_concedii, name='hr_concedii'),
    path('hr/concedii/<int:cerere_id>/<str:actiune>/', hr_concediu_actiune, name='hr_concediu_actiune'),
    path('concediu/creare/', cerere_concediu_creare, name='cerere_concediu_creare'),
    path('profil/editare/', editare_profil, name='editare_profil'),
    path('hr/angajati/<int:user_id>/toggle-activ/', hr_angajat_toggle_activ, name='hr_angajat_toggle_activ'),
    path('hr/calendar/', hr_calendar_concedii, name='hr_calendar_concedii'),
    path('hr/export/', hr_export_lunar, name='hr_export_lunar'),
    path('hr/export/excel/', hr_export_excel, name='hr_export_excel'),
    path('hr/angajati/creare/', hr_angajat_creare, name='hr_angajat_creare'),
    path('profil/schimbare-parola/', schimbare_parola, name='schimbare_parola'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)