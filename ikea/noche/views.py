from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views import View
from .forms import ArchivosForm,AltaRotacionCheckForm
import os
from django.contrib import messages
from .datos_utils import obtener_datos,file_upload
from .repo_auto_camion import repo_auto,camiones_auto
from .repeticiones_utils import repeticiones
from .check_picking_utils import sgf_pickingmv1,sgf_pickingmv0
from .repo_market_camion_utils import repo_market,camiones_market
from .alta_rotacion_utils import read_excel
from .models import AltaRotacionCheck


class SubirExcel(FormView):
    template_name = 'noche/upload_files.html'
    form_class = ArchivosForm
    success_url = reverse_lazy("noche:upload_files")
    
    def form_valid(self, form):
        file1_data = form.cleaned_data['file1']
        file2_data = form.cleaned_data['file2']
        file3_data = form.cleaned_data['file3']

        if (file1_data and not file2_data) or (file2_data and not file1_data):
            # Si uno de los archivos 1 o 2 está presente pero el otro no, muestra un mensaje de error
            form.add_error(None, "Debes seleccionar ambos 'Propuesta final' y 'Plan de descarga")
            return self.form_invalid(form)

        if file1_data:
            self.guardar_archivo(file1_data, "PROPUESTA_FINAL")
       
        if file2_data:
            self.guardar_archivo(file2_data, "PLAN")

        if file3_data:
            self.guardar_archivo(file3_data, "SG010")

        # Agregar el mensaje de éxito
        messages.success(self.request, "Archivos subidos con éxito")

        return super().form_valid(form)

    def guardar_archivo(self, archivo, nombre_archivo):
        upload_dir = './noche/static/noche/archivos/'
        file_path = os.path.join(upload_dir, nombre_archivo + ".xlsx")
        
        with open(file_path, 'wb') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)

class MenuView(View):
    def get (self, request):
        return render(request, 'noche/menu.html')
    
class DatosView(View):
    template_name = 'noche/datos.html'
    missing_files = 'noche/missing_files.html'

    def get_context_data(self):
        context = {}
        try:
            datos = obtener_datos()
        except Exception as e:
            # Maneja la excepción aquí, por ejemplo, puedes mostrar un mensaje de error personalizado
            error_message = "Ocurrió un error al obtener los datos: " + str(e)
            context = {
                'error_message': error_message
            }
            return context
        
        suma_repo = datos[1]['repo_mv0'] + datos[1]['repo_mv1'] + datos[1]['repo_mv2']
        suma_tie0 = datos[2]['tie00d'] + datos[2]['tie01d'] + datos[2]['tie02d']
        suma_aire = datos[0]['aire0'] + datos[0]['aire1'] + datos[0]['aire2']
        lineas_ar1 = suma_repo + suma_aire
        context = {
            'datos': datos,
            'suma_repo': suma_repo,
            'suma_tie0': suma_tie0,
            'suma_aire': suma_aire,
            'lineas_ar1': lineas_ar1
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not file_upload():
            return render(request, self.missing_files)
        if 'error_message' in context:
            return render(request, 'noche/wrong_file.html', context)
        
        context = self.get_context_data()
        return render(request, self.template_name, context)
    

class Mv1View(View):
    template_name = 'noche/camiones_mv1.html'

    def get(self, request, *args, **kwargs):
        repo_camion_mv1 = repo_auto()
        camion = camiones_auto()
        pallet_repetidos = repeticiones()
        sgf_gmv1 = sgf_pickingmv1()
        context = {
            'repo_camion_mv1': repo_camion_mv1,
            'camion': camion,
            'pallet_repetidos': pallet_repetidos,
            'sgf_mv1': sgf_gmv1,
        }
        return render(request, self.template_name, context)
    
class Mv0View(View):
    template_name = 'noche/camiones_mv0.html'

    def get (self, request, *args, **kwargs):
        repo_camion_mv0 = repo_market()
        camion = camiones_market()
        sgf_gmv0 = sgf_pickingmv0()
        context = {
            'repo_camion_mv0':  repo_camion_mv0,
            'camion': camion,
            'sgf_mv0': sgf_gmv0,
        }
        return render(request, self.template_name, context)
    

class AltaRotacion(View):
    template_name = 'noche/alta_rotacion.html'

    def get(self, request, *args, **kwargs):
        # Obtener los objetos existentes de la base de datos
        alta_rotacion_checks = AltaRotacionCheck.objects.all()

        alta_rotacion = read_excel()[0]

        # Combina los datos de alta_rotacion y alta_rotacion_checks alternativamente
        combined_data = []
        for row, check in zip(alta_rotacion.iterrows(), alta_rotacion_checks):
            combined_data.append({
                'row': row,
                'lv_checked': check.lv_checked,  # Nombre del campo de checkbox 1
                'bajado_checked': check.bajado_checked,  # Nombre del campo de checkbox 2
            })

        context = {
            'combined_data': combined_data,
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        existing_checks = AltaRotacionCheck.objects.all()

        for check in existing_checks:
            # Obtener el valor del checkbox correspondiente
            lv_checked = request.POST.get(f'lv_checked_{check.id}') == 'on'
            bajado_checked = request.POST.get(f'bajado_checked_{check.id}') == 'on'
            
            # Actualizar los campos del objeto con los valores de los checkboxes
            check.lv_checked = lv_checked
            check.bajado_checked = bajado_checked
            check.save()

        return redirect('noche:alta_rotacion')
    
class RefPorCamion(View):
    template_name = 'noche/referencia_por_camion_mv0.html'

    def get (self, request, *args, **kwargs):
        articulos = camiones_market()
        context = {
         'articulos':articulos
        }
        return render(request, self.template_name, context)
    
class RefPorCamionMv1(View):
    template_name = 'noche/referencia_por_camion_mv1.html'

    def get (self, request, *args, **kwargs):
        articulos = camiones_auto()
        context = {
         'articulos':articulos
        }
        return render(request, self.template_name, context)