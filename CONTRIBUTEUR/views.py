from django.shortcuts import render, redirect
from CROWDFUNDING.models import *
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
#from CROWDFUNDING.token import generatorToken
from django.template.loader import render_to_string
from PROJET_CORRIGER import settings
from django.contrib.auth.decorators import login_required

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
import uuid

# Create your views here.

def index(request):
    listpro=Projets.objects.all()
    types=Types_Projets.objects.all()
    donation_amount = 50.00  # Exemple de montant de don
   
    context={
        'listpro':listpro,
        'types':types,
       
    }
    return render(request, 'indexs.html', context)

@login_required
def envoyer(request):
    ut=request.user
    if request.method == "POST":
        mess=request.POST.get('mess')
        #Email de création des projets
        current_site=get_current_site(request)
        email_subject="DEMANDE DE CHANGEMENT DE STATUT"
        messageConfirm= render_to_string("demande.html", {
        "message":mess,
        "domain":current_site.domain,
        'id':ut.id,
            
        })
        li=["dieumercibaderha1@gmail.com"]
        email=EmailMessage(
                email_subject,
                messageConfirm,
                settings.EMAIL_HOST_USER,
                li
            )
        email.fail_silently=False
        email.send()
    return redirect('indexs')

@login_required
def contribuer(request):
    ut=request.user
    if request.method == "POST":
        projet=request.POST.get('projet')
        pp=Projets.objects.get(Titre=projet)
        types=request.POST.get('type')
        montant=request.POST.get('montant')
        inte=float(pp.Interet/100)*float(montant)
       
        montac=int(montant)
        if pp.Reste > 0 and montac <= pp.Reste:
            if types=="DON":
                con=Contributions.objects.create(Utilisateurs=ut.username,
                                                Projets=pp,
                                                Type_Contributions=types, Montant=float(montant),
            
                                                interet=0, Remboursement=0)
                con.save()
                pp.Contribution = float(pp.Contribution) + float(montac)
                pp.Reste = float(pp.Reste) - float(montac)
                host=request.get_host()
                paypal_dict = {
                    "business": pp.compte,
                    "amount": montant,
                    "item_name": f"Contribution pour le projet {projet}",
                    "invoice": str(uuid.uuid4()),
                    "currency_code": "USD",
                    "notify_url": 'https://{}{}'.format(host, reverse('paypal-ipn')),
                    "return_url":'https://{}{}'.format(host, reverse('payment_success')),
                    "cancel_return":'https://{}{}'.format(host, reverse('payment_cancel')),
                }
                paypal_form=PayPalPaymentsForm(initial=paypal_dict)
                context={
                    'projet':projet,
                    'type':types,
                    'montant':montant,
                    'paypal_form':paypal_form,
                    'id':pp.id
                }
                pp.save()
                return render(request, "confirmation1.html", context)
                
            elif types=="PRET":
                
                con=Contributions.objects.create(Utilisateurs=ut.username,
                                                Projets=pp,
                                                Type_Contributions=types, Montant=float(montant),
            
                                                interet=inte, Remboursement=montac + inte)
                con.save()
                pp.Contribution = float(pp.Contribution) + float(montac)
                pp.Reste = float(pp.Reste) - float(montac)
                host=request.get_host()
                paypal_dict = {
                    "business": settings.PAYPAL_RECEIVER_EMAIL,
                    "amount": montant,
                    "item_name": f"Contribution pour le projet {projet}",
                    "invoice": str(uuid.uuid4()),
                    "currency_code": "USD",
                    "notify_url": 'https://{}{}'.format(host, reverse('paypal-ipn')),
                    "return_url":'https://{}{}'.format(host, reverse('payment_success')),
                    "cancel_return":'https://{}{}'.format(host, reverse('payment_cancel')),
                }
                paypal_form=PayPalPaymentsForm(initial=paypal_dict)
                context={
                    'projet':projet,
                    'type':types,
                    'montant':montant,
                    'paypal_form':paypal_form,
                    'id':pp.id
                }
                
                
                
                pp.save()
                return render(request, "confirmation1.html", context)
 
    return redirect('indexs')



@login_required
def details(request, id):
    prdet=Projets.objects.get(id=id)
    
    context={
        'proid':prdet,
       
    }
    return render(request, 'details.html', context)

@login_required
def changement(request, id):
    usq=User.objects.get(id=id)
    usq.statut="APPORTEUR"
    usq.is_contri=False
    usq.save()
    return redirect('indexs')


def payment_success(request):
    return render(request, "payment_success.html")

def payment_cancel(request):
    return render(request, "payment_cancel.html")
