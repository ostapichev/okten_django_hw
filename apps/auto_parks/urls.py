from django.urls import path

from apps.auto_parks.views import AutoParkCarListCreateView, AutoParkListCreateView, AutoParkRetrieveUpdateDestroyView

urlpatterns = [
    path('', AutoParkListCreateView.as_view()),
    path('/<int:pk>', AutoParkRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/cars', AutoParkCarListCreateView.as_view()),
]