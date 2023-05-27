from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('login',views.login, name='login'),
    path('register',views.register),
    path('user_home',views.user_home),
    path('logout',views.logout_view),
    path('allgames',views.all_games),
    path('allevents',views.view_events),
    path('bookevent/<int:id>/<int:gid>/',views.book_event),
    path('my',views.mybookings),
    path('cancel/<int:id>/',views.cancel),
    path('payment/<int:booking_id>/',views.make_payment,name='payment'),
    path('upload_result/<int:id>/',views.upload_result),
    path('view',views.viewprofile),
    path('edit',views.edituer),
    path('change',views.changepassword),


]