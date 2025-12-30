import mysql.connector
import os
from tabulate import tabulate

# =========================
# CONFIGURACIÓN BD
# =========================
db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "tienda_online")
}

def conectar():
    return mysql.connector.connect(**db_config)

# =========================
# CONSULTAS (20)
# =========================
consultas = {

    # =========================
    # OPERADORES BÁSICOS (5)
    # =========================
    1: {
        "tipo": "σ Selección",
        "descripcion": "Clientes de la ciudad de CDMX",
        "sql": """
            SELECT * FROM clientes
            WHERE ciudad = 'CDMX';
        """
    },
    2: {
        "tipo": "π Proyección",
        "descripcion": "Nombres y correos de clientes",
        "sql": """
            SELECT nombre, correo FROM clientes;
        """
    },
    3: {
        "tipo": "∪ Unión",
        "descripcion": "Personas que son clientes o empleados",
        "sql": """
            SELECT nombre FROM clientes
            UNION
            SELECT nombre FROM empleados;
        """
    },
    4: {
        "tipo": "∩ Intersección",
        "descripcion": "Personas que son clientes y empleados",
        "sql": """
            SELECT nombre FROM clientes
            INTERSECT
            SELECT nombre FROM empleados;
        """
    },
    5: {
        "tipo": "- Diferencia",
        "descripcion": "Clientes que no han realizado pedidos",
        "sql": """
            SELECT c.nombre
            FROM clientes c
            LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
            WHERE p.id_pedido IS NULL;
        """
    },

    # =========================
    # REUNIONES / JOINS (5)
    # =========================
    6: {
        "tipo": "⨝ Join",
        "descripcion": "Pedidos con el nombre del cliente",
        "sql": """
            SELECT p.id_pedido, c.nombre
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente;
        """
    },
    7: {
        "tipo": "⟕ Left Join",
        "descripcion": "Clientes y sus pedidos (si existen)",
        "sql": """
            SELECT c.nombre, p.id_pedido
            FROM clientes c
            LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente;
        """
    },
    8: {
        "tipo": "⟖ Right Join",
        "descripcion": "Productos y pedidos en los que aparecen",
        "sql": """
            SELECT pr.nombre, dp.id_pedido
            FROM productos pr
            LEFT JOIN detalle_pedido dp ON pr.id_producto = dp.id_producto;
        """
    },
    9: {
        "tipo": "⨝ Join",
        "descripcion": "Productos con su categoría",
        "sql": """
            SELECT pr.nombre, c.nombre AS categoria
            FROM productos pr
            JOIN categorias c ON pr.id_categoria = c.id_categoria;
        """
    },
    10: {
        "tipo": "⨝ Join",
        "descripcion": "Detalle de pedidos con nombre de producto",
        "sql": """
            SELECT dp.id_pedido, pr.nombre, dp.cantidad
            FROM detalle_pedido dp
            JOIN productos pr ON dp.id_producto = pr.id_producto;
        """
    },

    # =========================
    # AGRUPACIÓN Y AGREGACIÓN (5)
    # =========================
    11: {
        "tipo": "GROUP BY / COUNT",
        "descripcion": "Cantidad de pedidos por cliente",
        "sql": """
            SELECT c.nombre, COUNT(p.id_pedido) AS total_pedidos
            FROM clientes c
            JOIN pedidos p ON c.id_cliente = p.id_cliente
            GROUP BY c.nombre;
        """
    },
    12: {
        "tipo": "GROUP BY / SUM",
        "descripcion": "Total gastado por cliente",
        "sql": """
            SELECT c.nombre, SUM(dp.cantidad * dp.precio_unitario) AS total_gastado
            FROM clientes c
            JOIN pedidos p ON c.id_cliente = p.id_cliente
            JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            GROUP BY c.nombre;
        """
    },
    13: {
        "tipo": "GROUP BY / AVG",
        "descripcion": "Precio promedio de productos por categoría",
        "sql": """
            SELECT c.nombre, AVG(pr.precio) AS promedio
            FROM categorias c
            JOIN productos pr ON c.id_categoria = pr.id_categoria
            GROUP BY c.nombre;
        """
    },
    14: {
        "tipo": "HAVING",
        "descripcion": "Clientes con más de 3 pedidos",
        "sql": """
            SELECT c.nombre, COUNT(*) AS pedidos
            FROM clientes c
            JOIN pedidos p ON c.id_cliente = p.id_cliente
            GROUP BY c.nombre
            HAVING pedidos > 3;
        """
    },
    15: {
        "tipo": "MAX",
        "descripcion": "Producto más caro por categoría",
        "sql": """
            SELECT c.nombre, MAX(pr.precio) AS precio_max
            FROM categorias c
            JOIN productos pr ON c.id_categoria = pr.id_categoria
            GROUP BY c.nombre;
        """
    },

    # =========================
    # DIVISIÓN (3)
    # =========================
    16: {
        "tipo": "División",
        "descripcion": "Clientes que han comprado TODOS los productos de una categoría",
        "sql": """
            SELECT c.nombre
            FROM clientes c
            WHERE NOT EXISTS (
                SELECT pr.id_producto
                FROM productos pr
                WHERE pr.id_categoria = 1
                AND NOT EXISTS (
                    SELECT *
                    FROM pedidos p
                    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
                    WHERE p.id_cliente = c.id_cliente
                    AND dp.id_producto = pr.id_producto
                )
            );
        """
    },
    17: {
        "tipo": "División",
        "descripcion": "Proveedores que surten todos los productos que venden",
        "sql": """
            SELECT pr.nombre
            FROM proveedores pr
            WHERE NOT EXISTS (
                SELECT p.id_producto
                FROM productos p
                WHERE p.id_proveedor = pr.id_proveedor
                AND p.stock = 0
            );
        """
    },
    18: {
        "tipo": "División",
        "descripcion": "Clientes que han comprado todos los productos disponibles",
        "sql": """
            SELECT c.nombre
            FROM clientes c
            WHERE NOT EXISTS (
                SELECT p.id_producto
                FROM productos p
                AND NOT EXISTS (
                    SELECT *
                    FROM pedidos pe
                    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
                    WHERE pe.id_cliente = c.id_cliente
                    AND dp.id_producto = p.id_producto
                )
            );
        """
    },

    # =========================
    # CUANTIFICADORES UNIVERSALES (2)
    # =========================
    19: {
        "tipo": "∀ Para todo",
        "descripcion": "Productos que siempre se han vendido",
        "sql": """
            SELECT pr.nombre
            FROM productos pr
            WHERE NOT EXISTS (
                SELECT *
                FROM pedidos p
                WHERE NOT EXISTS (
                    SELECT *
                    FROM detalle_pedido dp
                    WHERE dp.id_pedido = p.id_pedido
                    AND dp.id_producto = pr.id_producto
                )
            );
        """
    },
    20: {
        "tipo": "∀ Para todo",
        "descripcion": "Clientes cuyos pedidos siempre han sido enviados",
        "sql": """
            SELECT c.nombre
            FROM clientes c
            WHERE NOT EXISTS (
                SELECT *
                FROM pedidos p
                JOIN envios e ON p.id_pedido = e.id_pedido
                WHERE p.id_cliente = c.id_cliente
                AND e.estado != 'Enviado'
            );
        """
    }
}

# =========================
# EJECUCIÓN
# =========================
def ejecutar(n):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(consultas[n]["sql"])
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()

    print("\nTipo:", consultas[n]["tipo"])
    print("Descripción:", consultas[n]["descripcion"], "\n")
    print(tabulate(rows, headers=cols, tablefmt="grid") if rows else "Sin resultados")

    cur.close()
    conn.close()

# =========================
# MENÚ
# =========================
def menu():
    while True:
        print("\n===== MENÚ DE CONSULTAS – TIENDA EN LÍNEA =====")
        for k in consultas:
            print(f"{k}. [{consultas[k]['tipo']}] {consultas[k]['descripcion']}")
        print("0. Salir")

        op = input("Seleccione una opción: ")

        if op == "0":
            break
        if op.isdigit() and int(op) in consultas:
            ejecutar(int(op))
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
