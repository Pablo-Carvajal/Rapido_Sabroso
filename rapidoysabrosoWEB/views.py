from django.shortcuts import render, redirect
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Producto,  Categoria   # Asegúrate de importar el modelo Producto

# Vista de autenticación
def vista1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu') 
        else:
            error_message = 'Usuario o contraseña incorrectos.'
            return render(request, 'service/vista1.html', {'error_message': error_message})
    
    return render(request, 'service/vista1.html')

def menu(request):
    return render(request, 'service/menu.html')

def logout_view(request):
    logout(request)
    return redirect('vista1')

def menu(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    marcas_unicas = Producto.objects.values_list('marca', flat=True).distinct()
    context = {
        'productos': productos,
        'marcas_unicas': marcas_unicas,
        'categorias': categorias
    }
    return render(request, 'service/menu.html', context)

    
def productos_por_marca(request, marca):
    # Filtrar los productos por la marca seleccionada
    productos_filtrados = Producto.objects.filter(marca=marca)
    return render(request, 'service/marca.html', {'productos': productos_filtrados, 'marca': marca})

from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

def categorias(request, categoria):
    categorias = Categoria.objects.all()

    if categoria == "Todas":
        productos = Producto.objects.all()  
    else:
        
        categoria_obj = get_object_or_404(Categoria, nombre=categoria) 
        productos = Producto.objects.filter(categoria=categoria_obj) 

    context = {
        'productos': productos,
        'categoria_seleccionada': categoria,
        'categorias': categorias 
    }
    return render(request, 'service/categoria.html', context)

def producto(request, id):
    categorias = Categoria.objects.all()
    producto = get_object_or_404(Producto, id=id)
    context = {
        'producto': producto,
        'categorias': categorias 
    }
    return render(request, 'service/producto.html', context )




from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Orden, OrdenProducto

def agregar_a_orden(request, producto_id):
    # Obtenemos la orden actual o creamos una nueva
    orden, creada = Orden.objects.get_or_create(id=request.session.get('orden_id'))

    # Guardamos la id de la orden en la sesión
    request.session['orden_id'] = orden.id

    # Obtenemos el producto por su ID
    producto = get_object_or_404(Producto, id=producto_id)

    # Agregamos el producto a la orden o aumentamos la cantidad si ya está
    orden_producto, creado = OrdenProducto.objects.get_or_create(orden=orden, producto=producto)
    if not creado:
        orden_producto.cantidad += 1
    orden_producto.save()

    # Calcular el total de la orden, realizando la conversión en una línea
    total = sum(float(item.producto.precio.replace('$', '').replace('.', '').replace(',', '.')) * int(item.cantidad) for item in orden.ordenproducto_set.all())
    
    # Guardar el total en la orden
    orden.total = total
    orden.save()

    return redirect('ver_orden')


def eliminar_de_orden(request, producto_id):
    orden_id = request.session.get('orden_id')
    if orden_id:
        orden = get_object_or_404(Orden, id=orden_id)
        orden_producto = orden.ordenproducto_set.filter(producto__id=producto_id).first()
        
        if orden_producto:
            orden_producto.delete()
            
            # Recalcular el total
            total = sum(float(item.producto.precio.replace('$', '').replace('.', '').replace(',', '.')) * item.cantidad for item in orden.ordenproducto_set.all())
            orden.total = total
            orden.save()

    return redirect('ver_orden')




def ver_orden(request):
    orden = Orden.objects.get(id=request.session.get('orden_id'))
    productos_en_orden = orden.ordenproducto_set.all()
    return render(request, 'service/orden.html', {'orden': orden, 'productos_en_orden': productos_en_orden})



