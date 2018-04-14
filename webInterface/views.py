from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Share
from .form import ContactForm

import vobject

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
            # TODO: if contact is updated tell subscribers
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
def download_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    #TODO: Prove you have access to the contact
    #TODO: Public access to public contacts

    vcard_string = generate_vcard(contact)
    filename = contact.firstName + contact.lastName + ".vcf"
    response = HttpResponse(vcard_string, content_type="text/x-vCard")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required
def approve_share(request, pk):
    share = get_object_or_404(Share, pk=pk)

    if share.sharing != request.user:
        raise PermissionDenied("You do not have permission")

    share.accepted = True
    share.save()
    return redirect('profile')


@login_required
def remove_share(request, pk):
    share = get_object_or_404(Share, pk=pk, accepted=True)

    if share.sharing != request.user:
        raise PermissionDenied("You do not have permission")

    share.delete()
    return redirect('profile')


@login_required
def sharing(request):
    shares = Share.objects.filter(sharing=request.user)
    return render(request, 'sharing.html', {'shares': shares})


def generate_vcard(contact):
    v = vobject.vCard()
    v.add('n')
    v.n.value = vobject.vcard.Name(family=contact.lastName, given=contact.firstName)
    v.add('fn')
    v.fn.value = "%s %s" % (contact.firstName, contact.lastName)
    if contact.email is not None:
        v.add('email')
        v.email.value = contact.email
    if contact.phone is not None:
        v.add('tel')
        v.tel.value = str(contact.phone)
    if contact.company is not None:
        v.add('org')
        v.org.value = [contact.company]
    output = v.serialize()
    return output
