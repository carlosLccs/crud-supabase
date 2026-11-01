from django.shortcuts import render, redirect
from django.contrib import messages
from core.supabase_client import supabase


def login_view(request):
    """Vista de inicio de sesión"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # Guardar sesión en Django
            request.session["supabase_access_token"] = response.session.access_token
            request.session["supabase_user_id"] = response.user.id
            request.session["supabase_user_email"] = response.user.email
            
            messages.success(request, f"Bienvenido {response.user.email}")
            return redirect("lista_personas")
            
        except Exception as e:
            messages.error(request, "Credenciales incorrectas")
    
    return render(request, "personas/login.html")


def registro_view(request):
    """Vista de registro de nuevo usuario"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        
        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "personas/registro.html")
        
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            messages.success(request, "Usuario creado. Ahora puedes iniciar sesión")
            return redirect("login")
            
        except Exception as e:
            messages.error(request, f"Error al crear usuario: {str(e)}")
    
    return render(request, "personas/registro.html")


def logout_view(request):
    """Cerrar sesión"""
    try:
        supabase.auth.sign_out()
    except:
        pass
    
    # Limpiar sesión de Django
    request.session.flush()
    messages.success(request, "Sesión cerrada")
    return redirect("login")