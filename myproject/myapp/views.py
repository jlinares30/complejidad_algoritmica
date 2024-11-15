from django.shortcuts import render
import networkx as nx
import re
import json
from .models import Proveedor, Router
import math
import heapq as hq
from django.http import JsonResponse


def extraer_latencia(velocidad_str):
    match = re.search(r'(\d+)\s*<=\s*BW\s*<\s*(\d+)\s*(kbps|Mbps)', velocidad_str)
    if match:
        velocidad_minima = int(match.group(1))
        velocidad_maxima = int(match.group(2))
        unidad = match.group(3)

        # Convertir a kbps
        if unidad == 'Mbps':
            velocidad_minima *= 1000
            velocidad_maxima *= 1000

        return (velocidad_minima + velocidad_maxima) / 2
    return None


def crear_grafo(horario):
    G = nx.Graph()
    proveedores = Proveedor.objects.select_related('router')
    
    for proveedor in proveedores:
        latencia_base = 30 if horario == 'dia' else 70
        latencia = latencia_base / (1 + proveedor.conexiones)
        latencia += extraer_latencia(proveedor.velocidad) or 0

        G.add_node(proveedor.empresa, departamento=proveedor.departamento, tipo='Proveedor')
        if proveedor.router:
            nombre_router = proveedor.router.nombre
            G.add_node(nombre_router, tipo='Router')
            G.add_edge(proveedor.empresa, nombre_router, weight=latencia)
    return G


def mejor_empresa_por_departamento(grafo, departamento):
    empresas_departamento = [n for n, d in grafo.nodes(data=True) if d.get('departamento') == departamento]
    if not empresas_departamento:
        return None, None

    mejor_empresa = None
    menor_latencia = math.inf

    for empresa in empresas_departamento:
        latencia = sum(d['weight'] for _, _, d in grafo.edges(empresa, data=True))
        if latencia < menor_latencia:
            menor_latencia = latencia
            mejor_empresa = empresa

    return mejor_empresa, menor_latencia


def grafo_a_json(G):
    nodos = [{"id": node, "tipo": G.nodes[node]['tipo']} for node in G.nodes()]
    aristas = [{"source": u, "target": v, "weight": d['weight']} for u, v, d in G.edges(data=True)]
    
    return json.dumps({"nodos": nodos, "aristas": aristas})


def index(request):
    departamento = request.GET.get('departamento')
    horario = request.GET.get('horario', 'dia')
    mejor_empresa = None
    menor_latencia = None

    G = crear_grafo(horario)
    grafo_json = grafo_a_json(G)

    if departamento:
        mejor_empresa, menor_latencia = mejor_empresa_por_departamento(G, departamento)

    return render(request, 'grafo_app/index.html', {
        'grafo_json': grafo_json,
        'mejor_empresa': mejor_empresa,
        'menor_latencia': menor_latencia,
    })
