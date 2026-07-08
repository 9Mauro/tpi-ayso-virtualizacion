#!/usr/bin/env python3
"""
servidor.py
Trabajo Integrador - Arquitectura y Sistemas Operativos
Tema: Virtualizacion
Autor: Mauro Villanueva

Servidor web minimo basado en la libreria estandar de Python (http.server).
Pensado para ejecutarse dentro de una VM Ubuntu Server sobre VMware Workstation.
Sirve una pagina HTML de prueba y expone informacion basica del host invitado
para validar, desde el navegador del host fisico, que la maquina virtual esta
operativa y accesible por red (modo Bridged).
"""

import os
import socket
import platform
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"  # escucha en todas las interfaces de la VM
PUERTO_POR_DEFECTO = 8080


def limpiar_pantalla():
    """Limpia la consola de forma multiplataforma (Windows / Linux / macOS)."""
    os.system("cls" if os.name == "nt" else "clear")


def obtener_ip_local():
    """Devuelve la IP de la interfaz de red de la VM (la que ve el host)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No envia datos; solo fuerza la resolucion de la interfaz de salida.
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def construir_html(ip):
    """Arma la pagina HTML de respuesta con datos del host invitado."""
    marca = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Servidor Python en VM Ubuntu</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #222; }}
        h1 {{ color: #1a4c8b; }}
        table {{ border-collapse: collapse; margin-top: 20px; }}
        td {{ border: 1px solid #999; padding: 8px 14px; }}
        td.k {{ background: #f0f4f8; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Maquina virtual operativa</h1>
    <p>Este contenido se sirve desde un servidor Python ejecutado dentro
    de una VM Ubuntu Server sobre VMware Workstation 17 Player.</p>
    <table>
        <tr><td class="k">Sistema operativo</td><td>{platform.system()} {platform.release()}</td></tr>
        <tr><td class="k">Hostname</td><td>{socket.gethostname()}</td></tr>
        <tr><td class="k">IP de la VM</td><td>{ip}</td></tr>
        <tr><td class="k">Arquitectura</td><td>{platform.machine()}</td></tr>
        <tr><td class="k">Version de Python</td><td>{platform.python_version()}</td></tr>
        <tr><td class="k">Fecha y hora</td><td>{marca}</td></tr>
    </table>
    <p>Trabajo Integrador AYSO - Autor: Mauro Villanueva</p>
</body>
</html>"""


class Manejador(BaseHTTPRequestHandler):
    """Responde toda peticion GET con la pagina de prueba."""

    def do_GET(self):
        ip = obtener_ip_local()
        cuerpo = construir_html(ip).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, formato, *args):
        # Log limpio en consola: IP del cliente y recurso solicitado.
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"{self.client_address[0]} -> {args[0]}")


def pedir_puerto():
    """Solicita el puerto al usuario, validando el dato ingresado."""
    while True:
        entrada = input(f"\nPuerto de escucha [{PUERTO_POR_DEFECTO}]: ").strip()
        if entrada == "":
            return PUERTO_POR_DEFECTO
        if not entrada.isdigit():
            print("Error: ingrese solo numeros.")
            continue
        puerto = int(entrada)
        if not (1 <= puerto <= 65535):
            print("Error: el puerto debe estar entre 1 y 65535.")
            continue
        if puerto < 1024:
            print("Aviso: puertos menores a 1024 requieren privilegios de root.")
        return puerto


def iniciar_servidor(puerto):
    """Levanta el servidor y bloquea hasta Ctrl+C."""
    ip = obtener_ip_local()
    servidor = ThreadingHTTPServer((HOST, puerto), Manejador)
    print("\n" + "=" * 55)
    print("  SERVIDOR WEB PYTHON - VM UBUNTU")
    print("=" * 55)
    print(f"  Escuchando en   : {HOST}:{puerto}")
    print(f"  Acceso local    : http://127.0.0.1:{puerto}")
    print(f"  Acceso desde host: http://{ip}:{puerto}")
    print("=" * 55)
    print("  Presione Ctrl+C para detener el servidor.\n")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nDeteniendo servidor...")
    finally:
        servidor.server_close()
        print("Servidor detenido correctamente.")


def menu():
    """Menu principal con bucle permanente y opcion de salida."""
    while True:
        limpiar_pantalla()
        print("=" * 55)
        print("  TRABAJO INTEGRADOR AYSO - VIRTUALIZACION")
        print("  Servidor web Python en VM Ubuntu")
        print("  Autor: Mauro Villanueva")
        print("=" * 55)
        print("  1. Iniciar servidor web")
        print("  2. Mostrar IP de la VM")
        print("  3. Salir")
        print("=" * 55)

        opcion = input("Seleccione una opcion [1-3]: ").strip()

        if opcion == "1":
            puerto = pedir_puerto()
            iniciar_servidor(puerto)
            input("\nPresione ENTER para volver al menu...")
        elif opcion == "2":
            print(f"\nIP de la VM: {obtener_ip_local()}")
            input("\nPresione ENTER para volver al menu...")
        elif opcion == "3":
            print("\nSaliendo del programa. Hasta luego.")
            break
        else:
            print("\nOpcion invalida. Ingrese un numero del 1 al 3.")
            input("Presione ENTER para continuar...")


if __name__ == "__main__":
    menu()
