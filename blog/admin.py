from django.contrib import admin
from .models import OffreVoyage, Image,Reservation,Activite

# Voici où vous définissez la classe ImageInline
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Nombre d'emplacements vides pour de nouvelles images

# Voici où vous définissez la classe OffreVoyageAdmin avec l'inline Image
class OffreVoyageAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    # Ajoutez ici d'autres options de personnalisation si nécessaire

# Enregistrez vos modèles en utilisant les classes personnalisées ci-dessus

admin.site.register(Image)  # Vous pourriez aussi vouloir personnaliser l'admin de Image si nécessaire
admin.site.register(Reservation)
admin.site.register(Activite)


from django.contrib import admin
from .models import OffreVoyage, Activite

class ActiviteInline(admin.TabularInline):  # ou admin.StackedInline pour un style différent
    model = Activite
    extra = 1  # Combien de champs vides à afficher pour de nouvelles activités

class OffreVoyageAdmin(admin.ModelAdmin):
    inlines = [ActiviteInline]
    # Vous pouvez également ajouter d'autres options ici, comme list_display, search_fields, etc.

admin.site.register(OffreVoyage, OffreVoyageAdmin)

