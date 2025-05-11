import sqlite3
import datetime

# Crear o conectar a la base de datos
conn = sqlite3.connect('banco_telco.db')
cursor = conn.cursor()

# Crear tablas

# Tabla Clientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    ci TEXT UNIQUE NOT NULL
)
''')

# Tabla CuentaDebito
cursor.execute('''
CREATE TABLE IF NOT EXISTS CuentaDebito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    nro_cuenta TEXT NOT NULL,
    saldo REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
)
''')

# Tabla FacturaPendientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS FacturaPendientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    nrofactura TEXT NOT NULL,
    saldoPendiente REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
)
''')

# Tabla PagosServicios
cursor.execute('''
CREATE TABLE IF NOT EXISTS PagosServicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    id_cuenta_debito INTEGER NOT NULL,
    monto REAL NOT NULL,
    nro_factura TEXT NOT NULL,
    FOREIGN KEY (id_cuenta_debito) REFERENCES CuentaDebito(id)
)
''')

# Insertar datos de prueba

# Insertar clientes
clientes = [
    ("Juan", "Pérez", "1234567"),
    ("María", "González", "2345678"),
    ("Carlos", "Rodríguez", "3456789")
]

cursor.executemany("INSERT INTO Clientes (nombre, apellido, ci) VALUES (?, ?, ?)", clientes)

# Insertar cuentas de débito
cuentas = [
    (1, "100-1", 5000.0),  # Cuenta para Juan Pérez
    (2, "100-2", 3000.0),  # Cuenta para María González
    (3, "100-3", 2000.0)   # Cuenta para Carlos Rodríguez
]

cursor.executemany("INSERT INTO CuentaDebito (cliente_id, nro_cuenta, saldo) VALUES (?, ?, ?)", cuentas)

# Insertar facturas pendientes
facturas = [
    (1, "F-001", 1500.0),  # Factura para Juan Pérez
    (1, "F-002", 800.0),   # Otra factura para Juan Pérez
    (2, "F-003", 1200.0),  # Factura para María González
    (3, "F-004", 500.0)    # Factura para Carlos Rodríguez
]

cursor.executemany("INSERT INTO FacturaPendientes (cliente_id, nrofactura, saldoPendiente) VALUES (?, ?, ?)", facturas)

# Insertar un pago de ejemplo
fecha_actual = datetime.datetime.now().isoformat()
pagos = [
    (fecha_actual, 1, 500.0, "F-001")  # Pago parcial de la factura F-001 por Juan Pérez
]

cursor.executemany("INSERT INTO PagosServicios (fecha, id_cuenta_debito, monto, nro_factura) VALUES (?, ?, ?, ?)", pagos)

# Guardar cambios y cerrar conexión
conn.commit()
print("Base de datos creada exitosamente con datos de prueba.")

# Verificar datos insertados
print("\nClientes:")
cursor.execute("SELECT * FROM Clientes")
for row in cursor.fetchall():
    print(row)

print("\nCuentas de Débito:")
cursor.execute("SELECT * FROM CuentaDebito")
for row in cursor.fetchall():
    print(row)

print("\nFacturas Pendientes:")
cursor.execute("SELECT * FROM FacturaPendientes")
for row in cursor.fetchall():
    print(row)

print("\nPagos de Servicios:")
cursor.execute("SELECT * FROM PagosServicios")
for row in cursor.fetchall():
    print(row)

conn.close()