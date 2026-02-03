"""Mini-Sistema de Tienda Online
Demuestra: clases, herencia, polimorfismo, encapsulación, type hints, dataclasses.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


# =========================
# 1) DATACLASS: Producto
# =========================
@dataclass(slots=True, eq=False)
class Producto:
    """Representa un producto en la tienda."""

    codigo: str
    nombre: str
    precio: float
    stock: int = 0

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"

    def __eq__(self, other: object) -> bool:
        """Compara productos por código."""
        if not isinstance(other, Producto):
            return NotImplemented
        return self.codigo == other.codigo

    def __lt__(self, other: Producto) -> bool:
        """Permite comparar por precio."""
        return self.precio < other.precio


# =========================
# 2) CLASE BASE: Usuario
# =========================
class Usuario:
    """Clase base para usuarios del sistema."""

    _contador_usuarios: int = 1  # Atributo de clase (compartido)

    def __init__(self, nombre: str, email: str) -> None:
        self.nombre: str = nombre
        self.email: str = email
        self.id_usuario: int = Usuario._contador_usuarios
        Usuario._contador_usuarios += 1
        self.__historial_compras: list[str] = []  # Encapsulado (name mangling)

    def __str__(self) -> str:
        return f"{self.nombre} <{self.email}> (ID: {self.id_usuario})"

    def agregar_a_historial(self, producto_nombre: str) -> None:
        """Método protegido para agregar compra al historial."""
        self.__historial_compras.append(producto_nombre)

    @property
    def historial(self) -> list[str]:
        """Propiedad para acceder al historial de compras."""
        return self.__historial_compras.copy()

    def realizar_compra(self, producto: Producto) -> None:
        """Polimorfismo: las subclases pueden sobrescribir este método."""
        print(f"⚠️  Método base (no implementado para {self.__class__.__name__})")


# =========================
# 3) HERENCIA: Cliente y Admin
# =========================
class Cliente(Usuario):
    """Usuario cliente con límite de descuento."""

    def __init__(self, nombre: str, email: str, descuento_base: float = 0.0) -> None:
        super().__init__(nombre, email)
        self.descuento_base: float = descuento_base
        self.__dinero_gastado: float = 0.0  # Encapsulado

    @property
    def dinero_gastado(self) -> float:
        return self.__dinero_gastado

    def realizar_compra(self, producto: Producto) -> None:
        """Polimorfismo: sobrescribe el método base."""
        if producto.stock <= 0:
            print(f"❌ {self.nombre}: No hay stock de {producto.nombre}")
            return
        
        descuento = producto.precio * self.descuento_base
        precio_final = producto.precio - descuento
        self.__dinero_gastado += precio_final
        producto.stock -= 1
        self.agregar_a_historial(producto.nombre)
        
        print(f"✅ {self.nombre} compró {producto.nombre} por ${precio_final:.2f}")


class Admin(Usuario):
    """Usuario administrador con permisos especiales."""

    def __init__(self, nombre: str, email: str, departamento: str) -> None:
        super().__init__(nombre, email)
        self.departamento: str = departamento

    def realizar_compra(self, producto: Producto) -> None:
        """Polimorfismo: admins compran sin descuento pero aparecen en auditoría."""
        if producto.stock <= 0:
            print(f"❌ {self.nombre} (Admin): No hay stock de {producto.nombre}")
            return
        
        producto.stock -= 1
        self.agregar_a_historial(f"{producto.nombre} (compra admin)")
        print(f"✅ {self.nombre} (Departamento: {self.departamento}) compró {producto.nombre}")

    def reponer_stock(self, producto: Producto, cantidad: int) -> None:
        """Método exclusivo del admin: reponer stock."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        producto.stock += cantidad
        print(f"📦 {self.nombre} reponió {cantidad} unidades de {producto.nombre}")


# =========================
# 4) CLASE: Tienda
# =========================
class Tienda:
    """Gestiona productos y usuarios de la tienda."""

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []

    def __len__(self) -> int:
        """Retorna la cantidad de productos en la tienda."""
        return len(self._productos)

    def __str__(self) -> str:
        return f"Tienda: {self.nombre} ({len(self._productos)} productos, {len(self._usuarios)} usuarios)"

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto al catálogo (sin duplicados)."""
        if any(p.codigo == producto.codigo for p in self._productos):
            raise ValueError(f"Ya existe un producto con código {producto.codigo}")
        self._productos.append(producto)
        print(f"➕ Producto agregado: {producto.nombre}")

    def registrar_usuario(self, usuario: Usuario) -> None:
        """Registra un nuevo usuario en la tienda."""
        self._usuarios.append(usuario)
        print(f"👤 Usuario registrado: {usuario.nombre}")

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """Busca un producto por código."""
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def listar_productos(self) -> None:
        """Lista todos los productos disponibles."""
        print(f"\n📚 Catálogo de {self.nombre}:")
        if not self._productos:
            print("  (sin productos)")
            return
        for producto in sorted(self._productos):  # Usa __lt__ para ordenar por precio
            print(f"  {producto}")

    def listar_usuarios(self) -> None:
        """Lista todos los usuarios registrados."""
        print(f"\n👥 Usuarios de {self.nombre}:")
        if not self._usuarios:
            print("  (sin usuarios)")
            return
        for usuario in self._usuarios:
            print(f"  {usuario}")


# =========================
# 5) DEMOSTRACIÓN
# =========================
def main() -> None:
    print("=" * 60)
    print("DEMO: Mini-Sistema de Tienda Online")
    print("=" * 60)

    # Crear tienda
    tienda = Tienda("Tech Store")

    # Crear productos
    laptop = Producto("P001", "Laptop", 800.0, stock=5)
    mouse = Producto("P002", "Mouse", 25.0, stock=20)
    teclado = Producto("P003", "Teclado", 60.0, stock=10)

    tienda.agregar_producto(laptop)
    tienda.agregar_producto(mouse)
    tienda.agregar_producto(teclado)

    # Crear usuarios
    cliente1 = Cliente("Ana", "ana@email.com", descuento_base=0.1)  # 10% de descuento
    cliente2 = Cliente("Juan", "juan@email.com", descuento_base=0.05)  # 5% de descuento
    admin = Admin("Laura", "laura@email.com", "Inventario")

    tienda.registrar_usuario(cliente1)
    tienda.registrar_usuario(cliente2)
    tienda.registrar_usuario(admin)

    # Listar antes
    tienda.listar_productos()
    tienda.listar_usuarios()

    # -------- Compras (Polimorfismo) --------
    print("\n" + "=" * 60)
    print("COMPRAS:")
    print("=" * 60)

    cliente1.realizar_compra(laptop)  # Con descuento
    cliente2.realizar_compra(mouse)
    cliente1.realizar_compra(mouse)
    admin.realizar_compra(teclado)  # Sin descuento

    # -------- Admin repone stock --------
    print("\n" + "=" * 60)
    print("REPOSICIÓN DE STOCK:")
    print("=" * 60)

    admin.reponer_stock(laptop, 3)

    # -------- Resumen final --------
    print("\n" + "=" * 60)
    print("ESTADO FINAL:")
    print("=" * 60)

    tienda.listar_productos()

    print(f"\n💰 Dinero gastado por {cliente1.nombre}: ${cliente1.dinero_gastado:.2f}")
    print(f"🛒 Historial de {cliente1.nombre}: {cliente1.historial}")

    print(f"\n📋 Cantidad de productos en tienda: {len(tienda)}")
    print(f"📊 {tienda}")


if __name__ == "__main__":
    main()
