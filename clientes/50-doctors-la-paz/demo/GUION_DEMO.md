# Guion de la demostración · Fifty Doctors Hospital La Paz

Duración sugerida: 30–40 minutos. Base: la que crea `datos_demo/sembrar_demo.py`
(todos los pacientes empiezan con «DEMO» y los expedientes con `50D-`).

## 0. Antes de empezar (5 min antes)

- Abrir HemoTrack y entrar como `flobato` (Responsable Sanitario).
- Tener a la mano las contraseñas de `quimico` y `enfermeria` para cambiar de rol.
- Impresora o visor de PDF listo.

## 1. El problema que resolvemos (3 min, sin pantalla)

- Un servicio de transfusión nuevo tiene que nacer cumpliendo la NOM-253-SSA1-2012:
  trazabilidad vena a vena, hemovigilancia, informe mensual al CNTS e indicadores.
- Fifty Doctors Hospital La Paz necesita además un Responsable Sanitario para tramitar su
  licencia. La oferta es **las dos cosas juntas**: el responsable y el sistema
  con el que él mismo responde.

## 2. Identidad del hospital (2 min)

- **Configuración → Establecimiento**: denominación, domicilio de Blvd. Agustín
  Olachea, responsable sanitario. Licencia y CLUES aparecen «EN TRÁMITE».
- Mensaje clave: *el sistema ya está configurado para ustedes; el día que llegue
  la licencia se captura y todos los formatos la imprimen.*

## 3. Panel (2 min)

- Existencias por grupo y componente, reservas vigentes y **dos unidades por caducar**.

## 4. Flujo transfusional completo (10 min)

1. **Pacientes y solicitudes** → abrir `50D-000107` (artroplastia de cadera, AB+).
2. **Compatibilidades** → ya tiene dos CE cruzados. Mostrar que un cruce
   ABO-incompatible **se bloquea** (intentar cruzar un CE A+ a un paciente O+, p. ej. `50D-000111`).
3. **Transfusiones** → registrar la transfusión de una unidad reservada, con
   signos vitales pre y post. Imprimir la **nota transfusional** y la **hoja de
   control postransfusional** (membrete de 50 Doctors).
4. **Código rojo / urgencia vital** → liberación sin pruebas completas, auditada
   a nombre de quien la libera.

## 5. Trazabilidad (3 min)

- Buscar el paciente `50D-000101` (hemorragia obstétrica): tres unidades,
  de qué donación vienen, quién cruzó, quién transfundió y cuándo.
- Buscar un folio de unidad y mostrar su recorrido desde la recepción del CETS.

## 6. Hemovigilancia (5 min)

- Hay una **reacción febril no hemolítica** notificada por enfermería
  (paciente `50D-000102`).
- Entrar como Responsable: investigar, clasificar gravedad e imputabilidad,
  cerrar y **firmar** con contraseña. Mostrar la bitácora de hemovigilancia.

## 7. Reportes, informe CNTS e indicadores (5 min)

- **Reportes** → libro de transfusiones del mes.
- **Informe mensual al CNTS** (formatos oficiales CNTS-01-003-B y C).
- **Indicadores de calidad** y cierre mensual.

## 8. Seguridad y operación (3 min)

- Cuentas por rol (químico, médico, enfermería, consulta para Dirección) y
  bitácora de auditoría.
- Respaldo automático al arrancar; varios equipos con un Servidor HemoTrack.
- Funciona **sin internet**: la licencia se verifica en el propio equipo.

## 9. Cierre (5 min)

- Qué incluye la propuesta (ver `propuesta/`), calendario hacia la licencia
  sanitaria y siguiente paso: reunión con Dirección Médica y Jurídico.

## Si algo falla

- Si pide cambiar contraseña o no deja entrar: `Restablecer acceso.bat`.
- Si la base se ensucia durante un ensayo: borrar `hemotrack.db` de la carpeta
  de la demo y volver a correr `sembrar_demo.py`.
