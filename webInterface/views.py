from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .form import ContactForm


def landing_page(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    contacts = request.user.contact_set.all()
    return render(request, 'profile.html', {'contacts': contacts})


@login_required
def new_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('profile')
    else:
        form = ContactForm()
    return render(request, 'new_contact.html', {'form': form})


@login_required
def contact_details(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if contact.user != request.user:
        raise PermissionDenied("You do not have permission to see this contact")

    return render(request, 'contact_details.html', {'contact': contact})


@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if contact.user != request.user:
        raise PermissionDenied("You do not have permission to see this contact")

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()

            return redirect('profile')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'edit_contact.html', {'form': form})
