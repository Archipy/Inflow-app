from django.urls import path
from .views import SubirExcel,MenuView,DatosView,Mv1View,Mv0View,AltaRotacion,RefPorCamion,RefPorCamionMv1

app_name = 'noche'

urlpatterns = [
    path('upload_files/', SubirExcel.as_view() , name='upload_files'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('datos/', DatosView.as_view(), name='datos'),
    path('camiones_mv1/', Mv1View.as_view(), name='camiones_mv1'),
    path('camiones_mv0/', Mv0View.as_view(), name='camiones_mv0'),
    path('alta_rotacion/', AltaRotacion.as_view(), name='alta_rotacion'),
    path('referencia_por_camion_mv0/', RefPorCamion.as_view() , name='referencia_por_camion'),
    path('referencia_por_camion_mv1/', RefPorCamionMv1.as_view() , name='referencia_por_camion_mv1')
]
