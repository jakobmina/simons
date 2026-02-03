"""
EJEMPLOS PRÁCTICOS: Algoritmo de Simon Cuántico Mejorado

Este archivo muestra diferentes formas de usar el sistema:
1. Lista fija (números primos)
2. Distribución aleatoria
3. Secuencia periódica
4. Barrido de parámetros
"""

import numpy as np
import pandas as pd
from simon_complete import (
    experimento_simon_mejorado,
    AnalizadorSimetriaDinamica
)


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO 1: NÚMEROS PRIMOS (Estructura Alta)
# ═══════════════════════════════════════════════════════════════════════════

def ejemplo_1_numeros_primos():
    """
    Usa números primos como 'dado simulado'.
    
    Ventaja: Alta correlación interna, estructura matemática clara
    Expectativa: Pesos dinámicos más uniformes, mejor recuperación
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Números Primos (Estructura Alta)")
    print("="*80)
    
    # Lista de números primos (estructura altamente no aleatoria)
    lista_n = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    resultados = experimento_simon_mejorado(
        lista_n=lista_n,
        periodo_oculto=5,      # Queremos recuperar s = 5
        n_bits=4,              # 4 qubits = 16 estados
        num_mediciones=25
    )
    
    # Análisis adicional
    df = pd.DataFrame(resultados['analisis_simetria'])
    print(f"\n[ESTADÍSTICAS DE PESOS]")
    print(f"  Media de pesos: {df['peso_dinamico'].mean():.4f}")
    print(f"  Desv. Est.:     {df['peso_dinamico'].std():.4f}")
    print(f"  Min/Max:        {df['peso_dinamico'].min():.4f} / {df['peso_dinamico'].max():.4f}")
    
    print(f"\n[RESULTADO]")
    print(f"  Período encontrado: {resultados['periodo_estimado']}")
    print(f"  Período real:       {resultados['periodo_oculto']}")
    print(f"  Éxito: {'✓' if resultados['exito'] else '✗'}")
    print(f"  Confianza: {resultados['confianza']:.2%}")
    
    return resultados


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO 2: NÚMEROS ALEATORIOS (Estructura Baja)
# ═══════════════════════════════════════════════════════════════════════════

def ejemplo_2_numeros_aleatorios():
    """
    Usa números aleatorios como 'dado simulado'.
    
    Ventaja: Diversidad máxima
    Desventaja: Poca estructura interna, rendimiento variable
    Expectativa: Pesos dinámicos más dispersos
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Números Aleatorios (Estructura Baja)")
    print("="*80)
    
    # Números completamente aleatorios
    np.random.seed(42)
    lista_n = np.random.randint(1, 100, 15).tolist()
    
    print(f"\nLista aleatoria: {lista_n}")
    
    resultados = experimento_simon_mejorado(
        lista_n=lista_n,
        periodo_oculto=7,
        n_bits=4,
        num_mediciones=25
    )
    
    df = pd.DataFrame(resultados['analisis_simetria'])
    print(f"\n[ESTADÍSTICAS DE PESOS]")
    print(f"  Media de pesos: {df['peso_dinamico'].mean():.4f}")
    print(f"  Desv. Est.:     {df['peso_dinamico'].std():.4f}")
    print(f"  Rango:          {df['peso_dinamico'].min():.4f} a {df['peso_dinamico'].max():.4f}")
    
    print(f"\n[RESULTADO]")
    print(f"  Período encontrado: {resultados['periodo_estimado']}")
    print(f"  Período real:       {resultados['periodo_oculto']}")
    print(f"  Éxito: {'✓' if resultados['exito'] else '✗'}")
    
    return resultados


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO 3: SECUENCIA PERIÓDICA (Simulación de Proceso Físico)
# ═══════════════════════════════════════════════════════════════════════════

def ejemplo_3_secuencia_periodica():
    """
    Simula un proceso físico con estructura periódica.
    
    Caso de uso: Mediciones repetidas de un experimento (ej: conteo de fotones)
    Expectativa: Pesos muy localizados, baja entropía
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Secuencia Periódica (Simulación Física)")
    print("="*80)
    
    # Simular mediciones periódicas: 1,2,3,1,2,3,...
    lista_n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    print(f"\nSecuencia: {lista_n}")
    
    resultados = experimento_simon_mejorado(
        lista_n=lista_n,
        periodo_oculto=3,      # Período = 3
        n_bits=4,
        num_mediciones=20
    )
    
    df = pd.DataFrame(resultados['analisis_simetria'])
    print(f"\n[ESTADÍSTICAS DE PESOS]")
    print(f"  Media:          {df['peso_dinamico'].mean():.4f}")
    print(f"  Entropía media: {df['entropia_proxy'].mean():.4f}")
    
    print(f"\n[DISTRIBUCIÓN DE TIPOS]")
    print(df['tipo_particula'].value_counts())
    
    return resultados


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO 4: BARRIDO DE PARÁMETROS
# ═══════════════════════════════════════════════════════════════════════════

def ejemplo_4_barrido_de_periodos():
    """
    Prueba con diferentes períodos ocultos para evaluar robustez.
    
    Pregunta: ¿Algunos períodos son más fáciles de recuperar que otros?
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: Barrido de Períodos (Robustez)")
    print("="*80)
    
    lista_n_base = [2, 3, 5, 7, 11, 13]
    n_bits = 4
    
    resultados_barrido = []
    
    print(f"\nProbando todos los períodos para n_bits={n_bits}...\n")
    print(f"{'Período':<8} | {'Binario':<10} | {'Éxito':<6} | {'Confianza':<10} | {'Estimado':<10}")
    print("-" * 60)
    
    for periodo in range(1, 2**n_bits):
        res = experimento_simon_mejorado(
            lista_n=lista_n_base,
            periodo_oculto=periodo,
            n_bits=n_bits,
            num_mediciones=20
        )
        
        resultados_barrido.append({
            'periodo': periodo,
            'binario': format(periodo, f'0{n_bits}b'),
            'exito': res['exito'],
            'confianza': res['confianza'],
            'estimado': res['periodo_estimado']
        })
        
        print(f"{periodo:<8} | {format(periodo, f'0{n_bits}b'):<10} | "
              f"{'✓' if res['exito'] else '✗':<6} | {res['confianza']:<10.1%} | "
              f"{res['periodo_estimado']:<10}")
    
    # Análisis estadístico
    df_barrido = pd.DataFrame(resultados_barrido)
    tasa_exito = df_barrido['exito'].sum() / len(df_barrido)
    
    print("\n[RESUMEN]")
    print(f"  Tasa de éxito: {tasa_exito:.1%} ({df_barrido['exito'].sum()}/{len(df_barrido)})")
    print(f"  Confianza promedio: {df_barrido['confianza'].mean():.2%}")
    print(f"  Confianza mín/máx: {df_barrido['confianza'].min():.2%} / {df_barrido['confianza'].max():.2%}")
    
    return resultados_barrido


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO 5: IMPACTO DE n_bits
# ═══════════════════════════════════════════════════════════════════════════

def ejemplo_5_impacto_nbits():
    """
    Evalúa cómo cambia el desempeño con diferentes dimensiones cuánticas.
    
    Pregunta: ¿Es más fácil recuperar el período en sistemas grandes o pequeños?
    """
    print("\n" + "="*80)
    print("EJEMPLO 5: Impacto de Dimensión Cuántica (n_bits)")
    print("="*80)
    
    lista_n = [1, 2, 3, 5, 8, 13, 21, 34]  # Fibonacci
    
    print(f"\nVariando n_bits con lista fija: {lista_n}\n")
    print(f"{'n_bits':<8} | {'Dim. Est.':<10} | {'Período':<10} | {'Éxito':<6} | {'Confianza':<10}")
    print("-" * 55)
    
    resultados_nbits = []
    
    for n_bits in range(2, 7):
        periodo = 2**(n_bits - 2)  # Período proporcional a dimensión
        
        res = experimento_simon_mejorado(
            lista_n=lista_n,
            periodo_oculto=periodo,
            n_bits=n_bits,
            num_mediciones=2*n_bits + 5
        )
        
        resultados_nbits.append({
            'n_bits': n_bits,
            'dim': 2**n_bits,
            'periodo': periodo,
            'exito': res['exito'],
            'confianza': res['confianza']
        })
        
        print(f"{n_bits:<8} | {2**n_bits:<10} | {periodo:<10} | "
              f"{'✓' if res['exito'] else '✗':<6} | {res['confianza']:<10.1%}")
    
    # Análisis
    df_nbits = pd.DataFrame(resultados_nbits)
    print("\n[ANÁLISIS]")
    print(f"  Tendencia: {'Mejora' if df_nbits['confianza'].is_monotonic_increasing else 'Variación'}")
    print(f"  Correlación (dim, confianza): {df_nbits['dim'].corr(df_nbits['confianza']):.3f}")
    
    return resultados_nbits


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO 6: ANÁLISIS COMPARATIVO DE SIMETRÍA
# ═══════════════════════════════════════════════════════════════════════════

def ejemplo_6_comparativa_simetria():
    """
    Compara propiedades de simetría entre diferentes listas de entrada.
    """
    print("\n" + "="*80)
    print("EJEMPLO 6: Análisis Comparativo de Simetría")
    print("="*80)
    
    # Tres tipos de listas diferentes
    casos = {
        'Primos': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
        'Cuadrados': [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
        'Fibonacci': [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    }
    
    analizador = AnalizadorSimetriaDinamica()
    
    print("\nAnálisis de Simetría por Tipo de Secuencia:\n")
    
    resultados_comparativa = {}
    
    for nombre, lista_n in casos.items():
        analisis = analizador.analizar_lista_n(lista_n)
        df = pd.DataFrame(analisis)
        
        print(f"\n[{nombre}]")
        print(f"  Valores: {lista_n}")
        print(f"  Pesos (media): {df['peso_dinamico'].mean():.4f}")
        print(f"  Pesos (std):   {df['peso_dinamico'].std():.4f}")
        print(f"  Entropía (media): {df['entropia_proxy'].mean():.4f}")
        
        tipos = df['tipo_particula'].value_counts()
        print(f"  Distribución: Fermiones={tipos.get('Fermión', 0)}, Bosones={tipos.get('Bosón', 0)}")
        
        resultados_comparativa[nombre] = df
    
    # Comparación visual
    print("\n" + "="*80)
    print("TABLA COMPARATIVA")
    print("="*80)
    
    for nombre, df in resultados_comparativa.items():
        print(f"\n{nombre}:")
        print(df[['n', 'paridad', 'quiralidad', 'peso_dinamico', 'tipo_particula']].head().to_string(index=False))


# ═══════════════════════════════════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "█"*80)
    print("  EJEMPLOS PRÁCTICOS: ALGORITMO DE SIMON CUÁNTICO MEJORADO")
    print("█"*80)
    
    # Ejecutar ejemplos (descomenta los que quieras ejecutar)
    
    # Ejemplo 1: Estructura alta
    # resultado1 = ejemplo_1_numeros_primos()
    
    # Ejemplo 2: Estructura baja
    # resultado2 = ejemplo_2_numeros_aleatorios()
    
    # Ejemplo 3: Secuencia periódica
    # resultado3 = ejemplo_3_secuencia_periodica()
    
    # Ejemplo 4: Barrido de períodos (tiempo moderado)
    # resultado4 = ejemplo_4_barrido_de_periodos()
    
    # Ejemplo 5: Impacto de n_bits (tiempo de ejecución considerable)
    # resultado5 = ejemplo_5_impacto_nbits()
    
    # Ejemplo 6: Análisis comparativo (rápido)
    resultado6 = ejemplo_6_comparativa_simetria()
    
    print("\n" + "█"*80)
    print("  FIN DE EJEMPLOS")
    print("█"*80 + "\n")