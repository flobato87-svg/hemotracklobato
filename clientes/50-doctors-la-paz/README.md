# HemoTrack · 50 Doctors La Paz

Proyecto de demostración y oferta de **HemoTrack 2** y de la **responsabilidad
sanitaria** del Servicio de Transfusión Sanguínea para la red hospitalaria
**50 Doctors**, unidad **La Paz, B.C.S.**

| | |
|---|---|
| Establecimiento | Hospital 50 Doctors La Paz (en desarrollo) |
| Domicilio | Blvd. Gral. Agustín Olachea 4600, María Conchita, C.P. 23098, La Paz, B.C.S. |
| Servicio | Servicio de Transfusión Sanguínea (nuevo) |
| Licencia sanitaria | **Sin licencia todavía.** En la demo aparece «EN TRÁMITE (DEMOSTRACIÓN)» |
| CLUES | Por asignar. En la demo aparece «EN TRÁMITE» |
| Responsable Sanitario propuesto | Dr. Felipe Lobato Ferreyra |
| Proveedor de hemocomponentes (demo) | C.E.T.S. Baja California Sur (padrón CNTS 03-01-1-001) |
| Estado | Preparando la demostración |

## Contenido

| Carpeta | Qué hay |
|---|---|
| [`perfil/`](perfil/) | `50doctors-la-paz-demo.hemotrack-perfil`: identidad, claves documentales y procedencia. Se carga en HemoTrack → Configuración → «Importar configuración…» |
| [`datos_demo/`](datos_demo/) | `sembrar_demo.py`: crea una base con el perfil, cuentas por rol y datos clínicos **ficticios** |
| [`logotipos/`](logotipos/) | Aquí van los logotipos de 50 Doctors (ver su LEEME) |
| [`demo/`](demo/) | Guion de la presentación, paso a paso |
| [`propuesta/`](propuesta/) | Borrador de la propuesta comercial |

## Preparar la computadora de la demo (Windows)

1. Copiar HemoTrack 2 **en una carpeta sólo para la demo** (nunca sobre una instalación en uso).
2. `python -m pip install -r requirements.txt` dentro de esa carpeta.
3. Si ya están los logotipos, dejarlos en `logotipos/` como `izquierdo.png` y `derecho.png`.
4. Uno o dos días antes de la presentación:
   ```powershell
   python clientes\50-doctors-la-paz\datos_demo\sembrar_demo.py --hemotrack "C:\HemoTrack-Demo"
   ```
   Imprime las contraseñas de las cinco cuentas (`flobato`, `quimico`, `medico`,
   `enfermeria`, `direccion`). Anotarlas: no se vuelven a mostrar.
5. `Abrir HemoTrack.bat` → «Es el único equipo del servicio» → entrar como `flobato`.

La base nueva queda en **evaluación de 30 días**, suficiente para la demo sin
emitir licencia. La licencia real se emite cuando exista el CLUES definitivo,
porque va atada a él.

## Datos por confirmar con 50 Doctors

- [ ] Razón social y denominación exacta del establecimiento (la demo usa «HOSPITAL 50 DOCTORS LA PAZ»)
- [ ] Logotipos en buena resolución (PNG, fondo transparente)
- [ ] Teléfono del hospital
- [ ] CLUES (cuando se asigne)
- [ ] Director(a) médico(a) — firma el formato C del CNTS
- [ ] Ubicación del servicio dentro del hospital
- [ ] Banco de sangre que surtirá (CETS BCS u otro) y convenio
- [ ] Su sistema de control documental, para sustituir las claves propuestas `50D-LPZ-STS-Fxx`

## Datos del Responsable Sanitario por completar

- [ ] Cédula profesional y de especialidad (no se capturaron; el membrete sale sin «Céd. Prof.» hasta que se agreguen en Configuración)

## Nota

Este repositorio es privado del titular. HemoTrack 2 no lleva datos de ningún
hospital en su código: todo lo de 50 Doctors vive aquí y entra al programa como
configuración.
