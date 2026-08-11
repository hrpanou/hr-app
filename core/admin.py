from django.contrib import admin
from .models import ProfileAngajat, CerereConcediu, Pontaj, DocumentAngajat
from .models import SetariAplicatie

admin.site.register(SetariAplicatie)
admin.site.register(ProfileAngajat)
admin.site.register(CerereConcediu)
admin.site.register(Pontaj)
admin.site.register(DocumentAngajat)
admin.site.has_permission = lambda request: request.user.is_active and request.user.is_superuser