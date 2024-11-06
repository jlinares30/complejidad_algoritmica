from django.shortcuts import render
import networkx as nx
import re
import json
from .models import Proveedor, Router  # Ajusta la importación según tu estructura de proyecto


def extraer_velocidades(velocidad_str):
    # Usar una expresión regular para encontrar los valores de velocidad
    match = re.search(r'(\d+)\s*<=\s*BW\s*<\s*(\d+)\s*(kbps|Mbps)', velocidad_str)
    if match:
        velocidad_minima = int(match.group(1))
        velocidad_maxima = int(match.group(2))
        unidad = match.group(3)

        # convertir a kbps
        if unidad == 'Mbps':
            velocidad_minima *= 1000  
            velocidad_maxima *= 1000  
        elif unidad is None:
            pass

        return velocidad_minima, velocidad_maxima
    return None, None

def crear_grafo():
    G = nx.Graph()

    # Obtener solo los primeros 2000 proveedores y sus routers
    proveedores = Proveedor.objects.select_related('router')[:1500]  # Limitar a 2000 registros
    # Agregar nodos para cada proveedor y router
    for proveedor in proveedores:
        G.add_node(proveedor.empresa, tipo='Proveedor')  # Asumiendo que 'empresa' es el nombre del proveedor
        if proveedor.router:  # Verifica que el router no sea None
            nombre_router = proveedor.router.nombre  # Accede al nombre del router
            G.add_node(nombre_router, tipo='Router')

            # Extraer las velocidades
            velocidad_minima, velocidad_maxima = extraer_velocidades(proveedor.velocidad)

            if velocidad_minima is not None and velocidad_maxima is not None:
                # Calcular el peso de la arista como el promedio de las velocidades
                peso_velocidades = (velocidad_minima + velocidad_maxima) / 2
                
                # Incorporar el número de conexiones en el peso
                peso_total = peso_velocidades * proveedor.conexiones  # Multiplica por el número de conexiones
                
                # Agregar la arista al grafo
                G.add_edge(proveedor.empresa, nombre_router, weight=peso_total)

    return G

def grafo_a_json(G):
    nodos = [{"id": node, "tipo": G.nodes[node]['tipo']} for node in G.nodes()]
    aristas = [{"source": u, "target": v, "weight": d['weight']} for u, v, d in G.edges(data=True)]
    
    return json.dumps({"nodos": nodos, "aristas": aristas})

def index(request):
    G = crear_grafo()  # Asumiendo que esta función ya está definida
    #print(G)
    grafo_json = grafo_a_json(G)  # Convertir el grafo a JSON
    #print(grafo_json)
    return render(request, 'grafo_app/index.html', {'grafo_json': grafo_json})  # Pasar el JSON a la plantilla

# def index(request):
#     return render(request, 'grafo_app/index.html')
