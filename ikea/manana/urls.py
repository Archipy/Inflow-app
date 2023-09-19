from django.urls import path
from .views import AddOuts, DeleteOutView, update_out_status, delete_all_data   

app_name = 'manana'

urlpatterns = [
    path('outs/', AddOuts.as_view() , name='outs'),
    path('delete/<int:pk>/', DeleteOutView.as_view(), name='delete_out'),
    path('update_out_status/', update_out_status, name='update_out_status'),
    path('delete-all-data/', delete_all_data, name='delete_all_data'),
]
