from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('bill/<str:pk>/', views.bill, name="bill"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-bill/', views.createbill, name="create-bill"),
    path('update-bill/<str:pk>/', views.updatebill, name="update-bill"),
    path('delete-bill/<str:pk>/', views.deletebill, name="delete-bill"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('bill/<int:pk>/vote/', views.vote_bill, name='vote-bill'),
    path('bill/<int:pk>/votes-by-location/', views.bill_votes_by_location, name='votes-by-location'),
    path('bill/<int:bill_id>/statistics/', views.bill_statistics, name='bill-statistics'),
]