from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def login_required_supabase(view_func):
    """Decorador para proteger vistas que requieren autenticación"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si hay token en la sesión
        if not request.session.get("supabase_access_token"):
            messages.error(request, "Debes iniciar sesión para acceder")
            return redirect("login")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper