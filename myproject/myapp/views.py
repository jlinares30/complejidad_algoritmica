from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import networkx as nx
import os

def cargar_datos(file_path, cantidad_datos):
    df = pd.read_excel(file_path, header=None, nrows=cantidad_datos)
    return df

def procesar_datos(df):
    # (Tu código existente aquí)
    df['Merged'] = df[0].astype(str) + ';' + df[1].astype(str) + ';' + df[2].astype(str)
    df_split = df['Merged'].str.split(';', expand=True)
    
    columnas = ['AÑO', 'TRIMESTRE', 'PROVEEDOR', 'COD_DEPARTAMENTO', 'DEPARTAMENTO', 
                'COD_MUNICIPIO', 'MUNICIPIO', 'SEGMENTO', 'TECNOLOGIA', 
                'VELOCIDAD_BAJADA', 'VELOCIDAD_SUBIDA', 'NUMERO_ACCESOS', 
                'COLUMNA_EXTRA1', 'COLUMNA_EXTRA2']
    df_split.columns = columnas

    df_split['VELOCIDAD_BAJADA'] = pd.to_numeric(df_split['VELOCIDAD_BAJADA'], errors='coerce')
    df_split['VELOCIDAD_SUBIDA'] = pd.to_numeric(df_split['VELOCIDAD_SUBIDA'], errors='coerce')
    df_split['PROVEEDOR'] = df_split['PROVEEDOR'].astype(str)
    
    return df_split

def crear_grafo(df_split):
    # (Tu código existente aquí)
    G = nx.Graph()
    routers = ['Router 1', 'Router 2', 'Router 3', 'Router 4', 'Router 5']

    for router in routers:
        G.add_node(router, tipo='Router')


    for index, row in df_split.iterrows():
        proveedor = row['PROVEEDOR']
        velocidad_bajada = row['VELOCIDAD_BAJADA']
        velocidad_subida = row['VELOCIDAD_SUBIDA']
        
        if pd.notna(velocidad_bajada) and pd.notna(velocidad_subida):
            for router in routers:
                peso = (velocidad_bajada + velocidad_subida) / 2
                G.add_edge(proveedor, router, weight=peso)

    return G

def grafo_view(request):
    cantidad_datos = 50 
    # Actualiza la ruta del archivo aquí
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, 'BDInternet.xlsx')
    
    df = cargar_datos(file_path, cantidad_datos)
    df_split = procesar_datos(df)
    G = crear_grafo(df_split)

    # Convertir el grafo a un formato JSON
    nodos = list(G.nodes())
    aristas = [{"source": u, "target": v, "weight": d['weight']} for u, v, d in G.edges(data=True)]

    return JsonResponse({"nodos": nodos, "aristas": aristas})

def index(request):
    return render(request, 'grafo_app/index.html')
