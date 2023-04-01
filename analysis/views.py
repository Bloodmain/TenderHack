from django.shortcuts import render, redirect
from .forms import CompanyForm
from .models import Companies


def homepage(request):
    form = CompanyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            inn = form.cleaned_data["inn"]
            if Companies.objects.filter(pk=inn).count():
                return redirect(f'stats/{inn}')
            else:
                form.add_error("inn", "Non-existent inn")
    return render(request, 'homepage.html', {
        'form': form
    })


def stats(request, inn):
    return render(request, 'stats.html')
