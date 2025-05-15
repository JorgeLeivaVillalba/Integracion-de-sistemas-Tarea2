# TAREA 2: Integración de Servicios mediante API REST

## Instalacion

1. Corre el script creardb.py para crear la base de datos.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Instancia de Telco: `python -m telco.main`
4. Instancia de Banco: `python -m banco.main`

## Objetivo general

Desarrollar dos servicios RESTful utilizando FastAPI, simulando la interacción entre un banco y una empresa de telefonía (Telco) para la gestión de pagos de facturas. Ambas APIs deberán compartir una base de datos SQLite para fines académicos (lo pueden hacer igualmente en 2 base de datos independientes).

## 🔄 Flujo de Datos y Operaciones

### Consulta de deuda por parte del usuario

1. El usuario accede a la API del Banco para consultar su deuda mediante el método `consultar_deuda(ci)`.
2. Esta API internamente invoca a la API de la Telco usando el mismo método `consultar_deuda(ci)` para consultar facturas pendientes del cliente.

### Respuesta de la Telco

- La API de la Telco accede a la tabla **FacturaPendientes** y devuelve las facturas impagas asociadas al ci.

### Pago de deuda

1. El usuario solicita pagar una factura a través de la API del Banco, invocando `pagar_deuda(nro_factura, monto, nro_cuenta)`.

2. El servicio del Banco realiza las siguientes validaciones:
   - El saldo en la cuenta (**CuentaDebito**) debe ser mayor o igual al monto solicitado.
   - El monto a pagar no debe superar el saldo pendiente de la factura.
   - El número de cuenta debe existir en la base.

### Pago en Telco

1. Si las validaciones son exitosas, el Banco invoca `pagar_deuda(nro_factura, monto)` en la API de la Telco.

2. La Telco valida que:
   - La factura exista.
   - Se reste correctamente el saldoPendiente de la factura en la tabla **FacturaPendientes**.

### Confirmación del pago

- Si la Telco responde con código HTTP 200 OK, el Banco registra el pago en la tabla **PagosServicios**, incluyendo fecha, id_cuenta_debito, monto y nro_factura.

### Manejo de errores

- Toda validación o error en el flujo debe ser manejado apropiadamente con mensajes claros y retornos HTTP (400, 404, 422, etc.).
- El sistema debe imprimir en pantalla los errores en caso de validaciones no exitosas (por ejemplo, saldo insuficiente, factura inexistente, etc.).

## 🧾 Modelo de Datos

### Tabla: Clientes
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria (PK) |
| nombre | TEXT | |
| apellido | TEXT | |
| ci | TEXT | Único |

### Tabla: CuentaDebito
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria (PK) |
| cliente_id | INTEGER | Clave foránea (FK → Clientes.id) |
| nro_cuenta | TEXT | |
| saldo | REAL | |

### Tabla: FacturaPendientes
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria (PK) |
| cliente_id | INTEGER | Clave foránea (FK → Clientes.id) |
| nrofactura | TEXT | |
| saldoPendiente | REAL | |

### Tabla: PagosServicios
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria (PK) |
| fecha | TEXT | Formato ISO 8601 |
| id_cuenta_debito | INTEGER | Clave foránea (FK → CuentaDebito.id) |
| monto | REAL | |
| nro_factura | TEXT | |