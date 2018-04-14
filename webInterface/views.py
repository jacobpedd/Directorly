from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Share
from .form import ContactForm


def landing_page(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    contacts = request.user.contact_set.all()
    shares = Share.objects.filter(sharing=request.user, accepted=False)
    shared = Share.objects.filter(sharedWith=request.user, accepted=True)
    shared_contacts = set()
    for share in shared:
        shared_contacts.add(share.contact)
    return render(request, 'profile.html', {'contacts': contacts,
                                            'shares': shares,
                                            'shared_contacts': shared_contacts})


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
        return redirect('contact_public', pk=pk)

    return render(request, 'contact_details.html', {'contact': contact})


@login_required
def contact_public(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    shared_set = contact.share_set.all()
    if not contact.public and request.user not in shared_set:
        return render(request, 'contact_request_access.html', {'contact': contact})
    else:
        return render(request, 'contact_public.html', {'contact': contact})




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


@login_required
def contact_request(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    share = Share()
    share.contact = contact
    share.sharedWith = request.user
    share.sharing = contact.user
    share.save()
    return render(request, 'request_confirmed.html')


@login_required
def approve_share(request, pk):
    share = get_object_or_404(Share, pk=pk)

    if share.sharing != request.user:
        raise PermissionDenied("You do not have permission to see this contact")

    share.accepted = True
    share.save()
    return redirect('profile')
