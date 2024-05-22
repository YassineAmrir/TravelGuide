from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('offres-voyage/', views.offres_voyage, name='offres_voyage'),
    path('offres-special/', views.offres_special, name='offres_special'),
    path('a-propos/', views.about, name='about'),
    path('bookNow/', views.bookNow, name='bookNow'),
    path('logout/', views.logout, name='logout'),
    path('MonProfile/', views.MonProfile, name='Profile'),
    path('editeProfile/', views.editProfile, name='editProfile'),
    path('voyage/<int:id>/', views.voyage, name='voyage'),
    path('reservation/<int:id>/', views.reserver, name='reserver'),
    path('payement/<int:reservation>/', views.payement, name='payement'),
    path('activities/', views.activites, name='activities'),
    path('activities/<int:id>/', views.activity_detail, name='activity_detail'),
    path('payement_success/', views.payement_success, name='payement_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/ModifyUser/<int:id>/', views.dashboardModifyUser, name='dashboardModifyUser'),
     path('dashboard/AddUser', views.dashboardAddUser, name='dashboardAddUser'),
      path('dashboard/DeleteUser/<int:id>/', views.dashboardDeleteUser, name='dashboardDeleteUser'),
    path('dashboard/AddOffer', views.dashboardAddOffer, name='dashboardAddOffer'),
     path('dashboard/ModifyOffer/<int:id>/', views.dashboardModifyOffer, name='dashboardModifyOffer'),
      path('dashboard/DeleteOffer/<int:id>/', views.dashboardDeleteOffer, name='dashboardDeleteOffer'),
       path('dashboard/AddActivity', views.dashboardAddActivitie, name='dashboardAddActivitie'),
       path('dashboard/ModifyActivity/<int:id>/', views.dashboardModifyActivitie, name='dashboardModifyActivitie'),
        path('dashboard/DeleteActivity/<int:id>/', views.dashboardDeleteActivitie, name='dashboardDeleteActivitie'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)