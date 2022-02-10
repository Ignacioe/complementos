import argparse
from cmath import sqrt
import matplotlib.pyplot as plt
import numpy as np
import math

class LayoutGraph:

    def __init__(self, grafo, iters, refresh, const_repulsion, const_atraccion, verbose=False):
        """
        Parametros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        refresh: cada cuantas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        const_repulsion: constante de repulsion
        const_atraccion: constante de atraccion
        verbose: si esta encendido, activa los comentarios
        """

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        self.posicionesX = {}
        self.posicionesY = {}
        self.fuerzasX = {}
        self.fuerzasY = {}

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.const_repulsion = const_repulsion
        self.const_atraccion = const_atraccion

        # Cambiar por constantes!!!!!!!!!!!!!!!!!!!!
        self.k = 1 * math.sqrt(100/len(grafo[0]))

    def inicializar_fuerzas(self):
        for nodo in (self.grafo[0]):
            self.fuerzasX[nodo] = 0
            self.fuerzasY[nodo] = 0
        return

    #Genera el grafico del grafo
    def dibujar(self):
        posXver = self.posicionesX.values()
        posYver = self.posicionesY.values()
        fig, ax = plt.subplots()
        ax.scatter(posXver, posYver, s = 20, c = "Black")

        inicio_x_ari = []
        final_x_ari = []
        inicio_y_ari = []
        final_y_ari = []

        for ari in (self.grafo[1]):
            inicio_x_ari.append(self.posicionesX[ari[0]])
            final_x_ari.append(self.posicionesX[ari[1]])
            inicio_y_ari.append(self.posicionesY[ari[0]])
            final_y_ari.append(self.posicionesY[ari[1]])

        ax.plot(np.array([inicio_x_ari, final_x_ari]), np.array([inicio_y_ari, final_y_ari]), color="Blue")

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        plt.show()

    def random_pos(self):
        for ver in (self.grafo[0]):
            self.posicionesX[ver] = np.random.rand()*10
            self.posicionesY[ver] = np.random.rand()*10

    def f_atraccion(self, d): return d^2/self.k

    def f_repulsion(self, d): return self.k^2/d

    def computar_fuerzas_atraccion(self):
        for ari in self.grafo[1]:
            v1 = ari[0]
            v2 = ari[1]
            x1 = self.posicionesX[v1]
            x2 = self.posicionesX[v2]
            y1 = self.posicionesY[v1]
            y2 = self.posicionesY[v2]
            dis = math.sqrt(((x2 - x1)**2)+((y2 - y1)**2))
            mod_fa = self.f_atraccion(dis)
            fx = mod_fa * (x2-x1) / dis
            fy = mod_fa * (y2-y1) / dis
            self.fuerzasX[v1] += fx
            self.fuerzasY[v1] += fy
            self.fuerzasX[v2] -= fx
            self.fuerzasY[v2] -= fy

    def computar_fuerzas_repulsion(self):
        for v1 in self.grafo[0]:
                for v2 in self.grafo[0]:
                    if v1 != v2:
                        x1 = self.posicionesX[v1]
                        x2 = self.posicionesX[v2]
                        y1 = self.posicionesY[v1]
                        y2 = self.posicionesY[v2]
                        dis = math.sqrt(((x2 - x1)**2)+((y2 - y1)**2))
                        mod_fa = self.f_repulsion(dis)
                        fx = mod_fa * (x2-x1) / dis
                        fy = mod_fa * (y2-y1) / dis
                        self.fuerzasX[v1] += fx
                        self.fuerzasY[v1] += fy
                        self.fuerzasX[v2] -= fx
                        self.fuerzasY[v2] -= fy

    # Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar) un layout
    def layout(self):
        self.random_pos()

        for iteracion in range(0,self.iters):
            self.inicializar_fuerzas()
            #Calcular fuerzas
            self.computar_fuerzas_atraccion()
            for v1 in self.grafo[0]:
                for v2 in self.grafo[0]:
                    if v1 != v2:
                        fuerza = self.fuerza_repulsion(v1,v2)
                        self.fuerzasX[v1] += fuerza
                        self.fuerzasY[v2] -= fuerza

        self.dibujar()

        pass

def leer_grafo(nom_arch):
    ver = []
    ari = []

    archivo = open(nom_arch,"r")
    cver = int(archivo.readline().rstrip("\n"))
    for i in range(0,cver):
        ver.append(archivo.readline().rstrip("\n"))
    for linea in archivo:
        ari.append(tuple(linea.rstrip("\n").split()))
    archivo.close()

    return (ver,ari)


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=1
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    grafo = leer_grafo(args.file_name)

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo=grafo, 
        iters=args.iters,
        refresh=1,
        const_repulsion=0.1,
        const_atraccion=5.0,
        verbose=args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
