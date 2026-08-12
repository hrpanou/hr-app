from django.db import models
from django.contrib.auth.models import User


class ProfileAngajat(models.Model):
    ROL_CHOICES = [
        ('angajat', 'Angajat'),
        ('hr', 'HR / Manager'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    functia = models.CharField(max_length=100, verbose_name="Funcție")
    departament = models.CharField(max_length=100, verbose_name="Departament")
    telefon = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    data_angajare = models.DateField(null=True, blank=True, verbose_name="Data Angajării")
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='angajat', verbose_name="Rol")
    CONTRACT_CHOICES = [
        ('determinat', 'Determinat'),
        ('nedeterminat', 'Nedeterminat'),
    ]
    cnp = models.CharField(max_length=13, blank=True, default='', verbose_name="CNP")
    adresa = models.CharField(max_length=255, blank=True, default='', verbose_name="Adresă")
    tip_contract = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='nedeterminat', verbose_name="Tip Contract")
    salariu_baza = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Salariu de Bază")
    activ = models.BooleanField(default=True, verbose_name="Activ")
    data_incetare = models.DateField(null=True, blank=True, verbose_name="Data Încetării Contractului")
    zile_concediu_alocate = models.PositiveIntegerField(default=20, verbose_name="Zile Concediu Alocate/An")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.functia}"


class CerereConcediu(models.Model):
    TIP_CHOICES = [
        ('odihna', 'Concediu de Odihnă'),
        ('medical', 'Concediu Medical'),
        ('fara_plata', 'Concediu Fără Plată'),
    ]
    STATUS_CHOICES = [
        ('in_asteptare', 'În Așteptare'),
        ('aprobat', 'Aprobat'),
        ('respins', 'Respins'),
    ]
    angajat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cereri_concediu')
    tip_concediu = models.CharField(max_length=20, choices=TIP_CHOICES, default='odihna')
    data_inceput = models.DateField()
    data_sfarsit = models.DateField()
    motiv = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_asteptare')
    data_creare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.angajat.username} - {self.get_tip_concediu_display()}"


class Pontaj(models.Model):
    angajat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pontaje')
    data = models.DateField()
    ora_intrare = models.TimeField(null=True, blank=True)
    ora_iesire = models.TimeField(null=True, blank=True)

    @property
    def ore_lucrate(self):
        if self.ora_intrare and self.ora_iesire:
            from datetime import datetime, timedelta
            intrare = datetime.combine(self.data, self.ora_intrare)
            iesire = datetime.combine(self.data, self.ora_iesire)
            if iesire < intrare:
                iesire += timedelta(days=1)
            diferenta = iesire - intrare
            return round(diferenta.total_seconds() / 3600, 2)
        return 0

    def __str__(self):
        return f"Pontaj {self.angajat.username} - {self.data}"

    @property
    def total_km(self):
        if self.km_sosire > self.km_plecare:
            return self.km_sosire - self.km_plecare
        return 0

    @property
    def de_incasat(self):
        tarif_per_km = 0.7  # Poți modifica valoarea tarifului per kilometru aici
        return self.total_km * tarif_per_km

    @property
    def consum_100km(self):
        if self.total_km > 0 and self.litri_motorina:
            return round((float(self.litri_motorina) / self.total_km) * 100, 2)
        return 0

    def __str__(self):
        return f"Pontaj {self.angajat.username} - {self.data}"


class DocumentAngajat(models.Model):
    angajat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documente')
    titlu = models.CharField(max_length=200)
    fisier = models.FileField(upload_to='documente_angajati/')
    data_incarcare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titlu} ({self.angajat.username})"


class SetariAplicatie(models.Model):
    format_24h = models.BooleanField(default=True, verbose_name="Folosește formatul de 24 de ore")
    nume_companie = models.CharField(max_length=100, default="Panou HR", verbose_name="Nume Companie")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Setări Generale Aplicație"