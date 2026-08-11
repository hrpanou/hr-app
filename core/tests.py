from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date

from .models import ProfileAngajat, Pontaj


class PontajCalculeTestCase(TestCase):
    """Teste pentru calculele numerice de pe Pontaj (km, bani, consum)."""

    def setUp(self):
        self.user = User.objects.create_user(username='sofer_test', password='parola123')

    def test_total_km_calcul_corect(self):
        pontaj = Pontaj.objects.create(
            angajat=self.user, data=date(2026, 8, 1),
            km_plecare=1000, km_sosire=1100,
        )
        self.assertEqual(pontaj.total_km, 100)

    def test_total_km_negativ_devine_zero(self):
        # km_sosire mai mic decat km_plecare (date gresite) -> nu trebuie sa dea numar negativ
        pontaj = Pontaj.objects.create(
            angajat=self.user, data=date(2026, 8, 1),
            km_plecare=1000, km_sosire=900,
        )
        self.assertEqual(pontaj.total_km, 0)

    def test_de_incasat_calcul_corect(self):
        pontaj = Pontaj.objects.create(
            angajat=self.user, data=date(2026, 8, 1),
            km_plecare=0, km_sosire=100,
        )
        # tarif fix 0.7 RON/km, definit in model
        self.assertEqual(pontaj.de_incasat, 70)

    def test_consum_100km_calcul_corect(self):
        pontaj = Pontaj.objects.create(
            angajat=self.user, data=date(2026, 8, 1),
            km_plecare=0, km_sosire=100, litri_motorina=10,
        )
        self.assertEqual(pontaj.consum_100km, 10.0)

    def test_consum_100km_fara_km_nu_da_eroare(self):
        # daca total_km e 0, nu trebuie sa impartim la zero
        pontaj = Pontaj.objects.create(
            angajat=self.user, data=date(2026, 8, 1),
            km_plecare=100, km_sosire=100, litri_motorina=10,
        )
        self.assertEqual(pontaj.consum_100km, 0)


class PontajViewsTestCase(TestCase):
    """Teste pentru comportamentul view-urilor de pontaj (blocaje, validari)."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sofer_test', password='parola123')
        ProfileAngajat.objects.create(user=self.user, functia='Șofer', departament='Transport')
        self.client.login(username='sofer_test', password='parola123')

    def test_nu_poate_schimba_masina_in_aceeasi_zi(self):
        # Primul pontaj, cu masina A
        self.client.post(reverse('pontaj_intrare'), {
            'numar_inmatriculare': 'B111AAA', 'km_plecare': '1000',
        })
        # Al doilea pontaj, aceeasi zi, cu masina B -> trebuie blocat
        self.client.post(reverse('pontaj_intrare'), {
            'numar_inmatriculare': 'B222BBB', 'km_plecare': '2000',
        })
        pontaj = Pontaj.objects.get(angajat=self.user)
        # Numarul de inmatriculare NU trebuie sa se fi schimbat
        self.assertEqual(pontaj.numar_inmatriculare, 'B111AAA')
        self.assertEqual(pontaj.km_plecare, 1000)

    def test_litri_nerealisti_sunt_respinsi(self):
        Pontaj.objects.create(
            angajat=self.user, data=date.today(),
            km_plecare=1000, numar_inmatriculare='B111AAA',
        )
        self.client.post(reverse('pontaj_iesire'), {
            'km_sosire': '1100', 'litri_motorina': '5000', 'tip_traseu': 'urban',
        })
        pontaj = Pontaj.objects.get(angajat=self.user)
        # litri nu trebuie sa se fi salvat, ramane 0 (valoarea implicita)
        self.assertEqual(pontaj.litri_motorina, 0)


class AccesInactivTestCase(TestCase):
    """Testeaza ca un angajat marcat inactiv nu mai poate accesa dashboard-ul."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='fost_angajat', password='parola123')
        ProfileAngajat.objects.create(
            user=self.user, functia='Șofer', departament='Transport', activ=False,
        )
        self.client.login(username='fost_angajat', password='parola123')

    def test_angajat_inactiv_este_redirectionat(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('login'))


class AccesAdminTestCase(TestCase):
    """Testeaza ca un cont HR (fara is_superuser) nu poate accesa /admin/."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='hr_test', password='parola123', is_staff=True)
        ProfileAngajat.objects.create(user=self.user, functia='HR', departament='HR', rol='hr')
        self.client.login(username='hr_test', password='parola123')

    def test_hr_nu_are_acces_la_admin(self):
        response = self.client.get('/admin/')
        # Django Admin refuza accesul (fie 302 redirect la login, fie 403)
        self.assertIn(response.status_code, [302, 403])