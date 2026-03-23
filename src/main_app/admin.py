from django.contrib import admin

from main_app.models import *

admin.site.register(MyUser)
admin.site.register(Category)
admin.site.register(Animal)
admin.site.register(Measurement)
admin.site.register(Vaccination)
