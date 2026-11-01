from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.supabase_client import supabase
from .decorators import login_required_supabase


@login_required_supabase  # ← Añadir este decorador
def lista_personas(request):
    """Listar todas las personas"""
    response = supabase.table("personas").select("*").order("id", desc=True).execute()
    return render(request, "personas/lista.html", {"personas": response.data})


@login_required_supabase  # ← Añadir este decorador
def crear_persona(request):
    """Crear una nueva persona"""
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "apellido": request.POST.get("apellido"),
            "email": request.POST.get("email") or None,
            "telefono": request.POST.get("telefono") or None,
            "fecha_nacimiento": request.POST.get("fecha_nacimiento") or None,
        }
        supabase.table("personas").insert(data).execute()
        messages.success(request, "Persona creada correctamente")
        return redirect("lista_personas")
    return render(request, "personas/formulario.html", {"accion": "Crear"})


@login_required_supabase  # ← Añadir este decorador
def editar_persona(request, id):
    """Editar una persona existente"""
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "apellido": request.POST.get("apellido"),
            "email": request.POST.get("email") or None,
            "telefono": request.POST.get("telefono") or None,
            "fecha_nacimiento": request.POST.get("fecha_nacimiento") or None,
        }
        supabase.table("personas").update(data).eq("id", id).execute()
        messages.success(request, "Persona actualizada")
        return redirect("lista_personas")

    # Cargar datos actuales
    response = supabase.table("personas").select("*").eq("id", id).execute()
    persona = response.data[0] if response.data else None
    return render(
        request,
        "personas/formulario.html",
        {"accion": "Editar", "persona": persona},
    )


@login_required_supabase  # ← Añadir este decorador
def eliminar_persona(request, id):
    """Eliminar una persona"""
    supabase.table("personas").delete().eq("id", id).execute()
    messages.success(request, "Persona eliminada")
    return redirect("lista_personas")