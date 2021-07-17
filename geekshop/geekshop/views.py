from django.shortcuts import render
from mainapp.models import Product


def main(request):
    title = 'главная'

    context = {
        'title': title,
        'products': Product.objects.filter(category__is_active=True, is_active=True)[:3],
    }
    return render(request, 'index.html', context)


def contact(request):
    title = 'контакты'
    context = {
        'title': title,
        'contact_number': range(3)
    }

    return render(request, 'contact.html', context)
