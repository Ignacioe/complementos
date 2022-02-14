import argparse
from cmath import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

class LayoutGraph:

    def __init__(self, grafo, iters, gravedad, refresh, const_repulsion, const_atraccion, verbose=False):
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
        self.gravedad = gravedad
        # TODO: faltan opciones
        self.refresh = refresh
        self.const_repulsion = const_repulsion
        self.const_atraccion = const_atraccion

        # Cambiar por constantes!!!!!!!!!!!!!!!!!!!!
        self.ka = 2.4 * math.sqrt(100/len(grafo[0]))
        self.kr = 0.3 * math.sqrt(100/len(grafo[0]))

    def inicializar_fuerzas(self):
        for nodo in (self.grafo[0]):
            self.fuerzasX[nodo] = 0
            self.fuerzasY[nodo] = 0
        return

    #Genera el grafico del grafo
    def dibujar(self):
        plt.pause(0.001)
        plt.clf()
        ax = plt.gca()
        posXver = self.posicionesX.values()
        posYver = self.posicionesY.values()

        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 11)
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

        plt.plot(np.array([inicio_x_ari, final_x_ari]), np.array([inicio_y_ari, final_y_ari]), color="Blue")


    def random_pos(self):
        for ver in (self.grafo[0]):
            self.posicionesX[ver] = np.random.rand()*10
            self.posicionesY[ver] = np.random.rand()*10

    def f_atraccion(self, d): return math.pow(d,2)/self.ka

    def f_repulsion(self, d): return math.pow(self.kr,2)/d

    def computar_fuerzas_atraccion(self):
        for ari in self.grafo[1]:
            v1 = ari[0]
            v2 = ari[1]
            x1 = self.posicionesX[v1]
            x2 = self.posicionesX[v2]
            y1 = self.posicionesY[v1]
            y2 = self.posicionesY[v2]
            dis = math.sqrt(((x2 - x1)**2)+((y2 - y1)**2))
            if dis>0.05:
                mod_fa = self.f_atraccion(dis)
            else:
                mod_fa = 1
                dis = 1
            fx = mod_fa * (x2-x1) / dis
            fy = mod_fa * (y2-y1) / dis
            self.fuerzasX[v1] += fx
            self.fuerzasY[v1] += fy
            self.fuerzasX[v2] -= fx
            self.fuerzasY[v2] -= fy

    def computar_fuerzas_repulsion(self):
        nodos = self.grafo[0].copy()
        for v1 in nodos:
            del nodos[0]
            for v2 in nodos:
                if v1 != v2:
                    x1 = self.posicionesX[v1]
                    x2 = self.posicionesX[v2]
                    y1 = self.posicionesY[v1]
                    y2 = self.posicionesY[v2]
                    dis = math.sqrt(((x2 - x1)**2)+((y2 - y1)**2))
                    if dis>0.05:
                        mod_fr = self.f_repulsion(dis)
                    else:
                        mod_fr = 1
                        dis = 1
                    fx = mod_fr * (x1-x2) / dis
                    fy = mod_fr * (y1-y2) / dis
                    self.fuerzasX[v1] += fx
                    self.fuerzasY[v1] += fy
                    self.fuerzasX[v2] -= fx
                    self.fuerzasY[v2] -= fy

    def computar_fuerza_gravedad(self):
        for v in self.grafo[0]:
            x = self.posicionesX[v]
            y = self.posicionesY[v]
            dis = math.sqrt(((5 - x)**2)+((5 - y)**2))
            if dis>0.05:
                mod_fg = self.gravedad * dis
            else:
                mod_fg = 1
                dis = 1
            fx = mod_fg * (5-x) / dis
            fy = mod_fg * (5-y) / dis
            self.fuerzasX[v] += fx
            self.fuerzasY[v] += fy

    def actualizar_pos(self):
        for ver in self.grafo[0]:
            # print("  Vertice", ver)
            # print("    Posicion", self.posicionesX[ver])
            # print("    Fuerza", self.fuerzasX[ver])
            nueva_posx = self.posicionesX[ver] + self.fuerzasX[ver]
            if nueva_posx>=10: nueva_posx = 10
            if nueva_posx<=0: nueva_posx = 0
            self.posicionesX[ver] = nueva_posx

            nueva_posy = self.posicionesY[ver] + self.fuerzasY[ver]
            if nueva_posy>=10: nueva_posy = 10
            if nueva_posy<=0: nueva_posy = 0
            self.posicionesY[ver] = nueva_posy

    def computar(self):
        self.inicializar_fuerzas()
        print("Despues de inicializar fuerzas")
        print("Posicion X:",self.posicionesX)
        print("Posicion Y:",self.posicionesY)
        self.computar_fuerzas_atraccion()
        print("Despues de computar atraccion")
        print("Fuerzas X:",self.fuerzasX)
        print("Fuerzas Y:",self.fuerzasY)
        self.computar_fuerzas_repulsion()
        print("Despues de computar repulsion")
        print("Fuerzas X:",self.fuerzasX)
        print("Fuerzas Y:",self.fuerzasY)
        self.computar_fuerza_gravedad()
        print("Despues de computar gravedad")
        print("Fuerzas X:",self.fuerzasX)
        print("Fuerzas Y:",self.fuerzasY)
        self.actualizar_pos()

    # Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar) un layout
    def layout(self):
        self.random_pos()
        plt.ion()
        for i in range(0,self.iters):
            print("Iteracion ", i)
            self.dibujar()
            self.computar()   
        plt.ioff()
        plt.show()
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
        default=200
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=0.02
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
        gravedad=args.temp,
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
