#!/usr/bin/env python3
import argparse
import sys
import subprocess
import os

def run_algorithm():
    """Ejecuta el algoritmo de Simon H7 completo."""
    print("\n🚀 Iniciando Algoritmo de Simon H7...")
    result = subprocess.run([sys.executable, "simons_complete.py"], check=False)
    if result.returncode != 0:
        print("\n❌ Error al ejecutar el algoritmo.")
    sys.exit(result.returncode)

def run_viz():
    """Genera la visualización holográfica unificada."""
    print("\n🌌 Generando Visualización Holográfica H7...")
    result = subprocess.run([sys.executable, "simon_h7_holography.py"], check=False)
    if result.returncode == 0:
        print("\n✨ Visualización completada.")
        print("🔗 Abre Simon_H7_Holografia_Interactiva.html para ver los resultados.")
    else:
        print("\n❌ Error al generar la visualización.")
    sys.exit(result.returncode)

def run_tests():
    """Ejecuta la suite de pruebas Pytest."""
    print("\n🧪 Ejecutando pruebas de validación H7...")
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_simons.py"], env=env, check=False)
    sys.exit(result.returncode)

def show_cs():
    """Muestra el código de referencia en C#."""
    print("\n📋 Código de Referencia C# (AndroidHtmlUi):")
    try:
        with open("simon_h7_interface.cs", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("❌ Archivo simon_h7_interface.cs no encontrado.")

def main():
    parser = argparse.ArgumentParser(
        description="CLI Central para el Proyecto Simon H7 - Mandato Metriplético",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s run    # Ejecuta el experimento completo
  %(prog)s viz    # Genera la holografía interactiva
  %(prog)s test   # Ejecuta validaciones automatizadas
  %(prog)s show   # Muestra código C# de referencia
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    subparsers.add_parser("run", help="Ejecutar Algoritmo Simon H7")
    subparsers.add_parser("viz", help="Generar Visualización Holográfica")
    subparsers.add_parser("test", help="Ejecutar Suite de Pruebas")
    subparsers.add_parser("show", help="Mostrar referencia C#")
    
    args = parser.parse_args()
    
    if args.command == "run":
        run_algorithm()
    elif args.command == "viz":
        run_viz()
    elif args.command == "test":
        run_tests()
    elif args.command == "show":
        show_cs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
