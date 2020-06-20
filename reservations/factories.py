import factory
from factory.fuzzy import FuzzyDecimal, FuzzyInteger

from reservations.models import Table, Reservation, Client


class TableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Table

    max_capacity = FuzzyInteger(2, 12)
    shape = factory.Iterator(['rectangular', 'oval'])
    coordinates = FuzzyDecimal(0, 100)
    size = FuzzyDecimal(0, 100)


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    name = factory.Faker('first_name')
    email = factory.Faker('email')


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation
