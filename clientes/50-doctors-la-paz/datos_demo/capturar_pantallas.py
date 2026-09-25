# Toma capturas de HemoTrack 2 sin pantalla (Qt offscreen) usando la base de la demo.
# Uso: python capturar_pantallas.py <carpeta con demo.db> [vistas...]  (TRAZA=<folio> añade trazabilidad)
# Requiere HemoTrack-2 en /home/user/HemoTrack-2; ajuste la ruta si está en otro lugar.
import os, sys, sqlite3
os.environ["QT_QPA_PLATFORM"] = "offscreen"
sys.path.insert(0, "/home/user/HemoTrack-2")
S = sys.argv[1]
import database
database.DB_PATH = os.path.join(S, "demo.db")
from PySide6.QtWidgets import QApplication
app = QApplication([])
import qt_tema as t
app.setStyleSheet(t.hoja_mensajes())
import seguridad
con = sqlite3.connect(database.DB_PATH)
uid, usuario, nombre, rol = con.execute("SELECT id, usuario, nombre_completo, rol FROM Usuarios WHERE usuario='flobato'").fetchone()
seguridad.sesion.iniciar(uid, usuario, nombre, rol)
import qt_app
v = qt_app.VentanaPrincipal()
v.resize(1600, 1000)
v.show()
from PySide6.QtTest import QTest
def esperar():
    QTest.qWait(2500)
vistas = sys.argv[2:] or ["panel", "pacientes", "cruces", "transfusiones", "inventario", "trazabilidad", "rat", "reportes", "indicadores", "configuracion", "usuarios", "tipaje", "recepcion"]
for clave in vistas:
    try:
        v.barra._navegar(clave) if hasattr(v.barra, "_navegar") else v._navegar(clave)
    except Exception as e:
        print("error", clave, e); continue
    esperar()
    v.grab().save(os.path.join(S, "capturas", f"{clave}.png"))
    print("ok", clave)
if os.environ.get("TRAZA"):
    v.barra._navegar("trazabilidad"); esperar()
    vt = v.vistas["trazabilidad"]
    vt.rastrear_unidad(os.environ["TRAZA"]); esperar()
    v.grab().save(os.path.join(S, "capturas", "traza_unidad.png"))
    vt.e_paciente.setText("50D-000101"); vt.rastrear_paciente(); vt.pestanas.setCurrentIndex(1); esperar()
    v.grab().save(os.path.join(S, "capturas", "traza_paciente.png"))
    print("ok traza")
