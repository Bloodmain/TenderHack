from django.shortcuts import render, redirect
from .forms import CompanyForm


def homepage(request):
    form = CompanyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            return redirect('/stats')

    context = {
        'form': form
    }
    return render(request, 'homepage.html', context)


def stats(request, inn):
    pass
