from django.urls import path
from mp2_api import views


urlpatterns = [
    path('hello-view/', views.HelloAPIView.as_view()),
]
