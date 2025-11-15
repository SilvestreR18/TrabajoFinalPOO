import json
import os
import random
from datetime import datetime

# ==================== CLASES POO ====================
class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(Usuario):
    def __init__(self, username, password):
        super().__init__(username, password)

class Cliente(Usuario):
    def __init__(self, nombre, apellido, direccion, cp, id_personalizado):
        id_temp = f"CLI{id_personalizado}"
        super().__init__(id_temp, "")
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.cp = cp
        self.carrito = []
        self.id_personalizado = id_personalizado

class Producto:
    def __init__(self, id, nombre, precio, stock, categoria):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

class Pedido:
    ESTADOS = ["Sin hacer", "En proceso", "Enviado", "Entregado", "No pagó"]
    
    def __init__(self, cliente, productos):
        self.id = f"PED{random.randint(1000, 9999)}"
        self.cliente = cliente
        self.productos = productos
        self.estado = "Sin hacer"
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.total = sum(producto.precio for producto in productos)

# ==================== GESTORES ====================
class AdminManager:
    def __init__(self):
        self.archivo = "admins.json"
        self.admins = self.cargar_admins()
    
    def cargar_admins(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                return json.load(f)
        else:
            admins_default = [{"username": "admin", "password": "admin"}]
            self.guardar_admins(admins_default)
            return admins_default
    
    def guardar_admins(self, admins):
        with open(self.archivo, 'w') as f:
            json.dump(admins, f, indent=4)
    
    def verificar_login(self, username, password):
        for admin in self.admins:
            if admin["username"] == username and admin["password"] == password:
                return True
        return False

class ClienteManager:
    def __init__(self):
        self.archivo = "clientes.json"
        self.clientes = []
        self.cargar_clientes()
    
    def cargar_clientes(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                for cliente_data in datos:
                    cliente = Cliente(
                        cliente_data["nombre"],
                        cliente_data["apellido"],
                        cliente_data["direccion"],
                        cliente_data["cp"],
                        cliente_data["id_personalizado"]
                    )
                    self.clientes.append(cliente)
    
    def guardar_clientes(self):
        datos = []
        for cliente in self.clientes:
            datos.append({
                "username": cliente.username,
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "direccion": cliente.direccion,
                "cp": cliente.cp,
                "id_personalizado": cliente.id_personalizado
            })
        with open(self.archivo, 'w') as f:
            json.dump(datos, f, indent=4)
    
    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.guardar_clientes()
    
    def buscar_por_id(self, id_personalizado):
        for cliente in self.clientes:
            if cliente.id_personalizado == id_personalizado:
                return cliente
        return None

class ProductoManager:
    def __init__(self):
        self.archivo = "productos.json"
        self.productos = []
        self.cargar_productos()
    
    def cargar_productos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                self.productos = [Producto(item["id"], item["nombre"], item["precio"], item["stock"], item["categoria"]) for item in datos]
        else:
            self.crear_productos_ejemplo()
    
    def crear_productos_ejemplo(self):
        self.productos = [
            Producto("PROD001", "Arroz", 1200, 50, "Alimentos"),
            Producto("PROD002", "Aceite", 1800, 30, "Alimentos"),
            Producto("PROD003", "Jabón", 800, 100, "Limpieza"),
            Producto("PROD004", "Shampoo", 2200, 40, "Higiene")
        ]
        self.guardar_productos()
    
    def guardar_productos(self):
        datos = []
        for prod in self.productos:
            datos.append({
                "id": prod.id,
                "nombre": prod.nombre,
                "precio": prod.precio,
                "stock": prod.stock,
                "categoria": prod.categoria
            })
        with open(self.archivo, 'w') as f:
            json.dump(datos, f, indent=4)
    
    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_productos()
    
    def eliminar_producto(self, id_producto):
        self.productos = [p for p in self.productos if p.id != id_producto]
        self.guardar_productos()

class PedidoManager:
    def __init__(self):
        self.archivo = "pedidos.json"
        self.pedidos = []
        self.cargar_pedidos()
    
    def cargar_pedidos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                datos_pedidos = json.load(f)
                for pedido_data in datos_pedidos:
                    try:
                        # Reconstruir cliente - MANEJO DE VERSIONES ANTIGUAS
                        cliente_data = pedido_data["cliente"]
                        
                        # Si es un pedido antiguo, generar ID personalizado automático
                        if "id_personalizado" not in cliente_data:
                            id_personalizado = cliente_data.get("id", "0000")[-4:]  # Tomar últimos 4 dígitos
                        else:
                            id_personalizado = cliente_data["id_personalizado"]
                        
                        cliente = Cliente(
                            cliente_data["nombre"], 
                            cliente_data["apellido"], 
                            cliente_data["direccion"], 
                            cliente_data["cp"],
                            id_personalizado
                        )
                        cliente.username = cliente_data.get("username", f"CLI{id_personalizado}")
                        
                        # Reconstruir productos
                        productos = []
                        for prod_data in pedido_data["productos"]:
                            producto = Producto(
                                prod_data["id"], 
                                prod_data["nombre"], 
                                prod_data["precio"], 
                                prod_data["stock"], 
                                prod_data["categoria"]
                            )
                            productos.append(producto)
                        
                        # Crear pedido
                        pedido = Pedido(cliente, productos)
                        pedido.id = pedido_data["id"]
                        pedido.estado = pedido_data["estado"]
                        pedido.fecha = pedido_data["fecha"]
                        pedido.total = pedido_data["total"]
                        
                        self.pedidos.append(pedido)
                    except Exception as e:
                        print(f"  Error cargando pedido {pedido_data.get('id', 'DESCONOCIDO')}: {e}")
                        continue
    
    def guardar_pedidos(self):
        datos_pedidos = []
        for pedido in self.pedidos:
            # Convertir productos a diccionarios
            productos_data = []
            for producto in pedido.productos:
                productos_data.append({
                    "id": producto.id,
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "categoria": producto.categoria
                })
            
            # Convertir pedido a diccionario
            pedido_data = {
                "id": pedido.id,
                "cliente": {
                    "username": pedido.cliente.username,
                    "nombre": pedido.cliente.nombre,
                    "apellido": pedido.cliente.apellido,
                    "direccion": pedido.cliente.direccion,
                    "cp": pedido.cliente.cp,
                    "id_personalizado": pedido.cliente.id_personalizado
                },
                "productos": productos_data,
                "estado": pedido.estado,
                "fecha": pedido.fecha,
                "total": pedido.total
            }
            datos_pedidos.append(pedido_data)
        
        # Guardar en archivo
        with open(self.archivo, 'w') as f:
            json.dump(datos_pedidos, f, indent=4)
    
    def agregar_pedido(self, pedido):
        self.pedidos.append(pedido)
        self.guardar_pedidos()
    
    def obtener_pedidos_cliente(self, cliente):
        return [pedido for pedido in self.pedidos if pedido.cliente.username == cliente.username]

# ==================== SISTEMA PRINCIPAL ====================
class SistemaTienda:
    def __init__(self):
        self.admin_manager = AdminManager()
        self.cliente_manager = ClienteManager()
        self.producto_manager = ProductoManager()
        self.pedido_manager = PedidoManager()
        self.cliente_actual = None
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausa(self):
        input("\nPresiona Enter para continuar...")
    
    def login_admin(self):
        self.limpiar_pantalla()
        print("=== LOGIN ADMINISTRADOR ===")
        username = input("Usuario: ")
        password = input("Contraseña: ")
        
        if self.admin_manager.verificar_login(username, password):
            print(" Login exitoso!")
            self.pausa()
            self.menu_admin()
        else:
            print(" Credenciales incorrectas")
            self.pausa()
    
    def registro_cliente(self):
        self.limpiar_pantalla()
        print("=== REGISTRO CLIENTE ===")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        direccion = input("Direccion: ")
        cp = input("Codigo Postal: ")
        
        # ID personalizado de 4 dígitos
        while True:
            id_personalizado = input("Elige tu ID personalizado (4 dígitos): ")
            if len(id_personalizado) == 4 and id_personalizado.isdigit():
                # Verificar si ya existe
                if self.cliente_manager.buscar_por_id(id_personalizado):
                    print(" Este ID ya esta en uso. Elige otro.")
                else:
                    break
            else:
                print(" El ID debe tener exactamente 4 digitos numericos.")
        
        self.cliente_actual = Cliente(nombre, apellido, direccion, cp, id_personalizado)
        self.cliente_manager.agregar_cliente(self.cliente_actual)
        print(f" Registro exitoso!")
        print(f" Tu ID de cliente: {id_personalizado}")
        print(f" Guardalo para futuros accesos")
        self.pausa()
        self.menu_cliente()
    
    def login_cliente(self):
        self.limpiar_pantalla()
        print("=== LOGIN CLIENTE ===")
        id_personalizado = input("Ingresa tu ID personalizado (4 digitos): ")
        
        cliente = self.cliente_manager.buscar_por_id(id_personalizado)
        if cliente:
            self.cliente_actual = cliente
            print(f" Bienvenido de nuevo, {cliente.nombre}!")
            self.pausa()
            self.menu_cliente()
        else:
            print(" ID no encontrado. ¿Quieres registrarte?")
            self.pausa()
    
    def menu_admin(self):
        while True:
            self.limpiar_pantalla()
            print(" PANEL ADMINISTRADOR")
            print("1.  Gestion de Productos")
            print("2.  Gestion de Pedidos") 
            print("3.  Volver")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                self.menu_gestion_productos()
            elif opcion == "2":
                self.menu_gestion_pedidos()
            elif opcion == "3":
                break
            else:
                print(" Opcion invalida")
                self.pausa()
    
    def menu_gestion_productos(self):
        while True:
            self.limpiar_pantalla()
            print(" GESTION DE PRODUCTOS")
            print("1.  Agregar Producto")
            print("2.  Eliminar Producto") 
            print("3.  Listar Productos")
            print("4.  Volver")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                self.agregar_producto()
            elif opcion == "2":
                self.eliminar_producto()
            elif opcion == "3":
                self.listar_productos()
                self.pausa()
            elif opcion == "4":
                break
            else:
                print(" Opcion invalida")
                self.pausa()
    
    def agregar_producto(self):
        self.limpiar_pantalla()
        print(" AGREGAR PRODUCTO")
        id = f"PROD{random.randint(1000, 9999)}"
        nombre = input("Nombre: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        categoria = input("Categoría: ")
        
        nuevo_producto = Producto(id, nombre, precio, stock, categoria)
        self.producto_manager.agregar_producto(nuevo_producto)
        print(f" Producto {nombre} agregado!")
        self.pausa()
    
    def eliminar_producto(self):
        self.limpiar_pantalla()
        print(" ELIMINAR PRODUCTO")
        self.listar_productos()
        
        id_producto = input("ID a eliminar: ")
        self.producto_manager.eliminar_producto(id_producto)
        print(" Producto eliminado!")
        self.pausa()
    
    def listar_productos(self):
        print("\n PRODUCTOS:")
        for producto in self.producto_manager.productos:
            print(f"  {producto.id} | {producto.nombre} | ${producto.precio} | Stock: {producto.stock}")
    
    def menu_gestion_pedidos(self):
        while True:
            self.limpiar_pantalla()
            print(" GESTIÓN DE PEDIDOS")
            print("1.  Ver Pedidos")
            print("2.  Cambiar Estado")
            print("3.  Generar Etiqueta")
            print("4.  Volver")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                self.ver_pedidos()
            elif opcion == "2":
                self.cambiar_estado_pedido()
            elif opcion == "3":
                self.generar_etiqueta()
            elif opcion == "4":
                break
            else:
                print(" Opcion invalida")
                self.pausa()
    
    def ver_pedidos(self):
        self.limpiar_pantalla()
        print(" PEDIDOS:")
        if not self.pedido_manager.pedidos:
            print("  No hay pedidos registrados")
        else:
            for pedido in self.pedido_manager.pedidos:
                print(f"  {pedido.id} | {pedido.cliente.nombre} | Estado: {pedido.estado} | Total: ${pedido.total}")
        self.pausa()
    
    def cambiar_estado_pedido(self):
        self.limpiar_pantalla()
        self.ver_pedidos()
        
        if not self.pedido_manager.pedidos:
            self.pausa()
            return
            
        id_pedido = input("ID del pedido: ")
        print("Estados: 1-Sin hacer, 2-En proceso, 3-Enviado, 4-Entregado, 5-No pago")
        
        opcion = input("Nuevo estado (1-5): ")
        estados = ["Sin hacer", "En proceso", "Enviado", "Entregado", "No pago"]
        
        if opcion in ["1","2","3","4","5"]:
            for pedido in self.pedido_manager.pedidos:
                if pedido.id == id_pedido:
                    pedido.estado = estados[int(opcion)-1]
                    self.pedido_manager.guardar_pedidos()
                    print(" Estado actualizado!")
                    break
        else:
            print(" Estado invalido")
        self.pausa()
    
    def generar_etiqueta(self):
        self.limpiar_pantalla()
        self.ver_pedidos()
        
        if not self.pedido_manager.pedidos:
            self.pausa()
            return
            
        id_pedido = input("ID del pedido: ")
        
        for pedido in self.pedido_manager.pedidos:
            if pedido.id == id_pedido:
                etiqueta = f"""
ETIQUETA DE ENVIO
=================
CLIENTE: {pedido.cliente.nombre} {pedido.cliente.apellido}
DIRECCION: {pedido.cliente.direccion}
CODIGO POSTAL: {pedido.cliente.cp}
-----------------
PEDIDO: {pedido.id}
FECHA: {pedido.fecha}
ESTADO: {pedido.estado}
TOTAL: ${pedido.total}
=================
"""
                print(etiqueta)
                
                with open(f"etiqueta_{id_pedido}.txt", "w") as f:
                    f.write(etiqueta)
                print(" Etiqueta guardada exitosamente!")
                break
        self.pausa()
    
    def menu_cliente(self):
        while True:
            self.limpiar_pantalla()
            print(f" CLIENTE: {self.cliente_actual.nombre}")
            print("1.  Ver Productos")
            print("2.  Agregar al Carrito") 
            print("3.  Ver Carrito")
            print("4.  Finalizar Compra")
            print("5.  Mis Pedidos")
            print("6.  Volver")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                self.ver_productos_cliente()
            elif opcion == "2":
                self.agregar_al_carrito()
            elif opcion == "3":
                self.ver_carrito()
            elif opcion == "4":
                self.finalizar_compra()
            elif opcion == "5":
                self.ver_mis_pedidos()
            elif opcion == "6":
                break
            else:
                print("Opcion invalida")
                self.pausa()
    
    def ver_mis_pedidos(self):
        self.limpiar_pantalla()
        print("MIS PEDIDOS")
        
        mis_pedidos = self.pedido_manager.obtener_pedidos_cliente(self.cliente_actual)
        
        if not mis_pedidos:
            print(" No tienes pedidos registrados")
        else:
            for pedido in mis_pedidos:
                print(f"\n Pedido: {pedido.id}")
                print(f"Fecha: {pedido.fecha}")
                print(f"Estado: {pedido.estado}")
                print(f"Total: ${pedido.total}")
                print("Productos:")
                for producto in pedido.productos:
                    print(f"   - {producto.nombre} (${producto.precio})")
                print("-" * 30)
        
        self.pausa()
    
    def ver_productos_cliente(self):
        self.limpiar_pantalla()
        print("PRODUCTOS:")
        self.listar_productos()
        self.pausa()
    
    def agregar_al_carrito(self):
        self.limpiar_pantalla()
        print("AGREGAR AL CARRITO")
        self.listar_productos()
        
        id_producto = input("ID de producto: ")
        
        for producto in self.producto_manager.productos:
            if producto.id == id_producto:
                self.cliente_actual.carrito.append(producto)
                print(f"{producto.nombre} agregado!")
                break
        self.pausa()
    
    def ver_carrito(self):
        self.limpiar_pantalla()
        print("CARRITO:")
        if not self.cliente_actual.carrito:
            print("Carrito vacio")
        else:
            total = 0
            for producto in self.cliente_actual.carrito:
                print(f"  {producto.nombre} - ${producto.precio}")
                total += producto.precio
            print(f"Total: ${total}")
        self.pausa()
    
    def finalizar_compra(self):
        self.limpiar_pantalla()
        if not self.cliente_actual.carrito:
            print("Carrito vacio")
            self.pausa()
            return
        
        self.ver_carrito()
        confirmar = input("Confirmar compra? (s/n): ")
        
        if confirmar.lower() == 's':
            try:
                pedido = Pedido(self.cliente_actual, self.cliente_actual.carrito.copy())
                self.pedido_manager.agregar_pedido(pedido)
                self.cliente_actual.carrito.clear()
                print(f"Compra exitosa! Pedido: {pedido.id}")
            except Exception as e:
                print(f"Error al procesar compra: {e}")
        else:
            print("Compra cancelada")
        self.pausa()
    
    def menu_principal(self):
        while True:
            self.limpiar_pantalla()
            print("SISTEMA DE TIENDA")
            print("1. Administrador")
            print("2. Cliente Nuevo")
            print("3. Cliente Existente")
            print("4. Salir")
            
            opcion = input("Selecciona: ")
            
            if opcion == "1":
                self.login_admin()
            elif opcion == "2":
                self.registro_cliente()
            elif opcion == "3":
                self.login_cliente()
            elif opcion == "4":
                print("Saliendo del sistema...")
                break
            else:
                print("Opcion invalida")
                self.pausa()

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    sistema = SistemaTienda()
    sistema.menu_principal()