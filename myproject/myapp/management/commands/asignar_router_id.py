from django.core.management.base import BaseCommand
from myapp.models import Proveedor, Router

class Command(BaseCommand):
    help = 'Asigna el router_id a los proveedores basado en su departamento'

    def handle(self, *args, **kwargs):
        # Recuperar todos los routers
        routers = Router.objects.all()

        # Crear un diccionario para mapear departamentos a router_id
        departamento_router_map = {router.departamento: router.router_id for router in routers}

        # Recuperar todos los proveedores
        proveedores = Proveedor.objects.all()

        for proveedor in proveedores:
            departamento = proveedor.departamento  # Asegúrate de que este campo exista en tu modelo
            if departamento in departamento_router_map:
                try:
                    # Obtener la instancia del Router
                    router_instance = Router.objects.get(router_id=departamento_router_map[departamento])
                    proveedor.router = router_instance  # Asignar la instancia del Router
                    proveedor.save()  # Guardar el proveedor con el nuevo router
                    self.stdout.write(self.style.SUCCESS(f'Router ID {proveedor.router.router_id} asignado a {proveedor.empresa}'))
                except Router.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Router no encontrado para el ID: {departamento_router_map[departamento]}'))
            else:
                self.stdout.write(self.style.WARNING(f'No se encontró un router para el departamento: {departamento}'))

        self.stdout.write(self.style.SUCCESS('Asignación de router completada.'))