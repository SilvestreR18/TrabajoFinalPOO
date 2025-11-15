README REALIZADO con DEEPSEEK AI.
Alum. Pieres Rawson Paz, Silvestre.

# 🏪 Sistema de Gestión de Tienda - POO

## 📋 Tabla de Contenidos
1. [🚀 Ejecución de la Aplicación]
2. [🎯 Funcionamiento del Sistema]
3. [💻 Explicación del Código POO]
4. [📁 Estructura de Archivos]

---

## 🚀 Ejecución de la Aplicación

### Para Usuarios Finales (.exe):
1. **Descargar** el archivo `SistemaTienda.exe`
2. **Crear una carpeta vacía** y colocar el .exe ahí
3. **Ejecutar** el .exe (doble clic)
4. **Permitir** si el antivirus lo bloquea (falso positivo)
5. **¡Listo!** El sistema creará automáticamente todos los archivos necesarios

🔐 Credenciales de Acceso:
Administrador: usuario admin | contraseña admin

Clientes: Registrarse primero o usar ID personalizado

🎯 Funcionamiento del Sistema
Gestión de Productos:
├── ➕ Agregar nuevos productos
├── 🗑️ Eliminar productos del stock
├── 📋 Listar todos los productos
└── 💾 Persistencia automática en JSON

Gestión de Pedidos:
├── 📦 Ver todos los pedidos
├── 🔄 Cambiar estados (Sin hacer → En proceso → Enviado → Entregado)
├── 🏷️ Generar etiquetas de envío
└── 📊 Reportes y estadísticas

👤 Módulo Cliente
Flujo de Compra:
1. 🔐 Registro/Login con ID personalizado
2. 🛍️ Ver catálogo de productos
3. 🛒 Agregar productos al carrito
4. 📋 Revisar carrito y total
5. ✅ Finalizar compra → genera pedido
6. 📊 Consultar historial de pedidos

💾 Persistencia de Datos
El sistema maneja 4 archivos JSON automáticamente:

├── admins.json - Usuarios administradores
├── clientes.json - Clientes registrados
├── productos.json - Catálogo de productos
├── pedidos.json - Historial completo de pedidos

📁 Estructura de Archivos
SistemaTienda/
├── 🚀 SistemaTienda.exe          # Ejecutable principal
├── 📊 admins.json               # (Auto-generado) Usuarios admin
├── 👥 clientes.json             # (Auto-generado) Clientes registrados
├── 📦 productos.json            # (Auto-generado) Catálogo de productos
├── 📋 pedidos.json              # (Auto-generado) Historial de pedidos
├── 🏷️ etiqueta_PEDXXXX.txt      # (Auto-generado) Etiquetas de envío

└── 📄 README.md                 # Este archivo
