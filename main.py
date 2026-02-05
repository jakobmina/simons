#!/usr/bin/env python3
import argparse
import sys
import os
import pytest

# Importar funcionalidades directamente para evitar subprocess
try:
    from simons_complete import main as run_simon
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from simons_complete import main as run_simon

try:
    from simon_h7_holography import run_holography
except ImportError:
    def run_holography():
        print("❌ Error: Módulo simon_h7_holography no encontrado.")

def run_algorithm():
    """Ejecuta el algoritmo de Simon H7 completo."""
    print("\n🚀 Iniciando Algoritmo de Simon H7...")
    try:
        run_simon()
    except Exception as e:
        print(f"\n❌ Error al ejecutar el algoritmo: {e}")
        sys.exit(1)

def run_viz():
    """Genera la visualización holográfica unificada."""
    print("\n🌌 Generando Visualización Holográfica H7...")
    try:
        run_holography()
        print("\n✨ Visualización completada.")
        print("🔗 Abre Simon_H7_Holografia_Interactiva.html para ver los resultados.")
    except Exception as e:
        print(f"\n❌ Error al generar la visualización: {e}")
        sys.exit(1)

def run_tests():
    """Ejecuta la suite de pruebas Pytest."""
    print("\n🧪 Ejecutando pruebas de validación H7...")
    # Ejecutar pytest directamente desde Python
    retcode = pytest.main(["tests/test_simons.py"])
    sys.exit(retcode)

def show_cs():
    """Muestra el código de referencia en C#."""
    print("\n📋 Código de Referencia C# (AndroidHtmlUi):")
    try:
        # Intentar encontrar el archivo en el mismo directorio que este script
        base_path = os.path.dirname(os.path.abspath(__file__))
        cs_path = os.path.join(base_path, "simon_h7_interface.cs")
        with open(cs_path, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("❌ Archivo simon_h7_interface.cs no encontrado.")

def run_tripartite():
    """Ejecuta la simulación del Proceso Tripartito."""
    print("\n🧬 Iniciando Proceso Tripartito (2da Cuantización)...")
    try:
        from simon_tripartite import TripartiteMetriplecticSystem
        sys_tri = TripartiteMetriplecticSystem(input_val=7)
        res = sys_tri.run_tripartite_task()
        print(f"   -> Estado Estable: {'✅ SÍ' if res.is_stable else '❌ NO (DECOHERENCIA)'}")
        print(f"   -> Fase de Berry Acumulada: {res.berry_phase:.6f}")
        print(f"   -> Lagrangiano: L_symp={res.l_symp:.4f}, L_metr={res.l_metr:.4f}")
    except Exception as e:
        print(f"❌ Error en el Proceso Tripartito: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="CLI Central para el Proyecto Simon H7 - Mandato Metriplético",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s run          # Ejecuta el experimento completo
  %(prog)s viz          # Genera la holografía interactiva
  %(prog)s tripartite   # Ejecuta el proceso tripartito (hilos)
  %(prog)s test         # Ejecuta validaciones automatizadas
  %(prog)s show         # Muestra código C# de referencia
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    subparsers.add_parser("run", help="Ejecutar Algoritmo Simon H7")
    subparsers.add_parser("viz", help="Generar Visualización Holográfica")
    subparsers.add_parser("tripartite", help="Ejecutar Proceso Tripartito")
    subparsers.add_parser("test", help="Ejecutar Suite de Pruebas")
    subparsers.add_parser("show", help="Mostrar referencia C#")
    
    args = parser.parse_args()
    
    if args.command == "run":
        run_algorithm()
    elif args.command == "viz":
        run_viz()
    elif args.command == "tripartite":
        run_tripartite()
    elif args.command == "test":
        run_tests()
    elif args.command == "show":
        show_cs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
