from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="ShopHome"),
    path('login/',views.awlogin,name="LogIn"),
    path('logout/',views.awlogout,name="LogOut"),
    path('signup/',views.signup,name="SignUp"),
    path('about/',views.about,name="AboutUs"),
    path('contact/',views.contact,name="ContactUs"),
    path('tracker/',views.tracker,name="TrackingStatus"),
    path('search/',views.search,name="Search"),
    path('productview/<int:myid>',views.prodView,name="ProductView"),
    path('checkout/',views.checkout,name="CheckOut"),
    path('handlerequest/',views.handlerequest,name="HandleRequest"),
    path('error404/',views.error404,name="Error404"),
    path('myprofile/',views.myprofile,name="MyProfile"),
    path('editinfo/',views.editinfo,name="EditInfo"),
    path('uploadimage/',views.uploadimage,name="UploadImage"),
    path('workinprogress/',views.winp,name="WINP"),
    path('blog/',views.blog,name="BLOG")
]