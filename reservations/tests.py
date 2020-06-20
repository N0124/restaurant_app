import datetime

from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

from reservations.factories import TableFactory, ClientFactory, ReservationFactory
from reservations.models import Reservation


class TablesTests(APITestCase):

    def test_get_tables(self):
        TableFactory.create_batch(12)
        response = self.client.get('/api/tables/')
        self.assertEqual(len(response.data), 12)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReservationsTests(APITestCase):

    def test_create_reservation(self):
        table = TableFactory()
        data = {"client": {"name": "John", "email": "test@test.com"}, 'tables': [table.id], "date": "2020-09-21"}
        response = self.client.post('/api/reservations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservation = Reservation.objects.get(id=response.data['id'])
        self.assertEqual(len(reservation.tables.all()), 1)
        self.assertEqual(reservation.date, datetime.datetime.strptime('2020-09-21', '%Y-%m-%d').date())
        self.assertEqual(reservation.client.name, "John")
        self.assertEqual(reservation.client.email, "test@test.com")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reservation at Restaurant')
        self.assertEqual(mail.outbox[0].from_email, 'reservations@Restaurant.com')
        self.assertEqual(mail.outbox[0].to, ["test@test.com"])
        self.assertEqual(mail.outbox[0].body,
                         f'You have successfully reserved table(s) '
                         f'# 1 on {reservation.date}')

    def test_create_reservations_for_several_tables(self):
        tables = TableFactory.create_batch(2)
        data = {"client": {"name": "John", "email": "test@test.com"}, 'tables': [table.id for table in tables],
                "date": "2020-09-21"}
        response = self.client.post('/api/reservations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservation = Reservation.objects.get(id=response.data['id'])
        self.assertEqual(len(reservation.tables.all()), 2)
        self.assertEqual(reservation.date, datetime.datetime.strptime('2020-09-21', '%Y-%m-%d').date())
        self.assertEqual(reservation.client.name, "John")
        self.assertEqual(reservation.client.email, "test@test.com")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reservation at Restaurant')
        self.assertEqual(mail.outbox[0].from_email, 'reservations@Restaurant.com')
        self.assertEqual(mail.outbox[0].to, ["test@test.com"])
        self.assertEqual(mail.outbox[0].body,
                         f'You have successfully reserved table(s) '
                         f'# 1, 2 on {reservation.date}')

    def test_reservations_on_date(self):
        tables = TableFactory.create_batch(2)
        client = ClientFactory()
        reservation = ReservationFactory(client=client, date="2020-09-21")
        for table in tables:
            reservation.tables.add(table)
        response = self.client.get('/api/reservations/?date=2020-09-21')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tables'], [1, 2])

    def test_reservations_wrong_date_format(self):
        response = self.client.get('/api/reservations/?date=2020/09/21')
        self.assertEqual(response.status_code, 400)
