from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic import ListView, DeleteView
from django.forms import formset_factory
from .forms import OutsForm
from .models import Outs
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.http import JsonResponse

class AddOuts(FormView, ListView):
    template_name = 'manana/outs.html'
    queryset = Outs.objects.all()
    context_object_name = 'outs_data'
    form_class = OutsForm
    success_url = '.'

    def form_valid(self, form):
            code = form.cleaned_data.get('code')
            ubicacion = form.cleaned_data.get('ubicacion')

            if code and not code.isdigit():
                messages.error(self.request, 'El código debe contener solo números.')
                return self.form_invalid(form)

            if ubicacion and not ubicacion.isdigit():
                messages.error(self.request, 'La ubicación debe contener solo números.')
                return self.form_invalid(form)          
            form.save()
            return super().form_valid(form)
    
    def form_invalid(self, form):
        
        return redirect(self.success_url)

    
class DeleteOutView(DeleteView):
    model = Outs
    template_name = 'manana/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('manana:outs')

    def post(self, request, *args, **kwargs):
        try:
            outs = get_object_or_404(Outs, pk=self.kwargs['pk'])
            success_url = self.get_success_url()
            outs.delete()
            return redirect(success_url)
        except Http404:
            messages.error(request, 'El out ya ha sido borrado.')
            return redirect(self.get_success_url())
        
       
def update_out_status(request):
    if request.method == 'POST':
        out_id = request.POST.get('out_id')
        checked = request.POST.get('checked')

        # Obtén la instancia de Outs correspondiente
        outs_instance = Outs.objects.get(id=out_id)
        outs_instance.down = checked == 'True'  # Actualiza el campo "down"

        # Guarda los cambios en la base de datos
        outs_instance.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
def delete_all_data(request):
    if request.method == 'POST':
        Outs.objects.all().delete()
        messages.success(request, '¡Se han borrado todos los outs!')
    return redirect('manana:outs')