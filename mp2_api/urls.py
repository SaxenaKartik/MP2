from django.urls import path,include
from mp2_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name = 'hello-viewset')
router.register('drone', views.DroneViewSet)
router.register('client', views.ClientViewSet)

urlpatterns = [
    path('hello-view/', views.HelloAPIView.as_view()),
    path('', include(router.urls))
]
