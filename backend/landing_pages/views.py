from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from landing_pages.forms import ContateNosForm

# Create your views here.


def sobre_nos(request):
    return render(request, "pages/sobre_nos.html")


class ContateNosView(View):
    template_name = "pages/contate_nos.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': ContateNosForm()})

    def post(self, request, *args, **kwargs):
        form = ContateNosForm(request.POST)
        if form.is_valid():
            form.send_email_admins()
            messages.success(request, "Suas ideias foram enviadas")
            return redirect(reverse("landing_pages:contate_nos"))
        return render(request, self.template_name, {'form': form})
