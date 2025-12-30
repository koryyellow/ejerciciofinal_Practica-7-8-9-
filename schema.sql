DROP DATABASE IF EXISTS tienda_online;
CREATE DATABASE tienda_online;
USE tienda_online;

-- =========================
-- CLIENTES
-- =========================
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    ciudad VARCHAR(50),
    telefono VARCHAR(20)
);

-- =========================
-- EMPLEADOS
-- =========================
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    puesto VARCHAR(50),
    correo VARCHAR(100),
    salario DECIMAL(10,2)
);

-- =========================
-- CATEGORÍAS
-- =========================
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion VARCHAR(150),
    activo BOOLEAN
);

-- =========================
-- PROVEEDORES
-- =========================
CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    ciudad VARCHAR(50)
);

-- =========================
-- PRODUCTOS
-- =========================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10,2),
    stock INT,
    id_categoria INT,
    id_proveedor INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

-- =========================
-- PEDIDOS
-- =========================
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    id_cliente INT,
    total DECIMAL(10,2),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- =========================
-- DETALLE_PEDIDO
-- =========================
CREATE TABLE detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- =========================
-- ENVIOS
-- =========================
CREATE TABLE envios (
    id_envio INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    empresa_envio VARCHAR(50),
    estado VARCHAR(30),
    fecha_envio DATE,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
);

-- =========================
-- INSERTS
-- =========================

INSERT INTO clientes (nombre, correo, ciudad, telefono) VALUES
('Ana López','ana@mail.com','CDMX','5511111111'),
('Luis Pérez','luis@mail.com','CDMX','5522222222'),
('María Gómez','maria@mail.com','Guadalajara','5533333333'),
('Carlos Ruiz','carlos@mail.com','Monterrey','5544444444'),
('Laura Torres','laura@mail.com','CDMX','5555555555');

INSERT INTO empleados (nombre, puesto, correo, salario) VALUES
('Pedro Martínez','Ventas','pedro@tienda.com',12000),
('Sofía Ramírez','Almacén','sofia@tienda.com',11000),
('Jorge Castillo','Soporte','jorge@tienda.com',10000);

INSERT INTO categorias (nombre, descripcion, activo) VALUES
('Electrónica','Dispositivos electrónicos',1),
('Ropa','Prendas de vestir',1),
('Hogar','Artículos del hogar',1);

INSERT INTO proveedores (nombre, contacto, telefono, ciudad) VALUES
('TechSupplier','Juan Tech','5512345678','CDMX'),
('ModaMX','Ana Moda','5598765432','Guadalajara'),
('CasaPlus','Carlos Hogar','5588888888','Monterrey');

INSERT INTO productos (nombre, precio, stock, id_categoria, id_proveedor) VALUES
('Laptop',15000,10,1,1),
('Smartphone',8000,15,1,1),
('Playera',300,50,2,2),
('Pantalón',700,40,2,2),
('Licuadora',1200,20,3,3);

INSERT INTO pedidos (fecha, id_cliente, total) VALUES
('2025-01-10',1,15800),
('2025-01-11',2,300),
('2025-01-12',3,1500),
('2025-01-13',1,8000),
('2025-01-14',4,700);

INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario) VALUES
(1,1,1,15000),
(1,3,1,300),
(2,3,1,300),
(3,5,1,1200),
(4,2,1,8000),
(5,4,1,700);

INSERT INTO envios (id_pedido, empresa_envio, estado, fecha_envio) VALUES
(1,'DHL','Enviado','2025-01-11'),
(2,'FedEx','Enviado','2025-01-12'),
(3,'Estafeta','Enviado','2025-01-13'),
(4,'DHL','Enviado','2025-01-14'),
(5,'FedEx','Enviado','2025-01-15');
