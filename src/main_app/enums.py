from django.db import models


class GenderEnum(models.IntegerChoices):
    MALE = 1, 'Муж'
    FEMALE = 2, "Жен"


class VaccinationStatusEnum(models.IntegerChoices):
    DONE = 1, 'Выполнено'
    PLAN = 2, "Запланировано"