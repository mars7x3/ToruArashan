from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main_app.models import Animal, Measurement, Vaccination, MeasurementFile
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
            .prefetch_related('measurements__files', 'vaccinations')
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

    @extend_schema(
        parameters=[
            OpenApiParameter(name='date_from', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='date_to', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
        ]
    )
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


class CreateFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        files = request.FILES.getlist('files')
        measurement = request.data.get('measurement')
        if not Measurement.objects.get(id=measurement).animal.author == request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = [MeasurementFile(measurement_id=measurement, file=file) for file in files]
        MeasurementFile.objects.bulk_create(data)
        return Response("Success!", status=status.HTTP_201_CREATED)


class DeviceTokenCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        device_token = request.data.get('device_token')
        if not device_token:
            return Response(
                {'error': 'device_token is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.device_token = device_token
        request.user.save()
        return Response("Device token updated successfully", status=status.HTTP_200_OK)