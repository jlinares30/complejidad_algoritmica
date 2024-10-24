import csv
from django.core.management.base import BaseCommand
from myapp.models import Proveedor, Router
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Importa datos desde un archivo CSV a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('conexiones.csv', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['conexiones.csv']
        print(f"Intentando abrir el archivo: {csv_file}")
        print(f"Ruta del archivo: {csv_file}")

        with open(csv_file, newline='', encoding='latin-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            print(f"Encabezados del CSV: {reader.fieldnames}")
            
            departamentos_procesados = {}

            for row in reader:
                departamento = row.get('departamento', 'No disponible')
                print(f"Departamento: {departamento}")
                
                conexiones_str = row['conexiones'].replace(',', '') 
                conexiones = int(conexiones_str)  
                Proveedor.objects.create(
                    empresa=row['empresa'],
                    tecnologia=row['tecnologia'],
                    segmento=row['segmento'],
                    departamento=departamento,
                    velocidad=row['velocidad'],
                    conexiones=conexiones
                )

                # Crear un router por cada departamento único
                if departamento not in departamentos_procesados:
                    nombre_router = f"router_{departamento.lower().replace(' ', '_')}"
                    try:
                        Router.objects.create(
                            departamento=departamento,
                            nombre=nombre_router
                        )
                        departamentos_procesados[departamento] = True
                    except IntegrityError:
                        print(f"El router para el departamento {departamento} ya existe.")
        
        self.stdout.write(self.style.SUCCESS('Proveedores y routers importados correctamente'))
