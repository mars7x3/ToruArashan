from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main_app.models import Animal, Measurement, Vaccination
from main_app.permissions import IsOwner
from main_app.serializers import MeInfoSerializer, AnimalCRUDSerializer, AnimalListSerializer, \
    VaccinationCRUDSerializer, MeasurementCRUDSerializer, \
    TimelineMeasurementSerializer, TimelineVaccinationSerializer


class MeInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        response = MeInfoSerializer(user).data
        return Response(response)


class AnimalModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AnimalCRUDSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimalListSerializer
        return AnimalCRUDSerializer

    def get_queryset(self):
        qs = Animal.objects.filter(author=self.request.user)
        if self.action == 'list':
            return qs.select_related('category')
        return (
            qs
            .select_related(
                'category',
                'mother__category',
                'father__category',
                'popular_line__category',
            )
            .prefetch_related('measurements', 'vaccinations')
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MeasurementModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = MeasurementCRUDSerializer
    http_method_names = ['post', 'patch', 'delete']

    def get_queryset(self):
        return Measurement.objects.filter(animal__author=self.request.user)


class VaccinationModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = VaccinationCRUDSerializer
    http_method_names = ['post', 'patch', 'delete']

    def get_queryset(self):
        return Vaccination.objects.filter(animal__author=self.request.user)


class AnimalTimelineView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if not date_from or not date_to:
            return Response(
                {'error': 'date_from and date_to are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        measurements = (
            Measurement.objects
            .filter(animal__author=request.user, date__gte=date_from, date__lte=date_to)
            .select_related('animal')
        )
        vaccinations = (
            Vaccination.objects
            .filter(animal__author=request.user, date__gte=date_from, date__lte=date_to)
            .select_related('animal')
        )

        return Response({
            'measurements': TimelineMeasurementSerializer(measurements, many=True).data,
            'vaccinations': TimelineVaccinationSerializer(vaccinations, many=True).data,
        })