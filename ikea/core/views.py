from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get (self, request):
        return render(request, 'core/index.html')
    
class IndexNoches(View):
    def get (self, request):
        return render(request, 'core/index_noches.html')

