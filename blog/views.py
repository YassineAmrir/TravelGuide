from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import OffreVoyage ,Image, Reservation , Activite , Payment
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import stripe
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from django.shortcuts import render
from django.views import View

#stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(request):
    # Logique pour créer le paiement avec PayPal
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/success/",
            "cancel_url": "http://localhost:8000/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Produit",
                    "sku": "001",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Description du paiement"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                # Rediriger l'utilisateur vers l'URL d'approbation PayPal
                return HttpResponseRedirect(link.href)
    else:
        return HttpResponse('Erreur lors de la création du paiement')


def home(request):
    activites = Activite.objects.all()
    destinations = OffreVoyage.objects.values_list('destination', flat=True).distinct()
    offres=OffreVoyage.objects.all()
    offres_with_images = []
    for offre in offres:
        images = Image.objects.filter(offre_voyage=offre)
        offres_with_images.append({
            'offre': offre,
            'images': images
        })
    return render(request, 'blog/Home.html', {'offres_with_images': offres_with_images,'activites':activites,'GENRE_CHOICES': OffreVoyage.GENRE_CHOICES,'destinations': destinations})

def offres_voyage(request):
     # Obtenez les paramètres de recherche, filtrage et tri depuis la requête
    keyword = request.GET.get('location', '')
    category = request.GET.get('activities', '')
    destination = request.GET.get('select-destination', '')
    min_price = request.GET.get('prix_min', None)
    max_price = request.GET.get('prix_max', None)
    min_duration = request.GET.get('duree_min', None)

    # Affichez les paramètres pour déboguer
    print(f'Keyword: {keyword}')
    print(f'Category: {category}')
    print(f'Destination: {destination}')
    print(f'Min Price: {min_price}')
    print(f'Max Price: {max_price}')
    print(f'Min Duration: {min_duration}')

    # Filtrez les offres en fonction des paramètres
    offres = OffreVoyage.objects.filter(speciale=False)

    if keyword:
        offres = offres.filter(title__icontains=keyword)

    if category:
        offres = offres.filter(genre=category)

    if destination:
        offres = offres.filter(destination__icontains=destination)

    if min_price:
        offres = offres.filter(price__gte=min_price)

    if max_price:
        offres = offres.filter(price__lte=max_price)

    if min_duration:
        offres = offres.filter(duration__gte=min_duration)

    # Triez les offres par défaut (ajoutez plus d'options de tri si nécessaire)
    offres = offres.order_by('price')
    offres_with_images = []
    for offre in offres:
        images = Image.objects.filter(offre_voyage=offre)
        offres_with_images.append({
            'offre': offre,
            'images': images
        })

    return render(request, 'blog/offresVoyage.html', {'offres_with_images': offres_with_images, 'GENRE_CHOICES': OffreVoyage.GENRE_CHOICES})

def offres_special(request):
      # Obtenez les paramètres de recherche, filtrage et tri depuis la requête
    keyword = request.GET.get('location', '')
    category = request.GET.get('activities', '')
    destination = request.GET.get('select-destination', '')
    min_price = request.GET.get('prix_min', None)
    max_price = request.GET.get('prix_max', None)
    min_duration = request.GET.get('duree_min', None)

    # Affichez les paramètres pour déboguer
    print(f'Keyword: {keyword}')
    print(f'Category: {category}')
    print(f'Destination: {destination}')
    print(f'Min Price: {min_price}')
    print(f'Max Price: {max_price}')
    print(f'Min Duration: {min_duration}')

    # Filtrez les offres en fonction des paramètres
    offres = OffreVoyage.objects.filter(speciale=True)

    if keyword:
        offres = offres.filter(title__icontains=keyword)

    if category:
        offres = offres.filter(genre=category)

    if destination:
        offres = offres.filter(destination__icontains=destination)

    if min_price:
        offres = offres.filter(price__gte=min_price)

    if max_price:
        offres = offres.filter(price__lte=max_price)

    if min_duration:
        offres = offres.filter(duration__gte=min_duration)

    # Triez les offres par défaut (ajoutez plus d'options de tri si nécessaire)
    offres = offres.order_by('price')
    offres_with_images = []
    for offre in offres:
        images = Image.objects.filter(offre_voyage=offre)
        offres_with_images.append({
            'offre': offre,
            'images': images
        })

    return render(request, 'blog/offresSpecial.html', {'offres_with_images': offres_with_images, 'GENRE_CHOICES': OffreVoyage.GENRE_CHOICES})
   
def signin(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password'] 
        user = auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            return redirect('blog:home')
        else:
            messages.info(request,'invalide')
            return redirect('blog:signin')
    else :
      return render(request, 'blog/singIn.html', {})

def signup(request):
    if request.method == 'POST':
     first_name = request.POST['first_name']
     last_name = request.POST['last_name']
     username = request.POST['username']
     email = request.POST['email']
     password1 = request.POST['password1']
     password2 = request.POST['password2']
     if password1 == password2:
             user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,last_name=last_name)
             user.save()
             UserProfile.objects.create(user_id=user.id )
             print('user created')
             messages.success(request, 'Account created successfully')
             return redirect('blog:signin') # Assuming 'home' is a named URL patter
     else:
             return HttpResponse('Passwords do not match', status=400)
    else:
       return render(request, 'blog/singUp.html', {})
    
def about(request):
    return render(request, 'blog/about.html')

def bookNow(request):
    return render(request, 'blog/bookNow.html')

@login_required
def logout(request):
     auth.logout(request)
     return redirect('blog:signin')
@login_required
def MonProfile (request):
    user = request.user
    profil=get_object_or_404(UserProfile,user=user)
    
    reservations = Reservation.objects.filter(user=user)  # Modifier ici pour filtrer par user

   
    offres_voyage = {reservation.offre_voyage : reservation.num_places for reservation in reservations}

    # Passer le profil, les réservations et les offres de voyage au template
    return render(request, 'blog/MonProfile.html', {'profil': profil, 'reservations': reservations, 'offres_voyage': offres_voyage})
    
@login_required
def editProfile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
    
        age = request.POST.get('age', None)

        profile_photo = request.FILES.get('profile_photo')

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.age = age

        if profile_photo:
            file_path = default_storage.save('profile_images/' + profile_photo.name, profile_photo)
            profile.image = file_path
        elif created:
            profile.image = 'profile_images/profile.jpg'  # Utiliser l'image par défaut si un nouveau profil est créé

        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('blog:Profile')  # Assurez-vous que le nom de redirection est correct
    user = request.user
    profil=get_object_or_404(UserProfile,user=user)
    return render(request, 'blog/edite.html',{'profil':profil})

def voyage(request, id):
    offre_voyage = get_object_or_404(OffreVoyage, id=id)
    activites = Activite.objects.filter(offre_voyage=offre_voyage)  
    images = Image.objects.filter(offre_voyage=offre_voyage)
    return render(request, 'blog/voyage.html', {'OffreVoyage': offre_voyage, 'images': images,'activites':activites})

@login_required(login_url='blog:signin')
def reserver(request,id):
    if request.method == 'POST':
       
        full_name = request.POST.get('fullName')
        num_places = request.POST.get('numPlaces')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        commentaire = request.POST.get('commentaire', '')
        prix=request.POST.get('totalPrice')


        current_user = request.user
        selected_offer = get_object_or_404(OffreVoyage, id=id)

        
        reservation = Reservation(total_price=prix,full_name=full_name, num_places=num_places, email=email, phone=phone,user=current_user,commentaire=commentaire,offre_voyage=selected_offer,)
        reservation.save()
       
        
        return redirect('blog:payement',reservation.id )  # Replace 'success_url' with your success page URL
    offre_voyage = get_object_or_404(OffreVoyage, id=id)
    prix_offre = offre_voyage.price
    return render(request, 'blog/réserve.html', {'offre_voyage_id': id, 'prix_offre': prix_offre})
@login_required   
def payement_success(request):
     return render(request, 'blog/paiement_success.html')



@login_required(login_url='blog:signin')
def payement(request, reservation):
    reservation = get_object_or_404(Reservation, id=reservation)
    if request.method == 'POST':
        nom_porteur = request.POST.get('cardholderName')
        stripe_token = request.POST.get('stripeToken')
        montant = request.POST.get('amount')

        # Configurez votre clé secrète Stripe (remplacez par votre propre clé secrète)
        stripe.api_key = 'sk_test_51OgBP4CUbmAw4a7oohu8IHVSXDByRusef0uCorsNQNMXSRvRY5tJxG03eRfQrUgPU8d0hxw8FCA8dgt3hszaSxpw000HHpNJ2L'

        try:
            # Créez une charge (transaction) avec Stripe
            charge = stripe.Charge.create(
                amount=int(float(montant)) * 100,  # Montant en centimes
                currency='eur',
                description='Paiement avec carte de crédit',
                source=stripe_token,  # Fournissez la source de paiement
                receipt_email=reservation.email,  # Email de confirmation du paiement
            )
            current_user = request.user
            # Vous pouvez également enregistrer des informations dans votre base de données ou effectuer d'autres traitements nécessaires ici
            # Create a Payment object in your database
            payment = Payment( user=current_user, amount=montant )
            payment.save()
            payment.send_confirmation_email(reservation.email)
            # Redirection vers une page de confirmation de paiement
            return render(request, 'blog/paiement_success.html')

        except stripe.error.CardError as e:
            # Gérer les erreurs de carte
            message_erreur = e.error.message
            return render(request, 'blog/payment_refusé.html', {'message_erreur': message_erreur})
        except stripe.error.StripeError as e:
            # Gérer d'autres erreurs Stripe
            message_erreur = str(e)
            return render(request, 'blog/payment_refusé.html', {'message_erreur': message_erreur})
    return render(request, 'blog/payementEnligne.html', {'reservation': reservation})



def activites(request):
     activities = Activite.objects.all()
     print(f'Keyword: {activities}')
     return render(request, 'blog/activities.html', {'activities': activities})

def activity_detail(request, id):
    activite = get_object_or_404(Activite, id=id)
    offres_voyage = activite.offre_voyage
    images = Image.objects.filter(offre_voyage=offres_voyage)

    print(offres_voyage)

    return render(request, 'blog/activity_detail.html', {'activite': activite, 'offres_voyage': offres_voyage , 'images':images})

@login_required
def dashboard(request):
 if request.user.is_superuser:
    user = User.objects.all()
    offres_voyage=OffreVoyage.objects.all()
    reservations=Reservation.objects.all()
    activities=Activite.objects.all()
    return render(request, 'blog/dashboard.html', {'users': user,'offres_voyage':offres_voyage, 'reservations':reservations,'activities':activities})
 else :
     return render(request, 'blog/singIn.html', {})
@login_required
def dashboardModifyUser(request,id):
     user = get_object_or_404(User, id=id)
     profil=get_object_or_404(UserProfile,user=user)
     if request.method == 'POST':
        # Mettez à jour les champs du modèle avec les données du POST
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        profil.age = request.POST.get('age')
        
       
        # Sauvegardez les modifications dans la base de données
        user.save()
        profil.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('blog:dashboard')  # Redirigez vers la page de tableau de bord ou une autre page appropriée après la mise à jour du profil
     return render(request, 'blog/dashbordModifyUser.html',{'user':user , 'profil':profil})
@login_required
def dashboardAddUser(request):

   if request.method == 'POST':
     first_name = request.POST['first_name']
     last_name = request.POST['last_name']
     username = request.POST['username']
     email = request.POST['email']
     password1 = request.POST['password1']
    
    
     user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,last_name=last_name)
     user.save()
     UserProfile.objects.create(user_id=user.id )
           
     messages.success(request, 'Account created successfully')
     return redirect('blog:dashboard') # Assuming 'home' is a named URL patter
    
   else:
     return render(request, 'blog/dashboardAddUser.html')     
@login_required
def dashboardDeleteUser(request,id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=id)
        profil=get_object_or_404(UserProfile,user=user)
        user.delete()
        profil.delete()


        messages.success(request, 'User deleted successfully.')

        # Redirige vers la page souhaitée après la suppression (par exemple, la liste des utilisateurs)
        return redirect('blog:dashboard')
    return render(request, 'blog/dashboard.html')     
@login_required
def dashboardAddOffer(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        destination = request.POST.get('destination')
        countries = request.POST.get('countries')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        number_of_people = request.POST.get('number_of_people')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')
        speciale = request.POST.get('speciale') == 'on'  # Checkbox
        hebergement = request.POST.get('hebergement')
        type_transport = request.POST.get('type_transport')
        compagnie_transport = request.POST.get('compagnie_transport')
        # Créer une nouvelle instance d'OffreVoyage
        new_offer = OffreVoyage(
            title=title,
            destination=destination,
            countries=countries,
            description=description,
            start_date=start_date,
            end_date=end_date,
            price=price,
            number_of_people=number_of_people,
            duration=duration,
            genre=genre,
            speciale=speciale,
            hebergement=hebergement,
            type_transport=type_transport,
            compagnie_transport=compagnie_transport
        )
        # Enregistrer l'offre dans la base de données
        new_offer.save()
        imag = Image(image=image, offre_voyage_id=new_offer.id)
        imag.save()
        # Rediriger vers la page des offres après l'ajout
        return redirect('blog:dashboard')
    return render(request, 'blog/dashboardAddOffer.html')
@login_required
def dashboardModifyOffer(request,id):
     offres_voyage = get_object_or_404(OffreVoyage, id=id)
     if request.method == 'POST':
        
        title = request.POST.get('title')
        destination = request.POST.get('destination')
        countries = request.POST.get('countries')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('price')
        imag = request.FILES.get('image')
        number_of_people = request.POST.get('number_of_people')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')
        speciale = request.POST.get('speciale') == 'on'  # Checkbox
        hebergement = request.POST.get('hebergement')
        type_transport = request.POST.get('type_transport')
        compagnie_transport = request.POST.get('compagnie_transport')
       
        # Sauvegardez les modifications dans la base de données
        # Mettre à jour les champs de l'objet OffreVoyage
        offres_voyage.title = title
        offres_voyage.destination = destination
        offres_voyage.countries = countries
        offres_voyage.description = description
        offres_voyage.start_date = start_date
        offres_voyage.end_date = end_date
        offres_voyage.price = price
        offres_voyage.number_of_people = number_of_people
        offres_voyage.duration = duration
        offres_voyage.genre = genre
        offres_voyage.speciale = speciale
        offres_voyage.hebergement = hebergement
        offres_voyage.type_transport = type_transport
        offres_voyage.compagnie_transport = compagnie_transport

        # Sauvegarder les modifications dans la base de données
        offres_voyage.save()
        images = Image.objects.filter(offre_voyage=offres_voyage)
        if images.exists():
            image = images.first()
        else:
          image = Image(offre_voyage=offres_voyage, image=imag)
          image.image = imag
          image.save()
        


        messages.success(request, 'Profile updated successfully')
        return redirect('blog:dashboard')  # Redirigez vers la page de tableau de bord ou une autre page appropriée après la mise à jour du profil
     return render(request, 'blog/dashboardModifyOffer.html',{'offres_voyage':offres_voyage})
@login_required
def dashboardDeleteOffer(request,id):
    if request.method == 'POST':
        offres_voyage= get_object_or_404(OffreVoyage,id=id)
        offres_voyage.delete()


        messages.success(request, 'Offer deleted successfully.')

        # Redirige vers la page souhaitée après la suppression (par exemple, la liste des utilisateurs)
        return redirect('blog:dashboard')
    return render(request, 'blog/dashboard.html')  
@login_required
def dashboardAddActivitie(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        duration = int(request.POST.get('duration', 0))
        lieu = request.POST.get('lieu')
        participants_min = int(request.POST.get('participants_min', 0))
        participants_max = int(request.POST.get('participants_max', 0))
        image = request.FILES.get('image')
        offre_voyage_id = int(request.POST.get('offre_voyage', 0))
        prix_initial = float(request.POST.get('prix_initial', 0.0))
        prix_promo = float(request.POST.get('prix_promo', 0.0))

        offre_voyage = None
        if offre_voyage_id:
            # Vous devez définir la relation correcte avec votre modèle OffreVoyage ici
            offre_voyage = OffreVoyage.objects.get(id=offre_voyage_id)

        activitie = Activite.objects.create(
            nom=nom,
            description=description,
            duration=duration,
            lieu=lieu,
            participants_min=participants_min,
            participants_max=participants_max,
            image=image,
            offre_voyage=offre_voyage,
            prix_initial=prix_initial,
            prix_promo=prix_promo
        )


     
        return redirect('blog:dashboard') # Assuming 'home' is a named URL patter
    return render(request, 'blog/dashboardAddActivity.html')  
@login_required
def dashboardModifyActivitie(request, id):
    # Récupérer l'activité existante
    activity = get_object_or_404(Activite, id=id)

    if request.method == 'POST':
        # Obtenir les données du formulaire
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        duration = int(request.POST.get('duration', 0))
        lieu = request.POST.get('lieu')
        participants_min = int(request.POST.get('participants_min', 0))
        participants_max = int(request.POST.get('participants_max', 0))
        image = request.FILES.get('image')
        offre_voyage_id = int(request.POST.get('offre_voyage', 0))
        prix_initial = float(request.POST.get('prix_initial', 0.0))
        prix_promo = float(request.POST.get('prix_promo', 0.0))

        # Récupérer l'objet OffreVoyage lié
        offre_voyage = None
        if offre_voyage_id:
            offre_voyage = OffreVoyage.objects.get(id=offre_voyage_id)

        # Mettre à jour les données de l'activité existante
        activity.nom = nom
        activity.description = description
        activity.duration = duration
        activity.lieu = lieu
        activity.participants_min = participants_min
        activity.participants_max = participants_max
        activity.prix_initial = prix_initial
        activity.prix_promo = prix_promo

        # Mettre à jour l'image si une nouvelle image est fournie
        if image:
            activity.image = image

        # Mettre à jour l'offre_voyage si une nouvelle offre_voyage est fournie
        if offre_voyage:
            activity.offre_voyage = offre_voyage

        # Enregistrer les modifications
        activity.save()

        return redirect('blog:dashboard')

    # Passer l'activité à la page de modification
    return render(request, 'blog/dashboardModifyActivity.html', {'activity': activity})
@login_required
def dashboardDeleteActivitie(request,id):
    if request.method == 'POST':
        activites= get_object_or_404(Activite,id=id)
        activites.delete()


        messages.success(request, 'Offer deleted successfully.')

        # Redirige vers la page souhaitée après la suppression (par exemple, la liste des utilisateurs)
        return redirect('blog:dashboard')
    return render(request, 'blog/dashboard.html')
    




