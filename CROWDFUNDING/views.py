from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from PROJET_CORRIGER import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import *
from .models import *
from django.contrib.auth import get_user_model
from datetime import datetime, date
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
import uuid

User = get_user_model()

from paypal.standard.forms import PayPalPaymentsForm










auj=datetime.now()
auj1=date.today()

# Create your views here.
@login_required
def index(request):
    ut=request.user
    context={
        'en':ut,
        'mes_projets':Projets.objects.filter(Utilisateur=ut.username).count(),
        'mes_contrib':Contributions.objects.filter(Utilisateurs=ut.username).count(),
        'pro_en':Projets.objects.all().count(),
        'user_en':User.objects.all().count(),
        'contrib_en':Contributions.objects.filter(Utilisateurs=ut.username),
        'projets_en':Projets.objects.filter(Utilisateur=ut.username),
        'use':User.objects.all().count(),
        'projets_f':Projets.objects.filter(Utilisateur=ut.username, Reste=0).count(),
        
        }
        
    
    return render(request, 'index.html', context )

@login_required
def list_type(request):
    ut=request.user
    listtype=Types_Projets.objects.all().order_by("id")
    if request.method == "GET":
        rech=request.GET.get('recherche')
        if rech is not None:
            listtype=Types_Projets.objects.filter(type__icontains=rech)
    
    context={
        'listtype':listtype,
        'en':ut
    }
    return render(request, 'listtype.html', context)

@login_required
def voir_type(request):
    return render(request, 'voirtype.html')

@login_required
def add_type(request):
    ut=request.user
    if request.method == "POST":
        types=request.POST.get("types")
        desc=request.POST.get("desc")
        images=request.FILES["images"] or None
        crtype=Types_Projets.objects.create(type=types, Description=desc, Image=images)
        crtype.save()
        return redirect('list_type')
    return render(request, 'addtype.html', {'en':ut})

@login_required
def mod_type(request, id):
    ids=id
    ut=request.user
    if request.method == "POST":
        types=request.POST.get("types")
        desc=request.POST.get("desc")
        images=request.FILES["images"] or None
        motype=Types_Projets.objects.get(id=ids)
        motype.type=types
        motype.Description=desc
        motype.Image=images
        motype.save()
        return redirect('list_type')
    return render(request, 'modtype.html', {'en':ut, 'types':Types_Projets.objects.get(id=ids)})
@login_required
def sup_type(request, id):
    suptype=Types_Projets.objects.get(id=id)
    suptype.delete()
    return redirect('list_type')


@login_required
def type_contributions(request):
    listtcon=Types_Contributions.objects.all()
    ut=request.user
    context={
        "en":ut,
        'listtcon': listtcon,
    }
    return render(request, 'listtype_contri.html', context)

@login_required
def add_type_contributions(request):
    listtcon=Types_Contributions.objects.all()
    ut=request.user
    context={
        "en":ut,
        'listtcon': Types_Contributions.objects.all(),
        
    }
    if request.method == "POST":
        types=request.POST.get("types")
        crtype=Types_Contributions.objects.create(type=types, users=ut.username)
        crtype.save()
        return redirect('list_type_con')
    
    return render(request, 'addtype_contri.html', context)


@login_required
def mod_type_contribution(request,id):
    ut=request.user
    context={
        "en":ut,
    }
    if request.method == "POST":
        types=request.POST.get("types")
        crtype=Types_Contributions.objects.get(id=id)
        crtype.type=types
        crtype.save()
        return redirect('list_type_con')
    return render(request, 'modtype_contri.html', context)

@login_required
def sup_type_contribution(request,id):
    crtype=Types_Contributions.objects.get(id=id)
    crtype.delete()
    return redirect('list_type_con')
    

@login_required
def list_projet(request):
    ut=request.user
    listpro=Projets.objects.all().order_by("id")
    if request.method == "GET":
        rech=request.GET.get('projet')
        if rech is not None:
            listpro=Projets.objects.filter(Titre__icontains=rech)
    
    context={
        'listpro':listpro,
        'en':ut
    }
    return render(request, 'projets-grid.html', context)

@login_required
def sup_projet(request, id):
    suptype=Projets.objects.get(id=id)
    suptype.delete()
    return redirect('list_projets')


@login_required
def voir_projet(request, id):
    ltype=Types_Contributions.objects.all()
    ut=request.user
    vprojet=Projets.objects.get(id=id)
    conv_datef=vprojet.Date_de_fin
    e=(conv_datef-auj1).days
    vprojet.Echéance=e
    vprojet.save()
   
    context={
        'en':ut,
        'vprojet':vprojet,
        'vutil':User.objects.get(username=vprojet.Utilisateur),
        'ltype':ltype,
      
    }
    return render(request, 'voirprojet.html', context)




@login_required
def add_projet(request):
    ut=request.user
    listuserC=User.objects.filter(is_contri=True)
    listuserA=User.objects.filter(is_contri=False)
    context={
        'en':ut,
        'listtypess':Types_Projets.objects.all(),
        'invalide':""
    }
    if request.method == "POST":
        titre=request.POST.get('titre')
        types=request.POST.get('types')
        t=Types_Projets.objects.get(id=types)
        description=request.POST.get('desc')
        montant=request.POST.get('montant')
        dated=request.POST.get('dated')
        datef=request.POST.get('datef')
        image=request.FILES['image'] or None
        interet=request.POST.get('interet')
        commiss=(2/100)*float(montant)
        
        conv_dated=datetime.strptime(dated, "%Y-%m-%d")
        conv_datef=datetime.strptime(datef, "%Y-%m-%d")
        if conv_dated >= auj and conv_datef > conv_dated:
            e=(conv_datef-conv_dated).days
            procre=Projets.objects.create(Titre=titre, Type=t, 
                                            Utilisateur=ut.username, Description=description,
                                            Images=image, Date_du_début=dated, 
                                            Date_de_fin=datef, Interet=float(interet), 
                                            Montant=float(montant), Reste=float(montant),
                                            Echéance=e, Commission=float(commiss),
                                            compte=ut.compte
                )
                
            procre.save()
            
                
            #Email de création des projets
            current_site=get_current_site(request)
            email_subject="INITIATION D'UN NOUVEAU PROJET"
            messageConfirm= render_to_string("erreur3.html", {
            "name":ut.username,
            "projet":titre,
            "desc":description,
            "domain":current_site.domain,
            'id':procre.id,                
                })
            l=["dieumercibaderha1@gmail.com"]
            l.extend([li.email for li in listuserC])
                    
            email=EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            l)
            email.fail_silently=False
            email.send()
         
            
                #Email de création des projets
            current_site=get_current_site(request)
            email_subject="INITIATION D'UN NOUVEAU PROJET"
            messageConfirm= render_to_string("erreur2.html", {
                "name":ut.username,
                "projet":titre,
                "desc":description,
                "domain":current_site.domain,
                'id':procre.id,
                
                })
            l=["baderha1@gmail.com"]
            l.extend([li.email for li in listuserA])
                    
            email=EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            l
                )
            email.fail_silently=False
            email.send()
            return redirect('list_projets') 
                
        else:
            return render(request, 'addprojet.html', {'en':ut,
        'listtypess':Types_Projets.objects.all(),
        'invalide':"Impossible de créer ce projet car les dates de collecte de fonds sont invalides"})
                
    
    return render(request, 'addprojet.html', context)

@login_required
def projet_grid(request):
    ut=request.user
    listp=Projets.objects.all()
    context={
        'listpro':listp,
        'en':ut
    }
    return render(request, 'projets-grid.html', context)

@login_required
def mod_projet(request, id):
    ut=request.user
    context={
        'en':ut,
        'listtypess':Types_Projets.objects.all(),
        'invalide':"",
        'prom':Projets.objects.get(id=id)
    }
    if request.method == "POST":
        titre=request.POST.get('titre')
        types=request.POST.get('types')
        t=Types_Projets.objects.get(id=types)
        description=request.POST.get('desc')
        montant=request.POST.get('montant')
        dated=request.POST.get('dated')
        datef=request.POST.get('datef')
        image=request.FILES['image'] or None
        interet=request.POST.get('interet')
        commiss=(2/100)*float(montant)
        
        conv_dated=datetime.strptime(dated, "%Y-%m-%d")
        conv_datef=datetime.strptime(datef, "%Y-%m-%d")
        if conv_dated >= auj and conv_datef > conv_dated:
           
            promod=Projets.objects.get(id=id)
            promod.Titre=titre
            promod.Type=t
            promod.Description=description
            promod.Montant=int(montant)
            promod.Images=image
            promod.Date_du_début=dated
            promod.Date_de_fin=datef
            promod.Interet=float(interet)
            promod.Commission=float(commiss)
            promod.Utilisateur=ut.username
            promod.Reste=float(montant)
            promod.save()
            return redirect('list_projets') 
        else:
            return render(request, 'addprojet.html', {'en':ut,
        'listtypess':Types_Projets.objects.all(),
        'invalide':"Impossible de modifier ce projet car les dates de collecte de fonds sont invalides"})
                
    
    return render(request, 'modprojet.html', context)

@login_required
def list_utili(request):
    users=User.objects.all()
    ut=request.user
    return render(request, 'liste_utili.html', {'utlis':users, 'en':ut})

@login_required
def voir_utili(request):
    return render(request, 'voir_utili.html')

@login_required
def add_utili(request):
    return render(request, 'addprojet.html')

@login_required
def utili_grid(request):
    users=User.objects.all()
    ut=request.user
    return render(request, 'utiligrid.html', {'utlis':users, 'en':ut})

@login_required
def mod_utili(request):
    return render(request, 'modprojet.html')

@login_required
def profile(request):
    ut=request.user
    return render(request, 'profile.html', {'en':ut})

@login_required
def contributions(request):
    ut=request.user
    listcon=Contributions.objects.all()           
    context={
        "en":ut,
        'listcon':listcon
    }
    return render(request, 'contributions_.html', context)


@login_required
def user_details(request, id):
    user_d=User.objects.get(id=id)
    userpro=Projets.objects.filter(Utilisateur=user_d.username).count()
    userprolist=Projets.objects.filter(Utilisateur=user_d.username)
    usercontlist=Contributions.objects.filter(Utilisateurs=user_d.username)
    usercont=Contributions.objects.filter(Utilisateurs=user_d.username).count()
    ut=request.user
    context={
        'details':user_d,
        'en':ut,
        'userp':userpro,
        'usercont':usercont,
        'userprolist':userprolist,
        'usercontlist':usercontlist
        
    }
    return render(request, 'user_detail.html', context)

@login_required
def add_contributions(request):
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
                return render(request, "confirmation.html", context)
                
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
                return render(request, "confirmation.html", context)
 
    return redirect('list_projets')

@login_required
def payment_success(request):
    return render(request, "success.html")


@login_required
def payment_cancel(request):
    return render(request, "cancel.html")



@login_required
def edit_contributions(request):
    ut=request.user
    context={
        "en":ut,
    }
    return render(request, 'edit_contributions.html', context)


def oublie(request):
    return render(request, 'oublie.html')

@login_required
def erreur(request):
    return render(request, 'erreur.html')

def registe(request):
    if request.method == "POST":
        username=request.POST.get('username')
        firstname=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        compte=request.POST.get('compte')
        photo=request.FILES['Photo'] or None
        if User.objects.filter(username=username):
            messages.error(request,"ce nom d'utilisateur existe dèja")
            return redirect('registe')
        if User.objects.filter(email=email):
            messages.error(request, "cette addresse mail existe dèja, veuillez entré une nouvelle addresse")
            return redirect('registe')
        #if username.isalnum():
         #   messages.error(request,"le nom doit etre alphanumérique")
        #    return redirect('registe')
        if password1 != password2:
            messages.error("les deux mots de passes sont différents")
            return redirect('registe')
        createutili=User.objects.create_user(username, email, password1)
        createutili.first_name=firstname
        createutili.last_name=last_name
        createutili.Photo=photo
        createutili.compte=compte
        createutili.is_active=True
        createutili.save()
        messages.success(request, "vous avez crée un compte avec succès")
        subject="BIENVENUE DANS CROWDFUNDING"
        message=f"Félicitation "+firstname+" merci de rejoindire la communauté crowdfunding pour \n pour la création et la contribution des projets innovants"
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        #Email de confitmation
        current_site=get_current_site(request)
        email_subject="Confirmation de l'addresse mail dans crowdfunding"
        messageConfirm= render_to_string("erreur.html", {
            "name":createutili.first_name,
            "domain":current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(createutili.pk)),
            'token':generatorToken.make_token(createutili)
        })
        
        email=EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
           [email]
        )
        email.fail_silently=False
        email.send()
        
        
        return redirect('login')
        
            
    
    return render(request, "register.html")

@login_required
def deconnexion(request):
    logout(request)
    return redirect('login')

def logine(request):
    if request.method=="POST":
        usernames=request.POST.get('username')
        password=request.POST.get('password') 
        user=authenticate(request, username=usernames, password=password)
        try:
            my_user= User.objects.get(username=usernames)
            my_user.is_active=True
            my_user.save()
            if user is not None and user.is_active:
                login(request, user)
                if user.is_contri:
                    messages.success(request, "bienvenue")
                    return redirect('indexs')
                else:
                    messages.success(request, "bienvenue")
                    return redirect('index')
                
            elif my_user.is_active == False:
                messages.error(request, "vous n'avez pas confimez l'addresse")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
                return redirect('login')
        except:
                return redirect('login')
        
    return render(request, 'login.html')

def activate(request, uidb64, token):
    try:
       uid=force_text(urlsafe_base64_decode(uidb64))
       user=User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user=None
    if user is not None and generatorToken.check_token(user, token):
       user.is_active=True
       user.save()
       messages.success(request, "votre compte a été activé, connectez-vous maintenant")
       return redirect('login')
    else:
        messages.error("l'activation a échoué")
        return redirect('login')