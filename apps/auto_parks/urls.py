from django.urls import path

from apps.auto_parks.views import AutoParkListCreateView, AutoParkCarListCreateView

urlpatterns = [
    path('', AutoParkListCreateView.as_view()),
    path('/<int:pk>/cars', AutoParkCarListCreateView.as_view()),
]