import argparse
from cmath import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

class LayoutGraph:

    def __init__(self, grafo, iters, temperatura, gravedad, refresh, const_repulsion, const_atraccion, ancho, verbose):
        """
        Parametros:
        grafo: grafo en formato lista
        iters: cantidad de iteraciones a realizar
        temperatura: temperatura del sistema
        gravedad: fuerza con la que se atrae hacia el centro del grafico
        refresh: cada cuantas iteraciones graficar. Si su valor es cero, entonces debe graficarse solo al final.
        const_repulsion: constante de repulsion
        const_atraccion: constante de atraccion
        ancho: dimensiones del grafico
        verbose: si esta encendido, activa los comentarios
        """

        if(verbose): print(" Inicializando el objeto . . .")
        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        self.posicionesX = {}
        self.posicionesY = {}
        self.fuerzasX = {}
        self.fuerzasY = {}
        self.iters = iters
        self.verbose = verbose
        self.temperatura = temperatura
        self.gravedad = gravedad
        self.refresh = refresh
        self.const_repulsion = const_repulsion
        self.const_atraccion = const_atraccion
        self.ancho = ancho

        if(verbose): print(" Calculando constantes de atraccion y repulsion . . .")
        self.ka = const_atraccion * math.sqrt(math.pow(self.ancho,2)/len(grafo[0]))
        self.kr = const_repulsion * math.sqrt(math.pow(self.ancho,2)/len(grafo[0]))

        # epsilon: valor minimo para el cual se considera el caso borde
        self.epsilon = 0.05

    #Genera el grafico del grafo
    def dibujar(self):
        plt.pause(0.001)
        plt.clf()
        ax = plt.gca()
        posXver = self.posicionesX.values()
        posYver = self.posicionesY.values()

        ax.set_xlim(-(self.ancho*0.1), self.ancho*1.1)
        ax.set_ylim(-(self.ancho*0.1), self.ancho*1.1)
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

        if(self.verbose): print("  -  Dibujando el grafico . . .")
        plt.plot(np.array([inicio_x_ari, final_x_ari]), np.array([inicio_y_ari, final_y_ari]), color="Blue", lw=0.75)

    def random_pos(self):
        for ver in (self.grafo[0]):
            self.posicionesX[ver] = np.random.rand()*self.ancho
            self.posicionesY[ver] = np.random.rand()*self.ancho
        if(self.verbose): 
            print(" Generando coordenadas iniciales aleatorias para los vertices . . .")
            print("  -  posicionesX:",self.posicionesX)
            print("  -  posicionesY:",self.posicionesY)


    def inicializar_fuerzas(self):
        if(self.verbose): print("  -  Inicializando las fuerzas de atraccion y repulsion en 0 . . .")
        for nodo in (self.grafo[0]):
            self.fuerzasX[nodo] = 0
            self.fuerzasY[nodo] = 0
        return

    def f_atraccion(self, d): return math.pow(d,2)/self.ka

    def f_repulsion(self, d): return math.pow(self.kr,2)/d

    def actualizar_temp(self): 
        if(self.verbose): print(" Temperatura actual:",self.temperatura)
        self.temperatura *= 0.95
        return

    def distancia(self, x1, x2, y1, y2):
        return math.sqrt(pow((x2 - x1),2)+pow((y2 - y1),2))

    def computar_fuerzas_atraccion(self):
        for ari in self.grafo[1]:
            v1 = ari[0]
            v2 = ari[1]
            x1 = self.posicionesX[v1]
            x2 = self.posicionesX[v2]
            y1 = self.posicionesY[v1]
            y2 = self.posicionesY[v2]
            dis = self.distancia(x1,x2,y1,y2)
            if dis > self.epsilon:
                mod_fa = self.f_atraccion(dis)
                fx = mod_fa * (x2-x1) / dis
                fy = mod_fa * (y2-y1) / dis
                self.fuerzasX[v1] += fx
                self.fuerzasY[v1] += fy
                self.fuerzasX[v2] -= fx
                self.fuerzasY[v2] -= fy
        if(self.verbose): 
            print("  -  Computando las fuerzas de atraccion . . .")
            print("  -      fuerzasX:",self.fuerzasX)
            print("  -      fuerzasY:",self.fuerzasY)

    def computar_fuerzas_repulsion(self):
        nodos = self.grafo[0].copy()
        for v1 in nodos:
            nodos = np.delete(nodos,0)
            for v2 in nodos:
                if v1 != v2:
                    x1 = self.posicionesX[v1]
                    x2 = self.posicionesX[v2]
                    y1 = self.posicionesY[v1]
                    y2 = self.posicionesY[v2]
                    dis = self.distancia(x1,x2,y1,y2)
                    if dis < self.epsilon:
                        v_aleatorio = 0
                        while v_aleatorio < self.epsilon:
                            fx = np.random.rand()
                            fy = np.random.rand()
                            v_aleatorio = math.sqrt(math.pow(fx,2)+math.pow(fy,2))
                    else:
                        mod_fr = self.f_repulsion(dis)
                        fx = mod_fr * (x1-x2) / dis
                        fy = mod_fr * (y1-y2) / dis
                    self.fuerzasX[v1] += fx
                    self.fuerzasY[v1] += fy
                    self.fuerzasX[v2] -= fx
                    self.fuerzasY[v2] -= fy
        if(self.verbose): 
            print("  -  Computando las fuerzas de repulsion . . .")
            print("  -      fuerzasX:",self.fuerzasX)
            print("  -      fuerzasY:",self.fuerzasY)

    def computar_fuerza_gravedad(self):
        centro = self.ancho/2
        for v in self.grafo[0]:
            x = self.posicionesX[v]
            y = self.posicionesY[v]
            dis = self.distancia(x,centro,y,centro)
            if dis > self.epsilon:
                mod_fg = self.gravedad * dis
                fx = mod_fg * (centro-x) / dis
                fy = mod_fg * (centro-y) / dis
                self.fuerzasX[v] += fx
                self.fuerzasY[v] += fy
        if(self.verbose): 
            print("  -  Computando las fuerzas de gravedad . . .")
            print("  -      fuerzasX:",self.fuerzasX)
            print("  -      fuerzasY:",self.fuerzasY)

    def actualizar_pos(self):
        for ver in self.grafo[0]:
            mod_fa = math.sqrt((self.fuerzasX[ver]**2)+(self.fuerzasY[ver]**2))
            if(mod_fa > self.temperatura):
                self.fuerzasX[ver] = self.fuerzasX[ver] * self.temperatura / mod_fa
                self.fuerzasY[ver] = self.fuerzasX[ver] * self.temperatura / mod_fa
            nueva_posx = self.posicionesX[ver] + self.fuerzasX[ver]
            if nueva_posx>=self.ancho: nueva_posx = self.ancho
            if nueva_posx<=0: nueva_posx = 0
            self.posicionesX[ver] = nueva_posx

            nueva_posy = self.posicionesY[ver] + self.fuerzasY[ver]
            if nueva_posy>=self.ancho: nueva_posy = self.ancho
            if nueva_posy<=0: nueva_posy = 0
            self.posicionesY[ver] = nueva_posy
        if(self.verbose):
            print("  -  Actualizando las posiciones . . .")
            print("  -      posicionesX:",self.fuerzasX)
            print("  -      posicionesY:",self.fuerzasY)

    def computar(self):
        if(self.verbose): print("  -  Computando los valores para la proxima iteracion . . .")
        self.inicializar_fuerzas()
        self.computar_fuerzas_atraccion()
        self.computar_fuerzas_repulsion()
        self.computar_fuerza_gravedad()
        self.actualizar_pos()
        self.actualizar_temp()

    # Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar) un layout
    def layout(self):
        self.random_pos()
        plt.ion()
        if(self.verbose): print(" Aplicando el algoritmo de Fruchtermann-Reingold ",self.iters)
        refresh = self.refresh
        for i in range(0,self.iters):
            refresh-=1
            if(not refresh):
                if(self.verbose): print(" Iteracion",i,":")
                self.dibujar() 
                refresh = self.refresh
            self.computar()
        if(self.verbose): print(" Algoritmo finalizado en la iteracion",self.iters)
        plt.ioff()
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

    # Verbosidad
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa',
        default=False
    )
    # Cantidad de iteraciones
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=200
    )
    # Refresh
    parser.add_argument(
        '--ref',
        type=int,
        help='Cantidad de iteraciones entre refrescos de pantalla',
        default=1
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Gravedad
    parser.add_argument(
        '--grav',
        type=float,
        help='Gravedad',
        default=0.1
    )
    #Dimensiones del grafico
    parser.add_argument(
        '--ancho',
        type=int,
        help="Dimensiones del grafico",
        default = 10
    )
    # Archivo a leer
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
        temperatura=args.temp,
        gravedad=args.grav,
        refresh=args.ref,
        const_repulsion=0.15,
        const_atraccion=50.0,
        ancho=args.ancho,
        verbose=args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
