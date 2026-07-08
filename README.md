# Trabajo Integrador AYSO — Virtualización

Servidor web mínimo en Python ejecutado dentro de una máquina virtual Ubuntu Server sobre VMware Workstation 17 Player.

**Materia:** Arquitectura y Sistemas Operativos — Tecnicatura Universitaria en Programación a Distancia (UTN)
**Autor:** Mauro Villanueva
**Modalidad:** Individual

## Descripción

Este proyecto forma parte del Trabajo Integrador de la materia. Consiste en montar una máquina virtual con Linux sobre un hipervisor de tipo 2 (VMware Workstation) y ejecutar dentro de ella un servidor web desarrollado con la librería estándar de Python. El objetivo es validar la interacción entre el sistema anfitrión y el sistema invitado accediendo al servicio desde el navegador del host a través de la red local.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `servidor.py` | Servidor web basado en `http.server`. Sirve una página con datos del sistema invitado. |
| `README.md` | Guía del repositorio. |

## Requisitos

- Python 3.7 o superior (incluido de fábrica en Ubuntu Server 24.04).
- No requiere dependencias externas: usa únicamente la librería estándar.

## Entorno de prueba

- **Hipervisor:** VMware Workstation 17 Player
- **Sistema invitado:** Ubuntu Server 24.04 LTS
- **Recursos de la VM:** 4 GB de RAM, 20 GB de disco
- **Red:** modo Bridged (la VM obtiene IP propia en la red local)

## Uso

1. Clonar o descargar el repositorio dentro de la VM:

   ```bash
   git clone https://github.com/9Mauro/tpi-ayso-virtualizacion.git
   cd tpi-ayso-virtualizacion
   ```

2. (Opcional) Habilitar el puerto en el firewall del sistema invitado:

   ```bash
   sudo ufw allow 8080/tcp
   ```

3. Ejecutar el servidor:

   ```bash
   python3 servidor.py
   ```

4. En el menú, elegir la opción **1** (Iniciar servidor web) y confirmar el puerto (por defecto 8080).

5. Desde el navegador del equipo anfitrión, acceder a:

   ```
   http://IP-DE-LA-VM:8080
   ```

   La IP de la VM se obtiene dentro de la máquina virtual con el comando `ip a`.

## Funcionamiento

El servidor escucha en `0.0.0.0` para aceptar conexiones desde fuera de la VM. Ante cualquier petición GET responde con una página HTML que muestra datos del sistema invitado: sistema operativo, hostname, dirección IP, arquitectura, versión de Python y fecha y hora. Esto permite comprobar visualmente que el servicio corre dentro de la VM y es accesible desde el host.

## Autor

Mauro Villanueva — Tecnicatura Universitaria en Programación a Distancia (UTN)
