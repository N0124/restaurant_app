from rest_framework import serializers

from reservations.models import Table, Client, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'max_capacity', 'shape', 'coordinates', 'size']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'email']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'tables', 'date']


class ReservationFormSerializer(serializers.Serializer):
    client = ClientSerializer()
    tables = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), many=True)
    date = serializers.DateField()

