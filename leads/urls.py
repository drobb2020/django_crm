from django.urls import path
from .views import lead_list, lead_detail, lead_create

app_name = 'leads'

urlpatterns = [
  path('', lead_list),
  path('create/', lead_create),
  path('<int:pk>/', lead_detail)
]