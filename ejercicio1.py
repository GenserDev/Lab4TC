"""
UNIVERSIDAD DEL VALLE DE GUATEMALA 
lABORATORIO 4 -- EJERCICIO 1 
Javier Chávez -- Genser Catalan

Construya el AFN resultante de aplicar el algoritmo de Thompson al árbol construido 
y mostrar su dibujo en pantalla. Posteriormente debe simular el AFN para reconocer 
cadenas de la expresión regular asociada. 
"""

from typing import  Set
import matplotlib.pyplot as plt
import networkx as nx

class Estado:
    def __init__(self, id_estado: int):
        self.id = id_estado
        self.transiciones = {}
        self.es_final = False
    
    def agregar_transicion(self, simbolo: str, estado_destino):
        if simbolo not in self.transiciones:
            self.transiciones[simbolo] = []
        self.transiciones[simbolo].append(estado_destino)

class AFN:
    def __init__(self):
        self.estados = {}
        self.estado_inicial = None
        self.estados_finales = set()
        self.contador_estados = 0
        self.alfabeto = set()
    
    def crear_estado(self) -> Estado:
        estado = Estado(self.contador_estados)
        self.estados[self.contador_estados] = estado
        self.contador_estados += 1
        return estado
    
    def establecer_inicial(self, estado: Estado):
        self.estado_inicial = estado
    
    def establecer_final(self, estado: Estado):
        estado.es_final = True
        self.estados_finales.add(estado.id)
    
    def agregar_simbolo_alfabeto(self, simbolo: str):
        if simbolo != 'ε':
            self.alfabeto.add(simbolo)

#Construye AFN basico
def construir_afn_simbolo(simbolo: str) -> AFN:
    afn = AFN()
    q_inicial = afn.crear_estado()
    q_final = afn.crear_estado()
    
    afn.establecer_inicial(q_inicial)
    afn.establecer_final(q_final)
    
    q_inicial.agregar_transicion(simbolo, q_final)
    afn.agregar_simbolo_alfabeto(simbolo)
    
    return afn

#Une dos AFN mediante concatenacion
def construir_afn_concatenacion(afn1: AFN, afn2: AFN) -> AFN:
    afn_resultado = AFN()
    
    mapeo_estados1 = {}
    for estado_id, estado in afn1.estados.items():
        nuevo_estado = afn_resultado.crear_estado()
        mapeo_estados1[estado_id] = nuevo_estado
        if estado.es_final:
            estado.es_final = False
    
    mapeo_estados2 = {}
    for estado_id, estado in afn2.estados.items():
        nuevo_estado = afn_resultado.crear_estado()
        mapeo_estados2[estado_id] = nuevo_estado
        if estado.es_final:
            afn_resultado.establecer_final(nuevo_estado)
    
    for estado_id, estado in afn1.estados.items():
        estado_origen = mapeo_estados1[estado_id]
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                estado_destino = mapeo_estados1[destino.id]
                estado_origen.agregar_transicion(simbolo, estado_destino)
                afn_resultado.agregar_simbolo_alfabeto(simbolo)
    
    for estado_id, estado in afn2.estados.items():
        estado_origen = mapeo_estados2[estado_id]
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                estado_destino = mapeo_estados2[destino.id]
                estado_origen.agregar_transicion(simbolo, estado_destino)
                afn_resultado.agregar_simbolo_alfabeto(simbolo)
    
    afn_resultado.establecer_inicial(mapeo_estados1[afn1.estado_inicial.id])
    
    for estado_final_id in afn1.estados_finales:
        estado_final_afn1 = mapeo_estados1[estado_final_id]
        estado_inicial_afn2 = mapeo_estados2[afn2.estado_inicial.id]
        estado_final_afn1.agregar_transicion('ε', estado_inicial_afn2)
    
    afn_resultado.alfabeto = afn1.alfabeto.union(afn2.alfabeto)
    
    return afn_resultado

#Une dos AFN mediante |
def construir_afn_union(afn1: AFN, afn2: AFN) -> AFN:
    afn_resultado = AFN()
    
    nuevo_inicial = afn_resultado.crear_estado()
    nuevo_final = afn_resultado.crear_estado()
    
    afn_resultado.establecer_inicial(nuevo_inicial)
    afn_resultado.establecer_final(nuevo_final)
    
    mapeo_estados1 = {}
    for estado_id, estado in afn1.estados.items():
        nuevo_estado = afn_resultado.crear_estado()
        mapeo_estados1[estado_id] = nuevo_estado
    
    mapeo_estados2 = {}
    for estado_id, estado in afn2.estados.items():
        nuevo_estado = afn_resultado.crear_estado()
        mapeo_estados2[estado_id] = nuevo_estado
    
    for estado_id, estado in afn1.estados.items():
        estado_origen = mapeo_estados1[estado_id]
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                estado_destino = mapeo_estados1[destino.id]
                estado_origen.agregar_transicion(simbolo, estado_destino)
                afn_resultado.agregar_simbolo_alfabeto(simbolo)
    
    for estado_id, estado in afn2.estados.items():
        estado_origen = mapeo_estados2[estado_id]
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                estado_destino = mapeo_estados2[destino.id]
                estado_origen.agregar_transicion(simbolo, estado_destino)
                afn_resultado.agregar_simbolo_alfabeto(simbolo)
    
    nuevo_inicial.agregar_transicion('ε', mapeo_estados1[afn1.estado_inicial.id])
    nuevo_inicial.agregar_transicion('ε', mapeo_estados2[afn2.estado_inicial.id])
    
    for estado_final_id in afn1.estados_finales:
        mapeo_estados1[estado_final_id].agregar_transicion('ε', nuevo_final)
    
    for estado_final_id in afn2.estados_finales:
        mapeo_estados2[estado_final_id].agregar_transicion('ε', nuevo_final)
    
    afn_resultado.alfabeto = afn1.alfabeto.union(afn2.alfabeto)
    
    return afn_resultado

#Construye la operacion *
def construir_afn_kleene(afn: AFN) -> AFN:
    afn_resultado = AFN()
    
    nuevo_inicial = afn_resultado.crear_estado()
    nuevo_final = afn_resultado.crear_estado()
    
    afn_resultado.establecer_inicial(nuevo_inicial)
    afn_resultado.establecer_final(nuevo_final)
    
    mapeo_estados = {}
    for estado_id, estado in afn.estados.items():
        nuevo_estado = afn_resultado.crear_estado()
        mapeo_estados[estado_id] = nuevo_estado
    
    for estado_id, estado in afn.estados.items():
        estado_origen = mapeo_estados[estado_id]
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                estado_destino = mapeo_estados[destino.id]
                estado_origen.agregar_transicion(simbolo, estado_destino)
                afn_resultado.agregar_simbolo_alfabeto(simbolo)
    
    nuevo_inicial.agregar_transicion('ε', mapeo_estados[afn.estado_inicial.id])
    nuevo_inicial.agregar_transicion('ε', nuevo_final)
    
    for estado_final_id in afn.estados_finales:
        mapeo_estados[estado_final_id].agregar_transicion('ε', nuevo_final)
        mapeo_estados[estado_final_id].agregar_transicion('ε', mapeo_estados[afn.estado_inicial.id])
    
    afn_resultado.alfabeto = afn.alfabeto.copy()
    
    return afn_resultado

#Construye la cerradura +
def construir_afn_positivo(afn: AFN) -> AFN:
    afn_concatenado = construir_afn_concatenacion(afn, construir_afn_kleene(afn))
    return afn_concatenado

#Construye la cerradura ?
def construir_afn_opcional(afn: AFN) -> AFN:
    afn_resultado = AFN()
    
    nuevo_inicial = afn_resultado.crear_estado()
    nuevo_final = afn_resultado.crear_estado()
    
    afn_resultado.establecer_inicial(nuevo_inicial)
    afn_resultado.establecer_final(nuevo_final)
    
    mapeo_estados = {}
    for estado_id, estado in afn.estados.items():
        nuevo_estado = afn_resultado.crear_estado()
        mapeo_estados[estado_id] = nuevo_estado
    
    for estado_id, estado in afn.estados.items():
        estado_origen = mapeo_estados[estado_id]
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                estado_destino = mapeo_estados[destino.id]
                estado_origen.agregar_transicion(simbolo, estado_destino)
                afn_resultado.agregar_simbolo_alfabeto(simbolo)
    
    nuevo_inicial.agregar_transicion('ε', mapeo_estados[afn.estado_inicial.id])
    nuevo_inicial.agregar_transicion('ε', nuevo_final)
    
    for estado_final_id in afn.estados_finales:
        mapeo_estados[estado_final_id].agregar_transicion('ε', nuevo_final)
    
    afn_resultado.alfabeto = afn.alfabeto.copy()
    
    return afn_resultado

#Convierte expresión regular a posfix
def convertir_a_postfijo(expresion: str) -> str:
    precedencia = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    pila = []
    resultado = []
    
    expresion_con_concat = ""
    for i, char in enumerate(expresion):
        expresion_con_concat += char
        if i < len(expresion) - 1:
            siguiente = expresion[i + 1]
            if (char not in '(|' and siguiente not in ')*+?|' and 
                char not in '*+?'):
                expresion_con_concat += '.'
    
    for char in expresion_con_concat:
        if char.isalnum() or char == 'ε':
            resultado.append(char)
        elif char == '(':
            pila.append(char)
        elif char == ')':
            while pila and pila[-1] != '(':
                resultado.append(pila.pop())
            pila.pop()
        else:
            while (pila and pila[-1] != '(' and 
                   precedencia.get(pila[-1], 0) >= precedencia.get(char, 0)):
                resultado.append(pila.pop())
            pila.append(char)
    
    while pila:
        resultado.append(pila.pop())
    
    return ''.join(resultado)

#Construye AFN usando algoritmo de Thompson
def construir_afn_desde_expresion(expresion: str) -> AFN:
    postfijo = convertir_a_postfijo(expresion)
    pila = []
    
    for char in postfijo:
        if char.isalnum() or char == 'ε':
            afn = construir_afn_simbolo(char)
            pila.append(afn)
        elif char == '.':
            afn2 = pila.pop()
            afn1 = pila.pop()
            afn_resultado = construir_afn_concatenacion(afn1, afn2)
            pila.append(afn_resultado)
        elif char == '|':
            afn2 = pila.pop()
            afn1 = pila.pop()
            afn_resultado = construir_afn_union(afn1, afn2)
            pila.append(afn_resultado)
        elif char == '*':
            afn = pila.pop()
            afn_resultado = construir_afn_kleene(afn)
            pila.append(afn_resultado)
        elif char == '+':
            afn = pila.pop()
            afn_resultado = construir_afn_positivo(afn)
            pila.append(afn_resultado)
        elif char == '?':
            afn = pila.pop()
            afn_resultado = construir_afn_opcional(afn)
            pila.append(afn_resultado)
    
    return pila[0]

#Calcula la cerradura epsilon 
def obtener_cerradura_epsilon(estado: Estado, visitados: Set[int] = None) -> Set[Estado]:
    if visitados is None:
        visitados = set()
    
    if estado.id in visitados:
        return set()
    
    visitados.add(estado.id)
    cerradura = {estado}
    
    if 'ε' in estado.transiciones:
        for estado_destino in estado.transiciones['ε']:
            cerradura.update(obtener_cerradura_epsilon(estado_destino, visitados))
    
    return cerradura

#AFN con una cadena de entrada
def simular_afn(afn: AFN, cadena: str) -> bool:
    estados_actuales = obtener_cerradura_epsilon(afn.estado_inicial)
    
    for simbolo in cadena:
        nuevos_estados = set()
        for estado in estados_actuales:
            if simbolo in estado.transiciones:
                for estado_destino in estado.transiciones[simbolo]:
                    nuevos_estados.update(obtener_cerradura_epsilon(estado_destino))
        estados_actuales = nuevos_estados
        
        if not estados_actuales:
            return False
    
    for estado in estados_actuales:
        if estado.es_final:
            return True
    
    return False

#Dibuja el grafo
def dibujar_afn(afn: AFN):
    G = nx.DiGraph()
    
    for estado_id, estado in afn.estados.items():
        G.add_node(estado_id)
    
    edge_labels = {}
    for estado_id, estado in afn.estados.items():
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                edge = (estado_id, destino.id)
                if edge in edge_labels:
                    edge_labels[edge] += f", {simbolo}"
                else:
                    edge_labels[edge] = simbolo
                G.add_edge(estado_id, destino.id)
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    node_colors = []
    for node in G.nodes():
        if node == afn.estado_inicial.id:
            node_colors.append('lightgreen')
        elif node in afn.estados_finales:
            node_colors.append('lightcoral')
        else:
            node_colors.append('lightblue')
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
    
    plt.title("AFN generado por el Algoritmo de Thompson")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Procesa archivo expresiones.txt
def procesar_archivo(nombre_archivo: str):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for numero_linea, linea in enumerate(archivo, 1):
                expresion = linea.strip()
                if expresion:
                    print(f"\n--- Procesando línea {numero_linea}: {expresion} ---")
                    try:
                        afn = construir_afn_desde_expresion(expresion)
                        print(f"AFN construido exitosamente")
                        print(f"Estados: {len(afn.estados)}")
                        print(f"Estado inicial: {afn.estado_inicial.id}")
                        print(f"Estados finales: {afn.estados_finales}")
                        print(f"Alfabeto: {afn.alfabeto}")
                        
                        dibujar_afn(afn)
                        
                        cadenas_prueba = input("Ingresa cadenas para probar (separadas por espacio): ").split()
                        for cadena in cadenas_prueba:
                            resultado = simular_afn(afn, cadena)
                            print(f"Cadena '{cadena}': {'sí' if resultado else 'no'}")
                        
                    except Exception as e:
                        print(f"Error procesando la expresión: {e}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")

def main():
    nombre_archivo = "expresiones.txt"
    procesar_archivo(nombre_archivo)

if __name__ == "__main__":
    main()