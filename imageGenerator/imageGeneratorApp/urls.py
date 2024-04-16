from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup,name='signup'),
    path('login/',views.loginView, name='login'),
    #  path("home/",views.home,name="home"),
    path("",views.landing,name="landing"),
    path("about/",views.about, name="about"),
    path("editor/",views.editor, name="editor"),
    path("explore/",views.explore, name="explore"),
    #Password_Change
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    #Password_Reset
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('generate_image/', views.generate_image, name='generate_image'),

]
