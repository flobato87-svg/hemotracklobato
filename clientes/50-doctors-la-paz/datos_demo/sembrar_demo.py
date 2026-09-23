"""
sembrar_demo.py — Base de DEMOSTRACIÓN de HemoTrack para 50 Doctors La Paz.

Crea una base nueva con:

* la identidad de 50 Doctors La Paz (perfil ../perfil/*.hemotrack-perfil);
* cuentas de demostración, una por rol;
* pacientes, unidades, compatibilidades y transfusiones FICTICIOS, repartidos en
  los últimos días para que Panel, Trazabilidad, Reportes, Hemovigilancia e
  Indicadores tengan qué mostrar.

Todos los nombres, expedientes y folios son inventados. Esta base NO es para
operar: sólo para la presentación comercial.

Uso (en la computadora de la demo, con HemoTrack 2 ya instalado en modo fuente):

    python sembrar_demo.py --hemotrack "C:\\ruta\\HemoTrack-2"

Deja `hemotrack.db` dentro de la carpeta de HemoTrack. Si ya existe una base
ahí, se detiene sin tocarla: úsese una carpeta de HemoTrack sólo para la demo.
Conviene correrlo uno o dos días antes de la presentación: una base nueva da
30 días de evaluación, que es lo que dura la demo sin licencia instalada.
"""

import argparse
import datetime
import os
import random
import secrets
import sqlite3
import string
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PERFIL = os.path.join(AQUI, "..", "perfil", "50doctors-la-paz-demo.hemotrack-perfil")
LOGOTIPOS = os.path.join(AQUI, "..", "logotipos")

PROCEDENCIA = "03-01-1-001"          # CETS Baja California Sur (padrón CNTS)
USUARIO_QUIMICO = "Q.F.B. Ana Karen Demo Ruiz"

# usuario, nombre, rol (constante de seguridad), cédula
CUENTAS = (
    ("flobato", "Dr. Felipe Lobato Ferreyra", "ROL_RESPONSABLE", ""),
    ("quimico", USUARIO_QUIMICO, "ROL_QUIMICO", ""),
    ("medico", "Dra. Sofía Demo Castro", "ROL_MEDICO", ""),
    ("enfermeria", "Lic. Enf. Jorge Demo Amador", "ROL_ENFERMERIA", ""),
    ("direccion", "Dirección Médica (consulta)", "ROL_CONSULTA", ""),
)

# expediente, nombre, nacimiento, sexo, ABO, Rh, diagnóstico, servicio, médico
PACIENTES = (
    ("50D-000101", "DEMO GARCIA LUCERO MARIA FERNANDA", "1988-04-12", "F", "O", "+",
     "HEMORRAGIA OBSTETRICA POSPARTO", "GINECOOBSTETRICIA / 204", "DRA. SOFIA DEMO CASTRO"),
    ("50D-000102", "DEMO AGUNDEZ COTA JOSE LUIS", "1961-09-30", "M", "A", "+",
     "SANGRADO DE TUBO DIGESTIVO ALTO", "MEDICINA INTERNA / 312", "DR. RAUL DEMO VERDUGO"),
    ("50D-000103", "DEMO MURILLO GERALDO ANA PAULA", "1975-01-18", "F", "B", "+",
     "LEUCEMIA MIELOIDE AGUDA EN QUIMIOTERAPIA", "ONCOLOGIA / 405", "DR. RAUL DEMO VERDUGO"),
    ("50D-000104", "DEMO OSUNA MENDOZA CARLOS ALBERTO", "1992-07-03", "M", "O", "-",
     "POLITRAUMATISMO POR ACCIDENTE VIAL", "URGENCIAS / CHOQUE 1", "DRA. SOFIA DEMO CASTRO"),
    ("50D-000105", "DEMO CESEÑA LIERA ROSA ELENA", "1949-11-22", "F", "A", "+",
     "ANEMIA CRONICA SINTOMATICA, ERC", "MEDICINA INTERNA / 318", "DR. RAUL DEMO VERDUGO"),
    ("50D-000106", "DEMO ARCE BELTRAN MIGUEL ANGEL", "1958-03-05", "M", "O", "+",
     "REVASCULARIZACION CORONARIA PROGRAMADA", "CIRUGIA CARDIOVASCULAR / UCI 3", "DR. ERNESTO DEMO LUCERO"),
    ("50D-000107", "DEMO VILLAVICENCIO PAEZ LAURA", "1983-06-27", "F", "AB", "+",
     "ARTROPLASTIA TOTAL DE CADERA", "ORTOPEDIA / 220", "DR. ERNESTO DEMO LUCERO"),
    ("50D-000108", "DEMO GERALDO SANDEZ PEDRO", "1970-12-09", "M", "B", "-",
     "CIRROSIS HEPATICA CON COAGULOPATIA", "UCI / 5", "DRA. SOFIA DEMO CASTRO"),
    ("50D-000109", "DEMO RUBIO AMADOR VALERIA", "2019-02-14", "F", "O", "+",
     "DENGUE GRAVE CON TROMBOCITOPENIA", "PEDIATRIA / 110", "DRA. SOFIA DEMO CASTRO"),
    ("50D-000110", "DEMO LUCERO FIOL ALEJANDRO", "1966-08-01", "M", "A", "-",
     "COLECTOMIA POR CANCER DE COLON", "CIRUGIA GENERAL / 230", "DR. ERNESTO DEMO LUCERO"),
    ("50D-000111", "DEMO COTA AGUNDEZ ISABEL", "1995-10-10", "F", "O", "+",
     "EMBARAZO DE 38 SEMANAS, CESAREA PROGRAMADA", "GINECOOBSTETRICIA / 208", "DRA. SOFIA DEMO CASTRO"),
    ("50D-000112", "DEMO MENDOZA ARCE RAMON", "1952-05-19", "M", "O", "+",
     "SINDROME MIELODISPLASICO", "HEMATOLOGIA / 402", "DR. RAUL DEMO VERDUGO"),
)

CE = "Concentrado Eritrocitario"
PFC = "Plasma Fresco Congelado"
CP = "Concentrado Plaquetario"
PQA = "Plaquetoaféresis"
CRIO = "Crioprecipitado"

# tipo, (días de vigencia desde hoy), volumen
VIGENCIA = {CE: (42, 280), PFC: (365, 220), CP: (5, 50), PQA: (5, 250), CRIO: (365, 15)}

# Inventario: (tipo, ABO, Rh, cantidad)
INVENTARIO = (
    (CE, "O", "+", 14), (CE, "O", "-", 4), (CE, "A", "+", 8), (CE, "A", "-", 2),
    (CE, "B", "+", 4), (CE, "B", "-", 1), (CE, "AB", "+", 2),
    (PFC, "O", "+", 6), (PFC, "A", "+", 5), (PFC, "B", "+", 3), (PFC, "AB", "+", 3),
    (CP, "O", "+", 6), (CP, "A", "+", 4), (PQA, "O", "+", 2), (PQA, "A", "+", 1),
    (CRIO, "O", "+", 4), (CRIO, "A", "+", 2),
)

# Transfusiones ya hechas: (expediente, tipo, días atrás)
TRANSFUSIONES = (
    ("50D-000101", CE, 18), ("50D-000101", CE, 18), ("50D-000101", PFC, 18),
    ("50D-000102", CE, 15), ("50D-000102", CE, 14),
    ("50D-000103", CP, 13), ("50D-000103", CE, 11), ("50D-000103", PQA, 6),
    ("50D-000104", CE, 10), ("50D-000104", CE, 10), ("50D-000104", PFC, 10),
    ("50D-000105", CE, 8),
    ("50D-000106", CE, 7), ("50D-000106", PFC, 7), ("50D-000106", CRIO, 7),
    ("50D-000108", PFC, 5), ("50D-000108", PFC, 5),
    ("50D-000109", CP, 3), ("50D-000109", CP, 2),
    ("50D-000112", CE, 1),
)

# Compatibilidades vigentes (reserva para hoy): (expediente, tipo)
RESERVAS = (("50D-000107", CE), ("50D-000107", CE), ("50D-000110", CE),
            ("50D-000111", CE), ("50D-000111", CE))


def _contrasena():
    """Contraseña aleatoria que cumple la política de HemoTrack."""
    base = [secrets.choice(string.ascii_uppercase), secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits), secrets.choice("#$%&*+-?")]
    base += [secrets.choice(string.ascii_letters + string.digits) for _ in range(8)]
    random.SystemRandom().shuffle(base)
    return "".join(base)


def _grupo_rh(abo, rh):
    return f"{abo} {'Positivo (+)' if rh == '+' else 'Negativo (-)'}"


def _compatible_eritrocitos(abo_p, rh_p, abo_u, rh_u):
    abo_ok = {"O": {"O"}, "A": {"A", "O"}, "B": {"B", "O"}, "AB": {"AB", "A", "B", "O"}}
    return abo_u in abo_ok[abo_p] and (rh_p == "+" or rh_u == "-")


def _compatible_plasma(abo_p, abo_u):
    ok = {"O": {"O", "A", "B", "AB"}, "A": {"A", "AB"}, "B": {"B", "AB"}, "AB": {"AB"}}
    return abo_u in ok[abo_p]


def _ok(resultado, que):
    exito, mensaje = resultado[0], resultado[1]
    if not exito:
        sys.exit(f"No se pudo {que}: {mensaje}")
    return resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hemotrack", required=True,
                        help="Carpeta de HemoTrack 2 (la que tiene qt_app.py)")
    parser.add_argument("--base", help="Ruta de la base a crear "
                        "(por omisión, hemotrack.db dentro de la carpeta de HemoTrack)")
    args = parser.parse_args()

    carpeta = os.path.abspath(args.hemotrack)
    if not os.path.exists(os.path.join(carpeta, "qt_app.py")):
        sys.exit(f"{carpeta} no parece la carpeta de HemoTrack 2 (falta qt_app.py).")
    destino = os.path.abspath(args.base or os.path.join(carpeta, "hemotrack.db"))
    if os.path.exists(destino):
        sys.exit(f"Ya existe {destino}. No se toca: muévala o use otra carpeta para la demo.")

    sys.path.insert(0, carpeta)
    import database
    import perfil
    import seguridad
    import usuarios_db

    database.DB_PATH = destino
    database.inicializar_db()

    # 1. Identidad, claves documentales y procedencia.
    datos_perfil = perfil.leer(PERFIL)
    for posicion in ("izquierdo", "derecho"):
        ruta = os.path.join(LOGOTIPOS, f"{posicion}.png")
        if os.path.exists(ruta):
            import base64
            with open(ruta, "rb") as f:
                datos_perfil["logos"][posicion] = base64.b64encode(f.read()).decode("ascii")
    ok, mensajes = perfil.importar(datos_perfil)
    if not ok:
        sys.exit("No se pudo aplicar el perfil:\n" + "\n".join(mensajes))

    # 2. Cuentas de demostración.
    credenciales = []
    for usuario, nombre, rol, cedula in CUENTAS:
        clave = _contrasena()
        _ok(usuarios_db.crear_usuario(usuario, nombre, getattr(seguridad, rol), clave,
                                      cedula_profesional=cedula or None,
                                      debe_cambiar=False), f"crear la cuenta {usuario}")
        credenciales.append((usuario, nombre, clave))

    # 3. Pacientes.
    for exp, nombre, nac, sexo, abo, rh, dx, servicio, medico in PACIENTES:
        _ok(database.registrar_paciente_db(
            expediente=exp, nombre_completo=nombre, fecha_nacimiento=nac, sexo=sexo,
            grupo_rh=_grupo_rh(abo, rh), diagnostico=dx, servicio_cama=servicio,
            cirugia_programada="Sí" if "PROGRAMADA" in dx or "ARTROPLASTIA" in dx
            or "COLECTOMIA" in dx else "No",
            fecha_cirugia="", medico_indica=medico, req_ce=2), f"registrar a {exp}")

    # 4. Inventario recibido del CETS.
    hoy = datetime.date.today()
    unidades = []          # (folio, tipo, abo, rh)
    folio = 2650101
    for tipo, abo, rh, cantidad in INVENTARIO:
        dias, volumen = VIGENCIA[tipo]
        for i in range(cantidad):
            folio += 1
            atras = 1 + i % 3 if dias <= 5 else 3 + i % 4
            extraccion = hoy - datetime.timedelta(days=atras)
            caducidad = extraccion + datetime.timedelta(days=dias)
            _ok(database.registrar_hemocomponente_db(
                str(folio), tipo, abo, rh, caducidad.isoformat(), volumen,
                extraccion.isoformat(), "DONADOR ALTRUISTA", procedencia=PROCEDENCIA),
                f"registrar la unidad {folio}")
            unidades.append((str(folio), tipo, abo, rh))
    # Dos unidades por caducar, para que el Panel tenga una alerta que mostrar.
    for tipo, abo, rh, dias in ((CE, "O", "+", 2), (CP, "A", "+", 1)):
        folio += 1
        _ok(database.registrar_hemocomponente_db(
            str(folio), tipo, abo, rh, (hoy + datetime.timedelta(days=dias)).isoformat(),
            VIGENCIA[tipo][1], (hoy - datetime.timedelta(days=30)).isoformat(),
            "DONADOR ALTRUISTA", procedencia=PROCEDENCIA), f"registrar la unidad {folio}")
        unidades.append((str(folio), tipo, abo, rh))

    pacientes = {p[0]: p for p in PACIENTES}
    ids = {p["expediente"]: p["id"] for p in
           (dict(zip(("id", "expediente"), fila)) for fila in
            sqlite3.connect(destino).execute("SELECT id, expediente FROM Pacientes"))}
    usadas = set()

    def tomar_unidad(exp, tipo):
        _e, _n, _f, _s, abo_p, rh_p = pacientes[exp][:6]
        candidatas = sorted(unidades, key=lambda u: u[2] != abo_p)
        for u in candidatas:
            f, t, abo_u, rh_u = u
            if f in usadas or t != tipo:
                continue
            if tipo == CE and not _compatible_eritrocitos(abo_p, rh_p, abo_u, rh_u):
                continue
            if tipo in (PFC, CRIO) and not _compatible_plasma(abo_p, abo_u):
                continue
            # Plaquetas: ABO idéntico si hay; si no, cualquiera (el cruce pide confirmarlo).
            if tipo in (CP, PQA) and rh_p == "-" and rh_u == "+":
                continue
            usadas.add(f)
            return f
        sys.exit(f"No hay unidad de {tipo} compatible para {exp} en el inventario de demo.")

    def cruzar(exp, tipo):
        f = tomar_unidad(exp, tipo)
        _ok(database.registrar_cruce_db(ids[exp], f, "SI COMPATIBLE", USUARIO_QUIMICO,
                                        confirmar_advertencias=True), f"cruzar {f} con {exp}")
        return f

    # 5. Transfusiones ya realizadas, fechadas en los días anteriores.
    fechados = []
    for exp, tipo, dias in TRANSFUSIONES:
        f = cruzar(exp, tipo)
        _ok(database.registrar_transfusion_db(
            exp, f, {"ta": "118/74", "fc": "82", "temp": "36.6"},
            {"ta": "120/76", "fc": "80", "temp": "36.7"}, 0,
            "Transfusión sin incidentes. Datos de demostración.", USUARIO_QUIMICO),
            f"transfundir {f} a {exp}")
        fechados.append((f, dias))

    con = sqlite3.connect(destino)
    for f, dias in fechados:
        cuando = datetime.datetime.combine(hoy - datetime.timedelta(days=dias),
                                           datetime.time(8 + dias % 10, 15))
        uid = con.execute("SELECT id FROM Hemocomponentes WHERE id_isbt128 = ?", (f,)).fetchone()[0]
        con.execute("UPDATE Transfusiones SET fecha_hora_inicio = ?, fecha_hora_termino = ? "
                    "WHERE unidad_id = ?",
                    (cuando.strftime("%Y-%m-%d %H:%M:%S"),
                     (cuando + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"), uid))
        con.execute("UPDATE Cruces SET fecha_hora_cruce = ? WHERE unidad_id = ?",
                    ((cuando - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), uid))
    con.commit()

    # 6. Una sospecha de reacción febril, para mostrar Hemovigilancia.
    fila = con.execute(
        "SELECT T.id FROM Transfusiones T JOIN Pacientes P ON P.id = T.paciente_id "
        "WHERE P.expediente = '50D-000102' ORDER BY T.id LIMIT 1").fetchone()
    con.close()
    _ok(database.registrar_reaccion_db(
        fila[0], "Inmunológicas inmediatas", "Febril no hemolítica",
        minutos_desde_inicio=40, signos="Temperatura 38.4 °C, escalofríos",
        acciones="Se suspendió la transfusión y se notificó al banco de sangre",
        observaciones="Caso de demostración", usuario_responsable="Lic. Enf. Jorge Demo Amador",
        suspendio_transfusion=True), "notificar la reacción de demostración")

    # 7. Reservas vigentes para hoy (Compatibilidades y Panel).
    for exp, tipo in RESERVAS:
        cruzar(exp, tipo)

    print(f"\nBase de demostración creada: {destino}\n")
    print(f"  {len(PACIENTES)} pacientes, {len(unidades)} unidades, "
          f"{len(TRANSFUSIONES)} transfusiones, {len(RESERVAS)} reservas, 1 RAT\n")
    print("Cuentas (guárdelas; no se vuelven a mostrar):")
    for usuario, nombre, clave in credenciales:
        print(f"  {usuario:<11} {clave:<14} {nombre}")
    print("\nTodos los datos clínicos son ficticios.")


if __name__ == "__main__":
    main()
