from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Table, Reservation, Client
from reservations.serializers import TableSerializer, ReservationFormSerializer, ReservationSerializer


class TableView(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ReservationView(APIView):

    def get(self, request):
        reservations = Reservation.objects.all()
        date = request.query_params.get('date', None)
        if date:
            try:
                year, month, day = date.split('-')
            except ValueError:
                return Response({"error": "Wrong date format, need to be like YYYY-MM-DD"},
                                status=status.HTTP_400_BAD_REQUEST)

            reservations = reservations.filter(date__year=year, date__month=month, date__day=day)
        return Response(ReservationSerializer(reservations, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):

        request = ReservationFormSerializer(data=request.data)
        request.is_valid(raise_exception=True)
        client = Client.objects.create(**request.validated_data.pop('client'))
        reservation = Reservation.objects.create(client=client, date=request.validated_data['date'])
        for table in request.validated_data['tables']:
            reservation.tables.add(table)

        tables = [str(table.id) for table in reservation.tables.all()]

        send_mail(
            'Reservation at Restaurant',
            f'You have successfully reserved table(s) '
            f'# {", ".join(tables)} on {reservation.date}',
            'reservations@Restaurant.com',
            [client.email],
            fail_silently=False,
        )

        return Response({"id": reservation.id}, status=status.HTTP_201_CREATED)


