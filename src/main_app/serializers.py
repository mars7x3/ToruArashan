from rest_framework import serializers

from main_app.models import *


class MeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'username')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class ParentSerializer(serializers.ModelSerializer):
    category_info = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Animal
        fields = ('id', 'name', 'unicode', 'image', 'category_info', 'gender')


class AnimalListSerializer(serializers.ModelSerializer):
    category_info = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Animal
        fields = ('id', 'name', 'unicode', 'category_info', 'birthday', 'image')


class MeasurementFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementFile
        fields = ('id', 'file')


class MeasurementSerializer(serializers.ModelSerializer):
    files = MeasurementFileSerializer(many=True, read_only=True)

    class Meta:
        model = Measurement
        fields = ('id', 'date', 'weight', 'height', 'head_length', 'body_length', 'ear_length', 'files')


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ('id', 'date', 'preparation', 'text', 'status')


class AnimalCRUDSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_info = CategorySerializer(source='category', read_only=True)
    mother_info = ParentSerializer(source='mother', read_only=True)
    father_info = ParentSerializer(source='father', read_only=True)
    popular_line_info = ParentSerializer(source='popular_line', read_only=True)
    measurements = MeasurementSerializer(many=True, read_only=True)
    vaccinations = VaccinationSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields = (
            'id', 'name', 'unicode', 'image', 'author',
            'category', 'gender', 'birthday',
            'mother', 'father', 'popular_line',
            'category_info', 'mother_info', 'father_info', 'popular_line_info',
            'measurements', 'vaccinations',
        )


class MeasurementCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'animal', 'date', 'weight', 'height', 'head_length', 'body_length', 'ear_length')


class VaccinationCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ('id', 'animal', 'date', 'preparation', 'text', 'status')


class AnimalShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('id', 'name', 'unicode', 'gender')


class TimelineMeasurementSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)

    class Meta:
        model = Measurement
        fields = ('id', 'animal', 'date', 'weight', 'height', 'head_length', 'body_length', 'ear_length')


class TimelineVaccinationSerializer(serializers.ModelSerializer):
    animal = AnimalShortSerializer(read_only=True)

    class Meta:
        model = Vaccination
        fields = ('id', 'animal', 'date', 'preparation', 'text', 'status')