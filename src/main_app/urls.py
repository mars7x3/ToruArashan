from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.contrib import admin

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from conf import settings
from main_app.views import MeInfoView, AnimalModelViewSet, MeasurementModelViewSet, VaccinationModelViewSet, \
    AnimalTimelineView, CreateFileView, DeviceTokenCreateView

router = DefaultRouter()

router.register('animal', AnimalModelViewSet, basename='animal')
router.register('measurement', MeasurementModelViewSet, basename='measurement')
router.register('vaccination', VaccinationModelViewSet, basename='vaccination')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',
         include([
             path('schema/', SpectacularAPIView.as_view(), name='schema'),
             path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
             path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

             path('token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
             path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

             path('me/info/', MeInfoView.as_view()),
             path('timeline/', AnimalTimelineView.as_view()),
             path('measurement/file/create', CreateFileView.as_view()),
             path('device-token/create', DeviceTokenCreateView.as_view()),


            path('', include(router.urls)),
        ])
    )

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
