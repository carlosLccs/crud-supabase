from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Autenticación
    path("login/", auth_views.login_view, name="login"),
    path("registro/", auth_views.registro_view, name="registro"),
    path("logout/", auth_views.logout_view, name="logout"),
    
    # CRUD Personas (protegidas)
    path("", views.lista_personas, name="lista_personas"),
    path("crear/", views.crear_persona, name="crear_persona"),
    path("editar/<int:id>/", views.editar_persona, name="editar_persona"),
    path("eliminar/<int:id>/", views.eliminar_persona, name="eliminar_persona"),
]