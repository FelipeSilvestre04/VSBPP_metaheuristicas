import sys
import os
import ast
from collections import Counter
import time
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import turtle
import math
from botao import Botao
from nfp_teste import combinar_poligonos, triangulate_shapely,NoFitPolygon, interpolar_pontos_poligono
import shapely
from shapely import Polygon, MultiPolygon, unary_union, LineString, MultiLineString, MultiPoint, LinearRing, GeometryCollection

from scipy.spatial import ConvexHull
import numpy as np
import cv2
import copy
import pyautogui

def extrair_vertices(encaixes):
    vertices = []
    if isinstance(encaixes, MultiPolygon):
        for poly in encaixes.geoms:
            vertices.extend(list(poly.exterior.coords))
            for hole in poly.interiors:
                vertices.extend(list(hole.coords))
    elif isinstance(encaixes, Polygon):
        vertices.extend(list(encaixes.exterior.coords))
        for hole in encaixes.interiors:
            vertices.extend(list(hole.coords))
    elif isinstance(encaixes, MultiLineString):
        for line in encaixes.geoms:
            vertices.extend(list(line.coords))
    elif isinstance(encaixes, LineString):
        vertices.extend(list(encaixes.coords))
    elif isinstance(encaixes, Point):
        vertices.append((encaixes.x, encaixes.y))
    elif isinstance(encaixes, MultiPoint):
        for pt in encaixes.geoms:
            vertices.append((pt.x, pt.y))

    elif isinstance(encaixes, LinearRing):
        vertices.extend(list(encaixes.coords))

    elif isinstance(encaixes, GeometryCollection):
        encaixe = encaixes
        for encaixes in encaixe.geoms:
            if isinstance(encaixes, MultiPolygon):
                for poly in encaixes.geoms:
                    vertices.extend(list(poly.exterior.coords))
                    for hole in poly.interiors:
                        vertices.extend(list(hole.coords))
            elif isinstance(encaixes, Polygon):
                vertices.extend(list(encaixes.exterior.coords))
                for hole in encaixes.interiors:
                    vertices.extend(list(hole.coords))
            elif isinstance(encaixes, MultiLineString):
                for line in encaixes.geoms:
                    vertices.extend(list(line.coords))
            elif isinstance(encaixes, LineString):
                vertices.extend(list(encaixes.coords))

            elif isinstance(encaixes, Point):
                vertices.append((encaixes.x, encaixes.y))
            elif isinstance(encaixes, MultiPoint):
                for pt in encaixes.geoms:
                    vertices.append((pt.x, pt.y))

            elif isinstance(encaixes, LinearRing):
                vertices.extend(list(encaixes.coords))

    return vertices
def multiplicar_tudo(d, multiplicador):
    novo_dicionario = {}

    for chave, valor in d.items():
        # Multiplicar a chave
        nova_chave = tuple(
            multiplicar_elemento(e, multiplicador) for e in chave
        )

        # Multiplicar os valores (listas de tuplas)
        novo_valor = [
            tuple(x * multiplicador for x in ponto) for ponto in valor
        ]

        novo_dicionario[nova_chave] = novo_valor

    return novo_dicionario


def multiplicar_elemento(e, multiplicador):
    if isinstance(e, (int, float)):
        return e * multiplicador
    elif isinstance(e, tuple):
        return tuple(multiplicar_elemento(x, multiplicador) for x in e)
    else:
        return e  # se aparecer algo que não seja número/tupla, mantém igual

def projetar_vertices_em_poligono(poligono_principal, lista_poligonos):
    """
    Projeta os vértices de uma lista de polígonos em um polígono principal.
    
    Para cada vértice dos polígonos na lista, cria duas retas:
    - Uma paralela ao eixo X
    - Uma paralela ao eixo Y
    E adiciona ao polígono principal os pontos de interseção dessas retas com o polígono.
    
    Args:
        poligono_principal: Lista de tuplas (x, y) representando os vértices do polígono principal.
        lista_poligonos: Lista de polígonos, onde cada polígono é uma lista de tuplas (x, y).
        
    Returns:
        Lista de tuplas (x, y) representando o polígono principal com as projeções adicionadas.
    """
    import math
    from functools import cmp_to_key
    
    # Verificação de entrada
    if not poligono_principal or len(poligono_principal) < 3:
        return poligono_principal.copy() if poligono_principal else []
    
    # Cria uma cópia do polígono principal para não modificar o original
    poligono_resultado = poligono_principal.copy()
    
    # Coletar todos os vértices dos polígonos da lista
    todos_vertices = []
    for poligono in lista_poligonos:
        if poligono:  # Verificar se o polígono não está vazio
            todos_vertices.extend(poligono)
    
    # Para cada vértice, encontrar as interseções das retas paralelas aos eixos com o polígono principal
    for vertice in todos_vertices:
        x_vertice, y_vertice = vertice
        
        # Encontrar interseções da reta horizontal (paralela ao eixo X) com o polígono principal
        for i in range(len(poligono_principal)):
            p1 = poligono_principal[i]
            p2 = poligono_principal[(i + 1) % len(poligono_principal)]
            
            # Verificar se o segmento cruza a linha horizontal y = y_vertice
            if not ((p1[1] <= y_vertice <= p2[1]) or (p2[1] <= y_vertice <= p1[1])):
                continue
                
            # Se os pontos têm a mesma coordenada y (segmento horizontal)
            if abs(p1[1] - p2[1]) < 1e-10:  # Usar uma pequena tolerância para comparação
                # Se o y do vértice coincide com o y do segmento horizontal
                if abs(p1[1] - y_vertice) < 1e-10:
                    # Adicionar os pontos do segmento horizontal que estão entre xmin e xmax
                    x_min = min(p1[0], p2[0])
                    x_max = max(p1[0], p2[0])
                    if x_min <= x_vertice <= x_max:
                        ponto_intersecao = (x_vertice, y_vertice)
                        if ponto_intersecao not in poligono_resultado:
                            poligono_resultado.append(ponto_intersecao)
            else:
                # Segmento não horizontal - calcular interseção
                t = (y_vertice - p1[1]) / (p2[1] - p1[1])
                if 0 <= t <= 1:  # Verificar se a interseção está dentro do segmento
                    x_intersecao = p1[0] + t * (p2[0] - p1[0])
                    ponto_intersecao = (x_intersecao, y_vertice)
                    if ponto_intersecao not in poligono_resultado:
                        poligono_resultado.append(ponto_intersecao)
        
        # Encontrar interseções da reta vertical (paralela ao eixo Y) com o polígono principal
        for i in range(len(poligono_principal)):
            p1 = poligono_principal[i]
            p2 = poligono_principal[(i + 1) % len(poligono_principal)]
            
            # Verificar se o segmento cruza a linha vertical x = x_vertice
            if not ((p1[0] <= x_vertice <= p2[0]) or (p2[0] <= x_vertice <= p1[0])):
                continue
                
            # Se os pontos têm a mesma coordenada x (segmento vertical)
            if abs(p1[0] - p2[0]) < 1e-10:  # Usar uma pequena tolerância para comparação
                # Se o x do vértice coincide com o x do segmento vertical
                if abs(p1[0] - x_vertice) < 1e-10:
                    # Adicionar os pontos do segmento vertical que estão entre ymin e ymax
                    y_min = min(p1[1], p2[1])
                    y_max = max(p1[1], p2[1])
                    if y_min <= y_vertice <= y_max:
                        ponto_intersecao = (x_vertice, y_vertice)
                        if ponto_intersecao not in poligono_resultado:
                            poligono_resultado.append(ponto_intersecao)
            else:
                # Segmento não vertical - calcular interseção
                t = (x_vertice - p1[0]) / (p2[0] - p1[0])
                if 0 <= t <= 1:  # Verificar se a interseção está dentro do segmento
                    y_intersecao = p1[1] + t * (p2[1] - p1[1])
                    ponto_intersecao = (x_vertice, y_intersecao)
                    if ponto_intersecao not in poligono_resultado:
                        poligono_resultado.append(ponto_intersecao)
    
    # Se temos menos de 3 pontos, não podemos formar um polígono
    if len(poligono_resultado) < 3:
        return poligono_resultado
    
    # Reordenar os pontos no sentido anti-horário
    # Calcular o centroide
    cx = sum(x for x, _ in poligono_resultado) / len(poligono_resultado)
    cy = sum(y for _, y in poligono_resultado) / len(poligono_resultado)
    
    # Função para comparar pontos baseada no ângulo com respeito ao centroide
    def comparar_pontos(p1, p2):
        angulo1 = math.atan2(p1[1] - cy, p1[0] - cx)
        angulo2 = math.atan2(p2[1] - cy, p2[0] - cx)
        return -1 if angulo1 < angulo2 else (1 if angulo1 > angulo2 else 0)
    
    # Reordenar os pontos
    poligono_resultado.sort(key=cmp_to_key(comparar_pontos))
    
    # Remover pontos duplicados ou muito próximos
    i = 0
    while i < len(poligono_resultado):
        j = (i + 1) % len(poligono_resultado)
        p1 = poligono_resultado[i]
        p2 = poligono_resultado[j]
        
        # Verificar se os pontos são muito próximos
        distancia = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        if distancia < 1e-6:  # Tolerância para pontos próximos
            # Remover o ponto j
            poligono_resultado.pop(j if j < i else i)
        else:
            i += 1
    
    return poligono_resultado


def NFP(PecaA,grauA,PecaB,grauB):
    graus = [0,90,180,270]
    grauA = graus[grauA]
    grauB = graus[grauB]
    pontos_pol_A = [(int(rotate_point(cor[0], cor[1], grauA)[0]), int(rotate_point(cor[0], cor[1], grauA)[1])) for cor in PecaA]
    pontos_pol_B = [(int(rotate_point(cor[0], cor[1], grauB)[0]), int(rotate_point(cor[0], cor[1], grauB)[1])) for cor in PecaB]
    nfps_CB_CA = []

    if Polygon(pontos_pol_B).equals(Polygon(pontos_pol_B).convex_hull):
        convex_partsB = [pontos_pol_B] 
    else:
        convex_partsB = triangulate_shapely(pontos_pol_B)
    
    if Polygon(pontos_pol_A).equals(Polygon(pontos_pol_A).convex_hull):
        convex_partsA = [pontos_pol_A]
    else:
        convex_partsA = triangulate_shapely(pontos_pol_A)

    nfps_convx = []
    for CB in convex_partsB:
        for convex in convex_partsA:
            nfps_convx.append(Polygon(NoFitPolygon(convex, CB)))


    nfp = unary_union(nfps_convx)
    nfp_final = extrair_vertices(nfp)
    #print(nfp_final)

    return nfp_final
def ler_ins(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    idx = 0

    # 1. Ler número de itens e número de tamanhos de bin
    n_itens, n_bins = map(int, linhas[idx + 1].split())
    idx += 2

    # 2. Ignorar RELATIVE/ABSOLUTE instance number
    idx += 1

    # 3. Ler tamanhos dos bins (altura e largura de cada)
    valores = list(map(int, linhas[idx].split()))
    hbins = valores[:n_bins]
    wbins = valores[n_bins:2 * n_bins]
    idx += 1

    # 4. Ler lucro dos bins
    lucros_bins = list(map(int, linhas[idx].split()))
    idx += 1

    # 5. Ler dimensões das peças
    pecas = []
    while len(pecas) < n_itens:
        linha = list(map(int, linhas[idx].split()))
        for i in range(0, len(linha), 2):
            h, w = linha[i:i+2]
            coordenadas = [(0, 0), (w, 0), (w, h), (0, h)]  # Retângulo em coordenadas
            pecas.append(coordenadas)
        idx += 1

    return [((h, w), lucro) for h, w, lucro in zip(hbins, wbins, lucros_bins)], pecas
class CSP():
    def __init__(self,dataset='fu',Base=None,Altura=None,Escala=None,render=False,plot=True, x=-200, y=200, suavizar = True, pre_processar = False, tabela = None, margem = 5, ajuste = False):
        # self.graus = [0,1,2,3]
        self.x = x
        self.y = y
        
        self.render = render
        self.plot = plot
        
        self.pecas = dataset
        # self.rotacoes = [0,1,2,3]

        if not self.instancias():   
            if Base == None and Altura == None:
                self.base = 500
                self.altura = 500
                self.Escala = 0.3
            else:
                self.base = Base
                self.altura = Altura
                self.Escala = 1
                suavizar = False
        else:
            self.instancias()
            # self.base *= 2
            suavizar = False
        


        self.area = self.base * self.altura

        
       
        iteracoes = 10  # Número de iterações para a abertura
        tamanho_kernel = 15  # Tamanho do kernel para suavização
        area_minima = 50  # Área mínima para considerar o polígono válido
        epsilon = 1.8  # Parâmetro de suavização para simplificação de vértices


        try:
            self.lista_original = ler_ins( self.pecas +'.dat')
        except FileNotFoundError:
            self.lista_original = ler_ins(self.pecas)
        
        if suavizar:
            lista = [suavizar_poligono(idx, self.lista_original, iteracoes, tamanho_kernel, area_minima, epsilon)[0] for idx in range(len(self.lista_original))]
        else:
            lista = self.lista_original
        

        
        self.lista_original = copy.deepcopy(lista)
        self.nova_lista_original, self.nova_lista_completa_original = tratar_lista(self.lista_original, self.Escala)
        
        if ajuste:
            self.lista_original = [ajustar_poligono(pol) for pol in self.lista_original]
            self.nova_lista_original = [ajustar_poligono(pol) for pol in self.nova_lista_original]
            self.nova_lista_completa_original = [ajustar_poligono(pol) for pol in self.nova_lista_completa_original]

        self.max_pecas = len(self.lista_original)
        

        
        self.lista, self.nova_lista, self.nova_lista_completa = copy.deepcopy(self.lista_original), copy.deepcopy(self.nova_lista_original), copy.deepcopy(self.nova_lista_completa_original)
        
        if pre_processar:
            self.tabela_nfps = pre_processar_NFP([0,1,2,3], self.nova_lista, margem)
        else:
            self.tabela_nfps = tabela




   


        self.pecas_posicionadas = []
        self.indices_pecas_posicionadas = []
        self.lista_removida = []
        self.cordenadas_pecas = []
        
        self.cordenadas_area = ([self.x, self.y],[(self.x + self.base), self.y],[(self.x + self.base), (self.y - self.altura)],[self.x, (self.y - self.altura)])
        self._img = Image.new('L', (self.base, self.altura), 0)
        self._matriz = np.array(self._img)
        if self.plot:
            self._fig, self._ax = plt.subplots()
        
        if self.render:
            turtle.tracer(0)
            self.botao_remover = Botao(self.x - (self.base/2) + 350, self.y + 300, 200, 150, 'pop')
            self.botao_reset = Botao(self.x - (self.base/2) + 600, self.y + 300, 200, 150,'reset')
            self.botao_blf = Botao(self.x - (self.base/2) + 100, self.y + 300, 200, 150,'BLF', 'blue')
            self.botao_ex = Botao(self.x - (self.base/2) -150, self.y + 300, 200, 150,'ExSearch', "blue")
            
            self.botao_intmais = Botao(self.x - (self.base/2) -350, self.y - 200, 100, 100,'+', "deepskyblue")
            self.botao_intmenos = Botao(self.x - (self.base/2) -150, self.y - 200, 100, 100,'-', "deepskyblue")
            
            self.botao_pmais = Botao(self.x - (self.base/2) -350, self.y - 0, 100, 100,'+', "deepskyblue")
            self.botao_pmenos = Botao(self.x - (self.base/2) -150, self.y - 0, 100, 100,'-', "deepskyblue")
            
            self.botao_draw = Botao(self.x + (self.base/2) +350, self.y - 300, 200, 150,'Draw','mediumpurple')
            self.botao_nfp1 = Botao(self.x + (self.base/2) +350, self.y - 100, 200, 150,'NFP1','mediumpurple')
            self.botao_nfp2 = Botao(self.x + (self.base/2) +550, self.y - 100, 200, 150,'NFP2','mediumpurple')
            self.botao_ch = Botao(self.x + (self.base/2) +350, self.y + 100, 200, 150,'Fecho','mediumpurple')

            self.turtle_fecho = turtle.Turtle()
            self.turtle_dados = turtle.Turtle()
            self.lista_turtle = []
            self.renderizar()
            
        self.area_ocupada = 0
        self.fecho = 0
        self.vertices_fecho = []

        self.dict_nfps = {}

    def area_usada(self):
        # Converte os polígonos pra formato hashable (tupla de tuplas)
        original_counter = Counter(tuple(map(tuple, pol)) for pol in self.lista_original)
        nao_usado_counter = Counter(tuple(map(tuple, pol)) for pol in self.lista)

        # Subtrai pra obter os usados
        usados_counter = original_counter - nao_usado_counter

        # Reconstrói a lista de polígonos usados
        usados = []
        for pol, count in usados_counter.items():
            usados.extend([list(pol) for _ in range(count)])

        # Soma as áreas
        area_total = sum(Polygon(pol).area for pol in usados)

        # Área total do bin
        coords = []
        for pol in self.pecas_posicionadas:
            for x,y in pol:
                coords.append(x)
        
        larg = max(coords) - min(coords)
        # area_bin = (larg / self.Escala) * (self.altura / self.Escala)
        area_bin = (self.base / self.Escala) * (self.altura / self.Escala)

        return round((area_total / area_bin) * 100, 2) 
    def rot_pol(self,pol, grau_indice):
        graus = [0, 90, 180, 270]
        grau = graus[grau_indice]

        pol_posicionar = self.nova_lista[pol]

        pontos_posicionar = [(int(rotate_point(cor[0], cor[1], grau)[0]), int(rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_posicionar]
        
        return pontos_posicionar
     
    def acao(self,peca,x,y,grau_indice,flip = False,verificado=False):
        if peca < len(self.lista):
            if not verificado: 
                #print("Nao Verificado")       
                pol_verificacao = self.nova_lista_completa[peca]
                pol_posicionar = self.nova_lista[peca]
                if flip:
                    pol_posicionar = flip_polygon(pol_posicionar)
                    pol_verificacao = flip_polygon(pol_verificacao)
                graus = [0, 90, 180, 270]
                grau = graus[grau_indice]
        
                pontos_verificacao = [(int(x) + int(rotate_point(cor[0], cor[1], grau)[0]), int(y) + int(rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_verificacao]
                pontos_posicionar = [(int(x) + int(rotate_point(cor[0], cor[1], grau)[0]), int(y) + int(rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_posicionar]
                
                if self.posicao_disponivel(peca,grau_indice,x,y,pontos_verificacao):
                    self.indices_pecas_posicionadas.append([x,y,grau_indice,self.nova_lista_original.index(pol_posicionar)])
                    self.pecas_posicionadas.append(pontos_posicionar)
                    if self.render:
                        p = turtle.Turtle()
                        self.posicionar_turtle(pontos_posicionar,p)
                        p.hideturtle()
                        self.lista_turtle.append(p)
                    self.remover_lista(peca) 
                    self.atualizar_matriz()
                    self.atualizar_dados()
            else:
                    #print("entrou")
                    pol_posicionar = self.nova_lista[peca]
                    if flip:
                        pol_posicionar = flip_polygon(pol_posicionar)

                    graus = [0, 90, 180, 270]
                    grau = graus[grau_indice]
            
                    pontos_posicionar = [(int(x) + int(rotate_point(cor[0], cor[1], grau)[0]), int(y) + int(rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_posicionar]
                    
                    if True:
                        self.indices_pecas_posicionadas.append([x,y,grau_indice,self.nova_lista_original.index(pol_posicionar)])
                        self.pecas_posicionadas.append(pontos_posicionar)
                        if self.render:
                            p = turtle.Turtle()
                            self.posicionar_turtle(pontos_posicionar,p)
                            p.hideturtle()
                            self.lista_turtle.append(p)
                        self.remover_lista(peca) 
                        self.atualizar_matriz()
                        self.atualizar_dados()

        else:
            print("Error")
            return False
     
    def ExSearch(self, peca, grau_indice, draw = False, inter = 0):
        possiveis_posicoes = []
        nfp = []
        flip = False
        pol_posicionar = self.nova_lista[peca]
        graus = [0,90,180,270]
        grau = graus[grau_indice]
        pontos_pol = [(int(rotate_point(cor[0], cor[1], grau)[0]), int(rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_posicionar]
        lista = []


        nfp = self.nfp(peca, grau_indice, inter)

        for x,y in nfp:
                    if draw:
                            for i in range(50):
                                self.draw_click(x,-y,grau_indice,peca,flip)
                    pontos = [(int(x + rotate_point(cor[0], cor[1], grau)[0]), int(y + rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_posicionar]       
            


                    
                    posicao_valida = True
                    for x1,y1 in pontos:
                        if not ponto_dentro_poligono(x1,y1,self.cordenadas_area, True):
                            posicao_valida = False
                    if posicao_valida:

                        pecas_posicionadas = copy.deepcopy(self.pecas_posicionadas)
                        pecas_posicionadas.append(pontos)

                        area_ocupada = calcular_area_preenchida(pecas_posicionadas)
                        area_FC = calcular_fecho_area(pecas_posicionadas)
                        area_FR = area_fecho_retangular(pecas_posicionadas)

                        #fecho_convexo = (1 - (area_ocupada/area_FR))
                        fecho_convexo_max = area_ocupada/area_FC
                        fecho_retangular_max = area_ocupada/area_FR
                        #fechoR = (1 - (area_ocupada/area_FR))
                        #nfp_meu = (fecho_convexo_max**10)*(area_FC/(self.area))

                        pecas_posicionadas = []
                        #if fecho == "convexo":
                        possiveis_posicoes.append([peca,x,y,grau_indice,flip,round(fecho_convexo_max,2),round(fecho_retangular_max,2),self.lista[peca]])
                        #elif fecho == "retangular":
                        #possiveis_posicoes.append([peca,x,y,grau_indice,flip,round(fecho_retangular_max,2),round(fecho_convexo_max,2),self.lista[peca]])

        if possiveis_posicoes:
            maior = float('-inf')
            possiveis_pecas = []
                    
            for posicao1 in possiveis_posicoes:
                if posicao1[4] > maior:
                    possiveis_pecas = [copy.deepcopy(posicao1)]
                    maior = posicao1[4]
                elif posicao1[4] == maior:
                    possiveis_pecas.append(copy.deepcopy(posicao1))
                    
                    # Encontrar a peça com a maior área entre as possíveis peças
            area = float('-inf')
            melhor_posicao = None
            for pc in possiveis_pecas:
                area_atual = pc[5]
                if area_atual > area:
                    area = area_atual
                    melhor_posicao = copy.deepcopy(pc)
            
            return melhor_posicao
        else:
            return None

    def BLF(self, peca, grau_indice, draw=False, inter = 0):
        possiveis_posicoes = []
        nfp = []
        flip = False
        pol_posicionar = self.nova_lista[peca]
        graus = [0,90,180,270]
        grau = graus[grau_indice]
        pontos_pol = [(int(rotate_point(cor[0], cor[1], grau)[0]), int(rotate_point(cor[0], cor[1], grau)[1])) for cor in pol_posicionar]
        lista = []


        nfp = self.nfp(peca, grau_indice, inter)
        nfp = sorted(nfp, key=lambda ponto: (ponto[0], ponto[1]))

        for i,j in nfp:     
                x_t, y_t = i,j
                
                if draw:
                    for k in range(50):
                        self.draw_click(x_t, -y_t, grau_indice, peca, False)

                pontos = [(round(x_t + rotate_point(cor[0], cor[1], grau)[0]), 
                        round(y_t + rotate_point(cor[0], cor[1], grau)[1])) 
                        for cor in pol_posicionar]

                # Verifica se a posição é válida
                posicao_valida = True
                for x1, y1 in pontos:
                    if y1 > self.y:
                        posicao_valida = False
                        break
                    if x1 < self.cordenadas_area[0][0] or x1 > self.cordenadas_area[1][0] or y1 > self.cordenadas_area[0][1] or y1 < self.cordenadas_area[2][1]:
                        posicao_valida = False
                if nfp and ponto_dentro_poligono(x_t, y_t, nfp, False):
                    posicao_valida = False

                if posicao_valida:
                    pecas_posicionadas = copy.deepcopy(self.pecas_posicionadas)
                    pecas_posicionadas.append(pontos)

                    area_ocupada = calcular_area_preenchida(pecas_posicionadas)
                    area_FC = calcular_fecho_area(pecas_posicionadas)
                    area_FR = area_fecho_retangular(pecas_posicionadas)

                    fecho_convexo_max = area_ocupada/area_FC
                    fecho_retangular_max = area_ocupada/area_FR

                    possiveis_posicoes.append([peca, x_t, y_t, grau_indice, flip, 
                                            round(fecho_convexo_max,2), 
                                            round(fecho_convexo_max,2), 
                                            self.lista[peca]])
                    # Retorna a primeira posição válida encontrada
                    return possiveis_posicoes[0]

        return None
    def nfp(self, peca, grau_indice, inter = 0, proj = False, area = False, bin = False):
        

        if not self.pecas_posicionadas:
            ifp = self.ifp(self.rot_pol(peca, grau_indice))
            if area:
                return list(ifp), Polygon(ifp).area
            else:
                return list(ifp)


        ocupado = None
        chaves = []
        nfps = []   

        for x2, y2, grau1, pol in self.indices_pecas_posicionadas:
            chave = (
                tuple(self.nova_lista_original[pol]), grau1,
                tuple(self.nova_lista[peca]), grau_indice
            )
            chaves.append((chave,x2,y2))
            prefixo_t = tuple(chaves)

            if prefixo_t in self.dict_nfps:
                # já calculei essa união antes
                # print(1)
                ocupado = self.dict_nfps[prefixo_t]
            else:
                # cria o polígono deslocado
                # print(2)
                base_nfp = self.tabela_nfps[chave]
                p = Polygon([(x + x2, y + y2) for x, y in base_nfp])
                nfps.append(p)

                # une incrementalmente
                if ocupado is None:
                    ocupado = p
                    # print(11111111111111111111111111111111111)
                else:
                    ocupado = unary_union([ocupado,p])    

                # cacheia para esse prefixo
                # occupied = unary_union([ocupado])
                self.dict_nfps[prefixo_t] = ocupado    

        # bf = unary_union(nfps)
        # print("igual brute-force?", bf.equals(ocupado))





        if bin == False:
            ifp_coords = self.ifp(self.rot_pol(peca, grau_indice))
        else:
            # print(1)
            ifp_coords = self.ifp(self.rot_pol(peca, grau_indice), bin)
            # ifp_coords = list(set(ifp_coords))
            # print(ifp_coords)
            

    
        # print(ocupado)
        # supondo que ifp e ocupado já sejam geometrias Shapely
        intersec = Polygon(ifp_coords).boundary.intersection(ocupado.boundary)
        pts = []
        if intersec.geom_type == 'Point':
            pts = [(intersec.x, intersec.y)]
        else:
            for part in getattr(intersec, 'geoms', [intersec]):
                if hasattr(part, 'coords'):
                    for x, y in part.coords:
                        pts.append((x, y))


        # ocupado.buffer(-1)
        encaixes = Polygon(ifp_coords).difference(ocupado)
        # print(encaixes)

        vertices = extrair_vertices(encaixes)
        for cor in pts:
            vertices.append(cor)


        # print(vertices)


        


        if area:
            return vertices, encaixes.area
        else:
            
            return vertices

    def ifp(self, peca, bin = False):
        if not bin:
            maxx = max([x for x,y in peca])
            maxy = max([y for x,y in peca])

            minx = min([x for x,y in peca])
            miny = min([y for x,y in peca])

            cords = self.cordenadas_area

            v0 = (cords[0][0]- minx , cords[0][1] - maxy)
            v1 = (cords[1][0]- maxx , cords[1][1] - maxy)
            v2 = (cords[2][0]- maxx , cords[2][1] - miny)
            v3 = (cords[3][0]- minx , cords[3][1] - miny)
            ifp = [v0,v1,v2,v3]

            # print("IFP",ifp)
            
            return ifp
        else:
            maxb = max([x for x,y in bin])
            minb = min([x for x,y in bin])
            
            maxx = max([x for x,y in peca])
            maxy = max([y for x,y in peca])

            minx = min([x for x,y in peca])
            miny = min([y for x,y in peca])

            if (maxx - minx) > (maxb - minb):
                return []

            largura = maxx - minx
            altura = maxy - miny

            cords = bin

            v0 = (cords[0][0]- minx , cords[0][1] - maxy)
            v1 = (cords[1][0]- maxx , cords[1][1] - maxy)
            v2 = (cords[2][0]- maxx , cords[2][1] - miny)
            v3 = (cords[3][0]- minx , cords[3][1] - miny)
            ifp = [v0,v1,v2,v3]

            # print("IFP",ifp)
            
            return ifp
    def resetar(self):
        for i in range(len(self.pecas_posicionadas)):
            self.remover_da_area()

    def atualizar_dados(self):
        self.area_ocupada = sum([calcular_area(pol) for pol in self.pecas_posicionadas])
        self.vertices_fecho, self.fecho = calcular_fecho_e_area(self.pecas_posicionadas)
        self.atualizar_matriz()
        
        if self.render:
            turtle.tracer(0)
            self.turtle_fecho.clear()
            self.turtle_dados.clear()
            
            self.turtle_dados.penup()
            self.turtle_dados.goto(-925,350)
            self.turtle_dados.pendown()
            if self.fecho > 0:
                self.turtle_dados.write(f"Preenchimento fecho = {round(((self.area_ocupada)/self.fecho)*100, 2)}%", font=("Arial",16, "normal"))
            self.turtle_dados.penup()
            self.turtle_dados.goto(-925,450)
            self.turtle_dados.pendown()

            self.turtle_dados.write(f"Preenchimento total: {(round((self.area_ocupada/self.area)*100,2))}%", font=("Arial",16, "normal"))
            self.turtle_dados.penup()
            self.turtle_dados.goto(-925,400)
            self.turtle_dados.pendown()
            self.turtle_dados.write(f"Peças Disponiveis: {len(self.lista)}", font=("Arial",16, "normal"))
            self.turtle_dados.hideturtle()

              
    def posicionar_turtle(self, poli, p , fill =True, color = 'orange'):
        if fill:
            p.begin_fill()
            p.fillcolor(color)
        turtle.tracer(0)
        p.penup()
        p.goto(poli[0])
        p.pendown()                
        for cor in poli:
            p.goto(cor)

        p.goto(poli[0])
        if fill:
            p.end_fill()
        p.hideturtle()

        
    def CordenadaProibida(self,x,y):
        if (not ponto_dentro_poligono(x, y, self.cordenadas_area, True)):
            return True
        else:
            for pol in self.pecas_posicionadas:
                if ponto_dentro_poligono(x, y, pol,False):
                    return True
    
            return False 
    
    def remover_lista(self,peca):
        self.lista_removida.append([self.lista[peca], self.nova_lista[peca], self.nova_lista_completa[peca]])
        
        self.lista.pop(peca)
        self.nova_lista.pop(peca)
        self.nova_lista_completa.pop(peca)
  
    def remover_da_area(self):
        
        peca = -1
        if self.pecas_posicionadas:
            self.pecas_posicionadas.pop(peca)
            self.indices_pecas_posicionadas.pop(peca)
            
            self.lista.append(self.lista_removida[peca][0])           
            self.nova_lista.append(self.lista_removida[peca][1])
            self.nova_lista_completa.append(self.lista_removida[peca][2])
            
            self.restaurar_ordem_original()
            
            self.lista_removida.pop(peca)
            
            if self.render:
                self.lista_turtle[peca].clear()
                self.lista_turtle.pop(peca)
                
            self.atualizar_dados()
        
            
    def restaurar_ordem_original(self):
        # Função auxiliar para lidar com itens repetidos
        def restaurar_lista(lista_original, lista_atual):
            lista_restaurada = []
            # Copiar lista atual para contagem correta de repetidos
            lista_atual_copy = lista_atual[:]
            
            # Percorrer lista_original de trás para frente
            for item in reversed(lista_original):
                if item in lista_atual_copy:
                    # Inserir o item no início da lista restaurada para manter a ordem
                    lista_restaurada.insert(0, item)
                    lista_atual_copy.remove(item)  # Remove uma ocorrência do item
                    
            return lista_restaurada

        # Reorganizando self.lista com base em self.lista_original, lidando com repetições
        self.lista = restaurar_lista(self.lista_original, self.lista)
        
        # Reorganizando self.nova_lista com base em self.nova_lista_original
        self.nova_lista = restaurar_lista(self.nova_lista_original, self.nova_lista)
        
        # Reorganizando self.nova_lista_completa com base em self.nova_lista_completa_original
        self.nova_lista_completa = restaurar_lista(self.nova_lista_completa_original, self.nova_lista_completa)
      
    def posicao_disponivel(self,peca,grau,x,y, pontos_verificação):
        
        Dentro = True
        for x1,y1 in pontos_verificação:
            if not ponto_dentro_poligono(x1,y1,self.cordenadas_area, True):
                Dentro = False
        
        if len(self.pecas_posicionadas) == 0:
            return Dentro
        else:
            nfp = self.nfp(peca, grau)
            if not ponto_dentro_poligono(x,y,nfp,False):
                return False
            else:
                return Dentro
  
    def renderizar(self):
        turtle.tracer(0)
        t  = turtle.Turtle()
        t.color('red')
        t.begin_fill()
        t.penup()
        t.goto(self.x, self.y)
        t.pendown()
        
        for cor in self.cordenadas_area:
            t.goto(cor)

        t.goto(self.cordenadas_area[0])
        t.end_fill()
        t.hideturtle()

    def _plot(self):
        self._ax.clear()
        self._ax.imshow(self._matriz)
        plt.pause(0.001)
    
    def transformar_coordenadas(self, x, y):
        x1,y1 = transformar_coordenadas_inversa(x, y, self.x, (self.x + self.base), (self.y - self.altura), self.y, self.base, self.altura)
        return x1, -y1
    def atualizar_matriz(self):          
        self._img = Image.new('L', (int(self.base), int(self.altura)), 0)
        for poligono in self.pecas_posicionadas:
            poligono_transformado = [transformar_coordenadas(x, y, self.x, (self.x + self.base), (self.y - self.altura), self.y, self.base, self.altura) for x, y in poligono]
            ImageDraw.Draw(self._img).polygon(poligono_transformado, outline=1, fill=1)
        self._matriz = np.array(self._img)
        
        if self.plot:
            self._plot()
        
    def instancias(self):
        if self.pecas == 'fu':
            self.base = 340
            self.altura = 380
            self.Escala = 10
            self.rotacoes = [0,1,2,3]
            self.graus = [0,1,2,3]
            return True
            
        elif self.pecas == 'jackobs1':
            self.base = 400
            self.altura = 130
            self.Escala = 10
            self.rotacoes = [0,1,2,3]
            self.graus = [0,1,2,3]
            return True

            
        elif self.pecas == 'jackobs2':
            self.base = 700
            self.altura = 280
            self.Escala = 10
            self.rotacoes = [0,1,2,3]
            self.graus = [0,1,2,3]
            return True

            
        elif self.pecas == 'shapes0':
            self.altura = 400
            self.base = 630
            self.Escala = 10
            self.rotacoes = [0]
            self.graus = [0]            
            return True

            
        elif self.pecas == 'shapes1':
            self.altura = 400
            self.base = 590
            self.Escala = 10
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True

            
        elif self.pecas == 'shapes2':
            self.base = 270
            self.altura = 150
            self.Escala = 10
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True


        elif self.pecas == 'dighe1':
            self.altura = 300
            self.base = 414
            self.Escala = 3
            self.rotacoes = [0]
            self.graus = [0]
            return True

            
        elif self.pecas == 'dighe2':
            self.base = 300
            self.altura = 402
            self.Escala = 3
            self.rotacoes = [0]
            self.graus = [0]
            return True


        elif self.pecas == 'albano':
            self.altura = 350
            self.base = 723
            self.Escala = (1/14)
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True


        elif self.pecas == 'dagli':
            self.altura = 600
            self.base = 660
            self.Escala = 10
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True


        elif self.pecas == 'mao':
            self.altura = 425
            self.base = 343
            self.Escala = 1/6
            self.rotacoes = [0,1,2,3]
            self.graus = [0,1,2,3]
            return True


        elif self.pecas == 'marques':
            self.altura = 104
            self.base = 84
            self.Escala = 1
            self.rotacoes = [0,1,2,3]
            self.graus = [0,1,2,3]
            return True

            
        elif self.pecas == 'shirts':
            self.altura = 400
            self.base = 630
            self.Escala = 10
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True

            
        elif self.pecas == 'swim':
            self.altura = 719
            self.base = 821
            self.Escala = 1/8
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True

            
        elif self.pecas == 'trousers':
            self.altura = 79
            self.base = 246
            self.Escala = 1
            self.rotacoes = [0,2]
            self.graus = [0,2]
            return True


        else:
            self.rotacoes = [0,1,2,3]
            self.graus = [0,1,2,3]
            return False

    def draw_click(self,x1,y1, grau_indice,n,flip):
        graus = [0,90,180,270]
        grau = graus[grau_indice]
        x, y = x1,y1
        x_escala = 0
        y_escala = 0
        if len(self.lista) > 0 and n < len(self.lista):          
            pol = self.lista[n]
            if flip:
                pol = flip_polygon(pol)
            turtle.tracer(0)
            turtle.clear()
            turtle.begin_fill()
            turtle.fillcolor("green")
            turtle.penup()
            x_rot, y_rot = rotate_point(pol[0][0], pol[0][1], grau)
            turtle.goto(x+x_rot*self.Escala-x_escala, -y+y_rot*self.Escala+y_escala)
            turtle.pendown()
            for cor in pol:

                x_rot, y_rot = rotate_point(cor[0], cor[1], grau)
                turtle.goto(x+x_rot*self.Escala-x_escala, -y+y_rot*self.Escala+y_escala)
            turtle.goto(x+x_rot*self.Escala-x_escala, -y+y_rot*self.Escala+y_escala)
            turtle.end_fill()
            turtle.hideturtle()
            turtle.tracer(1)

      
    def mais_g(self,x,y):
        self.g += 1
        if self.g == 4:
            self.g = 0
        
    def mais_n(self,x,y):
        self.n += 1
        if self.n == len(self.nova_lista):
            self.n=0
        turtle.tracer(0)
        self.turtle_n.clear()
        self.turtle_n.penup()
        self.turtle_n.goto(self.x - (self.base/2) -200, self.y - 50)
        self.turtle_n.pendown()

        self.turtle_n.write(f"{self.n}", font=("Arial",16, "normal"))
        self.turtle_n.penup()
        self.turtle_n.hideturtle()
        
    def random_keys(self):
        return np.random.random(self.max_pecas)
    
    def decoder(self, keys):
        sequence = np.argsort(keys)
        return [self.lista_original[i] for i in sequence]
    
    def encoder(self, pecas):
        sequence = [0.99 * ((self.lista_original.index(peca)+1)/self.max_pecas) for peca in pecas]
        for i in range(self.max_pecas - len(sequence)):
            sequence.append(sequence[-1] + 0.01)
        return sequence
        
    
    def empacotar(self, sequence, regra = 'ExSearch', draw = False):
        for peca in sequence:
            idx = self.lista.index(peca)
            pos = self.PackS(idx, regra, draw)
            if pos:
                self.acao(pos[0], pos[1], pos[2], pos[3], pos[4], True)
                  
       
    def posicionar(self, pos):
        self.acao(pos[0], pos[1], pos[2], pos[3], pos[4], True)
    def PackS(self, peca, regra = 'ExSearch', draw = False):
        if len(self.lista) == self.max_pecas:
            x, y = self.cordenadas_area[3]
            first_idx = peca  
            
            minx = min([x for x,y in self.nova_lista[first_idx]]) 
            miny = min([y for x,y in self.nova_lista[first_idx]]) 
            
                
            
            return [peca,x- minx,y- miny,0,False,0,0,self.lista[first_idx]]
        else:
            if regra == 'ExSearch':
                posicoes = []
                for grau in self.rotacoes:
                    pos = self.ExSearch(peca,grau, draw)
                    if pos:
                        posicoes.append(pos)
                        
                if posicoes:
                    melhor = float('-inf')
                    melhor_pos = None
                    for pos in posicoes:
                        if pos[5] > melhor:
                            melhor = pos[5]
                            melhor_pos = pos
                    return melhor_pos
                
                else:
                    return None
                
            elif regra == 'BLF':
                
                posicoes = []
                for grau in self.rotacoes:
                    pos = self.BLF(peca,grau, draw)
                    if pos:
                        posicoes.append(pos)
                        
                if posicoes:
                    melhor = float('-inf')
                    melhor_pos = None
                    for pos in posicoes:
                        if pos[5] > melhor:
                            melhor = pos[5]
                            melhor_pos = pos
                    return melhor_pos
                
                else:
                    return None
            else:
                return None
     
    def GreedyIniSol(self, regra = 'ExSearch', draw = False, p = 0.1):
        cabe_peca = True
        solucao = []
        possiveis_pecas = []
        pecas_aleatoiras = math.ceil(self.max_pecas*p)
        
        if pecas_aleatoiras == 0:
            maior_area = 0
            maior_peca = None
            for i in range(len(self.lista)):
                area = Polygon(self.lista[i]).area
                if area > maior_area:
                    maior_area = area
                    maior_peca = i
                    print(maior_area, maior_peca)
                
                
                
            self.PackS(5, regra, draw)
        else:
            self.PackS(random.randint(0,self.max_pecas - 1), regra, draw)
            pecas_aleatoiras-=1
        
        while cabe_peca:
            possiveis_pecas = []
            for i in range(len(self.lista)):
                    pos = self.PackS(i, regra, draw)
                    if pos is not None:
                        possiveis_pecas.append(pos)
                        
            if possiveis_pecas:
                melhor = float('-inf')
                melhor_pos = None
                for pos in possiveis_pecas:
                    if pos[5] > melhor:
                        melhor = pos[5]
                        melhor_pos = pos
                        
                if pecas_aleatoiras == 0:
                    solucao.append(melhor_pos[-1])
                    self.acao(melhor_pos[0], melhor_pos[1], melhor_pos[2], melhor_pos[3], melhor_pos[4], True)
                else:
                    if random.random() > 0.5:
                        solucao.append(melhor_pos[-1])
                        self.acao(melhor_pos[0], melhor_pos[1], melhor_pos[2], melhor_pos[3], melhor_pos[4], True)
                    else:
                        melhor_pos = possiveis_pecas[random.randint(0, len(possiveis_pecas)-1)]
                        solucao.append(melhor_pos[-1])
                        self.acao(melhor_pos[0], melhor_pos[1], melhor_pos[2], melhor_pos[3], melhor_pos[4], True)
                        pecas_aleatoiras -= 1
            else:
                cabe_peca = False
                break
            
        
        return solucao
           
    def vizinhos(self,keys):
        new_keys = copy.deepcopy(keys)
        prob = random.random()
        if  prob > 0.5:
            print("1 ", end="")
            idx = random.randint(0,len(keys)-1)
            new_keys[idx] = random.random()
            
            idx = random.randint(0,len(keys)-1)
            new_keys[idx] = random.random()
            
        elif prob > 0.2:
            print("2 ", end="")
            for i, key in enumerate(new_keys):
                if random.random() > 0.5:
                    new_keys[i] = key + random.uniform(-0.5*key, 0.5*(1-key))
            
        else:
            print("3 ", end="")
            for i, key in enumerate(new_keys):
                if random.random() > 0.5:
                    new_keys[i] = random.random()
                    
        return new_keys
             
    def LocSearch(self,x, keys, regra = 'ExSearch', draw = False):
        best_keys = keys
        melhor_sol = self.decoder(best_keys)
        self.empacotar(melhor_sol, regra, draw)
        melhor_area = self.area_ocupada/self.area
        self.resetar()
        iteracao = 0
        while iteracao < x:
            iteracao += 1
            
            
            new_keys = self.vizinhos(best_keys)
            
            sol = self.decoder(new_keys)
            self.empacotar(sol, regra, draw)
            
            area = self.area_ocupada/self.area
            print(f"Iteração {iteracao}, melhor area = {round(melhor_area,4)*100}, P = {len(self.pecas_posicionadas)}/{self.max_pecas}, fecho = {round(self.area_ocupada/self.fecho,4)*100} area atual = {round(area, 4)*100}, {[round(key,4) for key in new_keys]}")
            if area > melhor_area:
                best_keys = new_keys
                iteracao = 0
                melhor_area = area
                melhor_sol = sol
                if len(self.lista) == 0:
                    print("Solução encontrada")
                    self.resetar()
                    return best_keys
                
            self.resetar()
        return best_keys
              
    def GRASP(self,x = 30, max_iter = 80, p = 0.1, regra = 'ExSearch', draw = False):     
        melhor_sol = None
        melhor_area = float('-inf')         
        for i in range(max_iter):
            
            inisol = self.GreedyIniSol(regra, draw, p)
            area = self.area_ocupada/self.area
            if area > melhor_area:
                melhor_area = area
                melhor_sol = inisol
                if len(self.lista) == 0:
                    print("Solução encontrada")
                    break
            self.resetar()
            
            keys = self.encoder(inisol)
            sol = self.LocSearch(x,keys, regra, draw)           
            pecas = self.decoder(sol)
            
            self.empacotar(pecas, regra, draw)
            area = self.area_ocupada/self.area
            if area > melhor_area:
                melhor_area = area
                melhor_sol = pecas
                if len(self.lista) == 0:
                    print("Solução encontrada")
                    break
            self.resetar()
        self.resetar()
        return melhor_sol
            

            
            
            
   
             
         
    def on_click(self,x,y):
 
        if self.render:
            
            if self.botao_nfp1.clicou(x,y):
                self.nofit = not self.nofit
                if self.nofit:
                
                    nfp = self.nfp(self.n, self.g, proj=False)
                    self.posicionar_turtle(nfp, self.Tnfp, False)
                else:
                    self.Tnfp.clear()
                return
            
            if self.botao_nfp2.clicou(x,y):
                coords_bin = copy.deepcopy(self.cordenadas_area)
                pol = self.pecas_posicionadas[-1]
                piece = self.rot_pol(self.n,self.g)
                x1 = self.indices_pecas_posicionadas[-1][0]
                maxx = max([x for x,y in pol])
                minxx = min([x for x,y in pol])

                fim_coluna = maxx - minxx
                coords_bin[0][0] = x1
                coords_bin[1][0] = x1 + (fim_coluna)
                coords_bin[2][0] = x1 + (fim_coluna)
                coords_bin[3][0] = x1
                self.nofit = not self.nofit
                if self.nofit:
                
                    ifp = self.ifp(piece, bin=coords_bin)
                    self.posicionar_turtle(ifp, self.Tnfp, False)
                    nfp = self.nfp(self.n, self.g, bin=coords_bin)
                    # self.posicionar_turtle(coords_bin, self.Tnfp, False)
                    
                    # nfp = Polygon(nfp).intersection(Polygon(ifp))
                    # nfp = extrair_vertices(nfp)
                    # self.posicionar_turtle(nfp, self.Tnfp, False)
                    # self.posicionar_turtle(coords_bin, self.Tnfp, False)
                else:
                    self.Tnfp.clear()
                return
            
            if self.botao_draw.clicou(x,y):
                self.d = not self.d
                return
            
            if self.botao_ch.clicou(x,y):
                self.ch = not self.ch
                if self.ch:
                
                    
                    desenhar_fecho(self.vertices_fecho,self.Tch)
                else:
                    self.Tch.clear()
                
                return
            
            if self.botao_pmais.clicou(x,y):
                self.n += 1
                if self.n == len(self.nova_lista):
                    self.n=len(self.nova_lista)-1
                turtle.tracer(0)
                self.turtle_n.clear()
                self.turtle_n.penup()
                self.turtle_n.goto(self.x - (self.base/2) -200, self.y - 50)
                self.turtle_n.pendown()

                self.turtle_n.write(f"{self.n}", font=("Arial",16, "normal"))
                self.turtle_n.penup()
                self.turtle_n.hideturtle()
                return
            if self.botao_pmenos.clicou(x,y):
                self.n -= 1
                if self.n == -1:
                    self.n=0
                
                turtle.tracer(0)
                self.turtle_n.clear()
                self.turtle_n.penup()
                self.turtle_n.goto(self.x - (self.base/2) -200, self.y - 50)
                self.turtle_n.pendown()

                self.turtle_n.write(f"{self.n}", font=("Arial",16, "normal"))
                self.turtle_n.penup()
                self.turtle_n.hideturtle()
                return
            
            if self.botao_intmais.clicou(x,y):
                self.intense_nfp += 1
                if self.intense_nfp == 6:
                    self.intense_nfp=5
                    
                turtle.tracer(0)
                self.turtle_inter.clear()
                self.turtle_inter.penup()
                self.turtle_inter.goto(self.x - (self.base/2) -200, self.y - 250)
                self.turtle_inter.pendown()

                self.turtle_inter.write(f"{self.intense_nfp}", font=("Arial",16, "normal"))
                self.turtle_inter.penup()
                self.turtle_inter.hideturtle()
                return
            if self.botao_intmenos.clicou(x,y):
                self.intense_nfp -= 1
                if self.intense_nfp == -1:
                    self.intense_nfp=0
                turtle.tracer(0)
                self.turtle_inter.clear()
                self.turtle_inter.penup()
                self.turtle_inter.goto(self.x - (self.base/2) -200, self.y - 250)
                self.turtle_inter.pendown()

                self.turtle_inter.write(f"{self.intense_nfp}", font=("Arial",16, "normal"))
                self.turtle_inter.penup()
                self.turtle_inter.hideturtle()
                return
            
            if self.botao_remover.clicou(x,y):
                self.n = 0
                self.remover_da_area()
                return
            
            if self.botao_reset.clicou(x,y):
                self.n = 0
                self.resetar()
                return
            
            if self.botao_ex.clicou(x,y):
                
                if len(self.lista) == self.max_pecas:
                    x, y = self.cordenadas_area[3]
                    first_idx = self.n   
                    
                    minx = min([x for x,y in self.nova_lista[first_idx]]) 
                    miny = min([y for x,y in self.nova_lista[first_idx]]) 
                    
                
                    peca1 = [first_idx, x - minx, y - miny, 0, 0, self.lista[first_idx]]
                    self.acao(first_idx, x - minx, y - miny, 0, False)
                    
                else:
                    pos = self.ExSearch(self.n,self.g, self.d, self.intense_nfp)
                    self.acao(pos[0], pos[1], pos[2], 
                                        pos[3], pos[4], True)
            
                if self.n > 0:
                    self.n -=1
                return
            if self.botao_blf.clicou(x,y):
                
                if len(self.lista) == self.max_pecas:
                    x, y = self.cordenadas_area[3]
                    first_idx = self.n   
                    
                    minx = min([x for x,y in self.nova_lista[first_idx]]) 
                    miny = min([y for x,y in self.nova_lista[first_idx]]) 
                    
                
                    peca1 = [first_idx, x - minx, y - miny, 0, 0, self.lista[first_idx]]
                    self.acao(first_idx, x - minx, y - miny, 0, False)
                    
                else:
                    pos = self.BLF(self.n,self.g, self.d, self.intense_nfp)
                    self.acao(pos[0], pos[1], pos[2], 
                                        pos[3], pos[4], True)
            
                
                if self.n > 0:
                    self.n -=1
                return
        
        numero_pecas = len(self.lista)
        self.acao(self.n,x,y,self.g, False)
        if numero_pecas > len(self.lista):
            if self.n > 0:
                self.n -=1
            
    def click(self):
        self.loop = True
        self.n = 0
        self.g = 0
        self.d = False
        self.nofit = False
        self.Tch = turtle.Turtle()
        self.Tnfp = turtle.Turtle()
        self.turtle_inter = turtle.Turtle()
        self.turtle_n = turtle.Turtle()
        self.ch = False
        self.intense_nfp = 1
        turtle.tracer(0)
        self.turtle_inter.clear()
        self.turtle_inter.penup()
        self.turtle_inter.goto(self.x - (self.base/2) -200, self.y - 250)
        self.turtle_inter.pendown()

        self.turtle_inter.write(f"{self.intense_nfp}", font=("Arial",16, "normal"))
        self.turtle_inter.penup()
        self.turtle_inter.hideturtle()
        
        turtle.tracer(0)
        self.turtle_n.clear()
        self.turtle_n.penup()
        self.turtle_n.goto(self.x - (self.base/2) -200, self.y - 50)
        self.turtle_n.pendown()

        self.turtle_n.write(f"{self.n}", font=("Arial",16, "normal"))
        self.turtle_n.penup()
        self.turtle_n.hideturtle()
        while self.loop:
    
            turtle.onscreenclick(self.mais_g,3)
            turtle.onscreenclick(self.mais_n,2)
            turtle.onscreenclick(self.on_click)

            x1,y1 = pyautogui.position()
            x1 -= 963
            y1 -= 533
             
            self.draw_click(x1,y1,self.g,self.n, False)
            
            if len(self.nova_lista)==0:
                self.loop = False
                turtle.clear()
                break


def offset_polygon(vertices, offset):
    """
    Cria um novo polígono com offset a partir de um polígono original usando Shapely
    
    Args:
        vertices: Lista de tuplas (x, y) representando os vértices do polígono
        offset: Valor do offset (positivo para expandir, negativo para contrair)
    
    Returns:
        Lista de tuplas (x, y) representando os vértices do novo polígono
    """
    if offset > 0:
        # Cria um polígono Shapely
        poly = Polygon(vertices)
        
        # Verifica se o polígono é válido
        if not poly.is_valid:
            return vertices
        
        # Aplica o buffer (offset)
        # join_style=1 (round) para suavizar cantos
        # mitre_limit controla quanto os cantos podem se estender
        buffered = poly.buffer(offset, join_style=1, mitre_limit=2.0)
        
        # Se o resultado for vazio ou inválido, retorna o original
        if buffered.is_empty or not buffered.is_valid:
            return vertices
        
        # Extrai os vértices do polígono resultante
        if buffered.geom_type == 'Polygon':
            # Pega apenas o exterior do polígono
            new_vertices = list(buffered.exterior.coords)[:-1]  # Remove o último ponto (duplicado)
        else:
            # Se o resultado for um MultiPolygon, pega o maior polígono
            largest = max(buffered.geoms, key=lambda x: x.area)
            new_vertices = list(largest.exterior.coords)[:-1]
        
        return new_vertices
    
    else:
        return vertices

def pre_processar_NFP(rotacoes, lista_pecas,offset):
    tabela_nfps = {}
    lista_unica = []
    for peca in lista_pecas:
        if peca not in lista_unica:
            lista_unica.append(peca)
    
    # Calcula o total de iterações
    total = len(lista_unica) * len(rotacoes) * len(lista_unica) * len(rotacoes)
    atual = 0


    
    for pecaA in lista_unica:
        for grauA in rotacoes:
            for pecaB in lista_unica:
                for grauB in rotacoes:
                    # Atualiza e mostra o progresso
                    atual += 1
                    porcentagem = (atual / total) * 100
                    print(f"\rPré-processando NFPs: {porcentagem:.1f}% concluído", end="")
                    
                   
                    chave = (tuple(pecaA), grauA, tuple(pecaB), grauB)
                    nfp = NFP(pecaA, grauA, pecaB, grauB)
                 
                    tabela_nfps[chave] = offset_polygon(nfp,offset)


    
   
    return tabela_nfps


def flip_polygon(polygon, axis='y'):
    """
    Flipa o polígono ao longo do eixo x ou y.
    
    Args:
        polygon: Lista de tuplas representando os vértices [(x1, y1), (x2, y2), ...].
        axis: Eixo de reflexão, 'x' para flipar ao longo do eixo x, ou 'y' para o eixo y.
        
    Returns:
        Lista de vértices do polígono flipado.
    """
    if axis == 'x':
        # Reflete ao longo do eixo x: inverte o sinal da coordenada y
        return [(x, -y) for x, y in polygon]
    elif axis == 'y':
        # Reflete ao longo do eixo y: inverte o sinal da coordenada x
        return [(-x, y) for x, y in polygon]
    else:
        raise ValueError("Eixo inválido. Use 'x' ou 'y'.")

from shapely.geometry import Point, Polygon
import random

def suavizar_poligono(index, poligonos, iteracoes=1, tamanho_kernel=5, area_minima=50, epsilon=5.0):
    """
    Suaviza um polígono e garante que a geometria resultante seja válida.
    
    Args:
        index: índice do polígono na lista
        poligonos: lista de polígonos
        iteracoes: número de iterações de suavização
        tamanho_kernel: tamanho do kernel para operações morfológicas
        area_minima: área mínima para filtrar polígonos
        epsilon: parâmetro de aproximação do polígono
    
    Returns:
        Lista de polígonos suavizados e validados
    """
    if index < 0 or index >= len(poligonos):
        print(f"Índice inválido. Escolha um índice entre 0 e {len(poligonos) - 1}.")
        return []

    # Selecionar o polígono
    poligono = poligonos[index]
    
    # Verificar se o polígono tem pontos suficientes
    if len(poligono) < 3:
        print("Polígono inválido: precisa ter pelo menos 3 pontos")
        return []

    # Determinar o tamanho da matriz de visualização com margem
    max_x = int(max(pt[0] for pt in poligono)) + 50
    max_y = int(max(pt[1] for pt in poligono)) + 50
    min_x = int(min(pt[0] for pt in poligono)) - 50
    min_y = int(min(pt[1] for pt in poligono)) - 50
    
    width = max_x - min_x
    height = max_y - min_y

    # Criar uma matriz binária
    canvas = np.zeros((height, width), dtype=np.uint8)
    
    # Ajustar coordenadas para o novo sistema
    adjusted_poly = np.array([(pt[0] - min_x, pt[1] - min_y) for pt in poligono], dtype=np.int32)
    
    # Preencher o polígono na matriz
    cv2.fillPoly(canvas, [adjusted_poly], 255)
    
    # Aplicar abertura morfológica para remover ruídos
    kernel = np.ones((tamanho_kernel, tamanho_kernel), np.uint8)
    for i in range(iteracoes):
        canvas = cv2.morphologyEx(canvas, cv2.MORPH_OPEN, kernel)
        canvas = cv2.morphologyEx(canvas, cv2.MORPH_CLOSE, kernel)

    # Encontrar novos contornos após a abertura
    contornos, _ = cv2.findContours(canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar e simplificar os contornos
    novos_poligonos = []
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area >= area_minima:
            # Suavizar o contorno com aproximação de polígonos
            epsilon_value = epsilon * (cv2.arcLength(contorno, True) / 100)
            contorno_suavizado = cv2.approxPolyDP(contorno, epsilon_value, True)
            
            # Converter de volta para o sistema de coordenadas original
            pontos_ajustados = [(pt[0] + min_x, pt[1] + min_y) for pt in contorno_suavizado.reshape(-1, 2)]
            
            # Validar o polígono resultante
            if len(pontos_ajustados) >= 3:  # Verificar se tem pelo menos 3 pontos
                # Verificar se o polígono não tem auto-interseções
                poly = Polygon(pontos_ajustados)
                if poly.is_valid:
                    novos_poligonos.append(pontos_ajustados)
                else:
                    # Tentar corrigir o polígono
                    poly_corrigido = poly.buffer(0)
                    if poly_corrigido.is_valid:
                        coords = list(poly_corrigido.exterior.coords)[:-1]  # Remover o último ponto (duplicado)
                        novos_poligonos.append(coords)

   
        
    
    return novos_poligonos

def pontos_no_poligono(pontos_poligono, num_pontos=100):
    # Criar o objeto Polígono a partir dos pontos
    poligono = Polygon(pontos_poligono)

    # Ponto central (mesmo cálculo que já foi feito)
    xs = [x for x, y in pontos_poligono]
    ys = [y for x, y in pontos_poligono]
    centro_x = sum(xs) / len(xs)
    centro_y = sum(ys) / len(ys)
    ponto_central = (centro_x, centro_y)

    # Gerar pontos aleatórios dentro do polígono
    pontos_internos = []
    min_x, min_y, max_x, max_y = poligono.bounds
    while len(pontos_internos) < num_pontos:
        # Gerar coordenadas aleatórias dentro dos limites do polígono
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if poligono.contains(random_point):
            pontos_internos.append((random_point.x, random_point.y))

    return [ponto_central] + pontos_internos


def ajustar_poligono(poligono):
    # Encontrar o primeiro vértice
    if poligono[0][0] == 0 and poligono[0][1] == 0:
        return poligono
    else:
        x_min = poligono[0][0]
        y_min = poligono[0][1]
        
        # Transladar todos os vértices para garantir que o primeiro ponto seja (0,0)
        poligono_ajustado = [(x - x_min, y - y_min) for (x, y) in poligono]
        
        return poligono_ajustado 

    
def rotate_point(x, y, angle):
    rad = math.radians(angle)
    x_new = x * math.cos(rad) - y * math.sin(rad)
    y_new = x * math.sin(rad) + y * math.cos(rad)
    return x_new, y_new
def transformar_coordenadas_inversa(x, y, x_min, x_max, y_min, y_max, width, height):
    x_scaled = (x / width) * (x_max - x_min) + x_min
    y_scaled = ((height - y) / height) * (y_max - y_min) + y_min
    return x_scaled, y_scaled
def pontos_entre_vertices(vertices):
    def mdc(a, b):
        # Função auxiliar para calcular o MDC (Máximo Divisor Comum)
        while b:
            a, b = b, a % b
        return a

    pontos = []
  
    # Adiciona o último vértice ao início para conectar o último ao primeiro
    vertices = vertices + [vertices[0]]

    for i in range(len(vertices) - 1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        # Calcula as diferenças
        dx = x2 - x1
        dy = y2 - y1
        # Calcula o MDC das diferenças
        passo_mdc = mdc(abs(dx), abs(dy))
        # Calcula os incrementos
        inc_x = dx // passo_mdc if passo_mdc != 0 else 0
        inc_y = dy // passo_mdc if passo_mdc != 0 else 0
        # Adiciona os pontos à lista
        for j in range(0, passo_mdc + 1):  # Inclui o ponto final
            ponto = (x1 + j * inc_x, y1 + j * inc_y)
            pontos.append(ponto)

    return pontos
from shapely.geometry import Polygon

def tratar_lista(lista_poligonos, Escala):
    def remove_vertices_repetidos(polygon):
        seen = set()
        unique_polygon = []
        for vertex in polygon:
            if vertex not in seen:
                unique_polygon.append(vertex)
                seen.add(vertex)
        return unique_polygon
    
    nova_lista = []
    nova_lista_completa = []
    
    for pol in lista_poligonos:
        novo_pol = []
        
        # Escalando os vértices
        for cor in pol:
            novo_pol.append((int(cor[0] * Escala), int(cor[1] * Escala)))
        
        # Removendo qualquer vértice repetido
        novo_pol = remove_vertices_repetidos(novo_pol)
        
        
        # Gerando pontos intermediários
        pol_completo = pontos_entre_vertices(novo_pol)
        nova_lista_completa.append(pol_completo)
        nova_lista.append(novo_pol)
    
    return nova_lista, nova_lista_completa


    
def ler_poligonos(arquivo):
    with open(arquivo, 'r') as f:
        conteudo = f.read().strip()

    # Divide o conteúdo em linhas
    linhas = conteudo.split('\n')

    # Lê o número total de polígonos
    num_poligonos = int(linhas[0].strip())
    #print(f"Número total de polígonos: {num_poligonos}")

    poligonos = []
    i = 1  # Começa a leitura a partir da segunda linha

    while i < len(linhas):
        # Verifica se a linha não está vazia
        if linhas[i].strip():
            try:
                # Lê o número de vértices
                num_vertices = int(linhas[i].strip())
                #print(f"Lendo polígono com {num_vertices} vértices")  # Depuração
                i += 1

                # Lê os vértices
                vertices = []
                for _ in range(num_vertices):
                    # Verifica se a linha não está vazia
                    while i < len(linhas) and not linhas[i].strip():
                        i += 1
                    if i < len(linhas):
                        coords = linhas[i].strip().split()
                        if len(coords) != 2:
                            raise ValueError(f"Esperado 2 valores por linha, mas obteve {len(coords)}: '{linhas[i].strip()}'")
                        x, y = map(float, coords)
                        vertices.append((x, y))
                        i += 1
                    else:
                        raise ValueError(f"Esperado {num_vertices} vértices, mas o arquivo terminou prematuramente.")

                poligonos.append(vertices)
            except ValueError as ve:
                print(f"Erro ao processar a linha {i}: {linhas[i].strip()} - {ve}")
                i += 1
        else:
            i += 1
    if num_poligonos == len(poligonos):
        pass
        #print(f'Todos os {num_poligonos} poligonos foram lidos com sucesso!')
    return poligonos
def ponto_dentro_poligono(x, y, poligono, tag):
    def ponto_na_aresta(px, py, p1, p2):
        # Verifica se o ponto (px, py) está na aresta definida por p1 e p2
        if p1[1] == p2[1]:  # Verifica horizontal
            if p1[1] == py and min(p1[0], p2[0]) <= px <= max(p1[0], p2[0]):
                return True
        if p1[0] == p2[0]:  # Verifica vertical
            if p1[0] == px and min(p1[1], p2[1]) <= py <= max(p1[1], p2[1]):
                return True
        # Verifica diagonal
        if min(p1[0], p2[0]) <= px <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= py <= max(p1[1], p2[1]):
            if (p2[0] - p1[0]) * (py - p1[1]) == (px - p1[0]) * (p2[1] - p1[1]):
                return True
        return False

    n = len(poligono)
    dentro = False

    p1x, p1y = poligono[0]
    for i in range(n + 1):
        p2x, p2y = poligono[i % n]
        
        # Verifica se o ponto está na borda do polígono
        if ponto_na_aresta(x, y, (p1x, p1y), (p2x, p2y)):
            return tag
        
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        dentro = not dentro
        p1x, p1y = p2x, p2y

   
    return dentro
def transformar_coordenadas(x, y, x_min, x_max, y_min, y_max, width, height):
    x_scaled = (x - x_min) / (x_max - x_min) * width
    y_scaled = (y - y_min) / (y_max - y_min) * height
    y_scaled = height - y_scaled

    return x_scaled, y_scaled
def calcular_area(vertices):
    num_vertices = len(vertices)
    area = 0

    for i in range(num_vertices):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % num_vertices]  # Próximo vértice (considerando o último vértice conectado ao primeiro)

        area += (x1 * y2) - (x2 * y1)

    return abs(area) / 2
def calcular_fecho_e_area(poligonos):
    if poligonos:
        # Concatenar todos os vértices de todos os polígonos
        vertices = np.concatenate(poligonos, axis=0)
        
        # Calcular o fecho convexo
        fecho = ConvexHull(vertices)
        
        # Obter os vértices do fecho convexo
        vertices_fecho = vertices[fecho.vertices]
        
        # Calcular a área do fecho convexo
        area = fecho.volume
        
        return vertices_fecho, area
    else:
        return None, 0
    
def desenhar_fecho(vertices_fecho, p):
    if vertices_fecho is not None:
        turtle.tracer(0)
        p.clear()
    
        p.speed(5)

        
        # Levantar a caneta antes de mover para a primeira coordenada
        p.penup()
        p.goto(vertices_fecho[0])
        
        # Abaixar a caneta e começar a desenhar
        p.pendown()
        for cordenada in vertices_fecho[1:]:
            p.goto(cordenada)
        
        # Fechar o polígono voltando ao primeiro vértice
        p.goto(vertices_fecho[0])
        
        # Esconder a tartaruga e terminar o desenho
        p.hideturtle()
        
def calcular_area_preenchida(poligonos):
    area = 0
    for pol in poligonos:
        area += calcular_area(pol)
    return area
def calcular_fecho_area(poligonos):
    if poligonos:
        # Concatenar todos os vértices de todos os polígonos
        vertices = np.concatenate(poligonos, axis=0)
        
        # Calcular o fecho convexo
        fecho = ConvexHull(vertices)
        
        # Obter os vértices do fecho convexo
        vertices_fecho = vertices[fecho.vertices]
        
        # Calcular a área do fecho convexo
        area = fecho.volume
        
        return area
    else:
        return 0        
def area_fecho_retangular(poligonos):
    # Inicializar valores mínimos e máximos
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    
    # Iterar sobre todos os vértices de todos os polígonos
    for poligono in poligonos:
        for (x, y) in poligono:
            # Atualizar os valores mínimos e máximos de x e y
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
    
    # Calcular a largura e altura do fecho retangular
    largura = max_x - min_x
    altura = max_y - min_y
    
    # Calcular a área do fecho retangular
    area = largura * altura
    
    return area

if __name__ == "__main__":
    render = False
    instancias = ["fu","jackobs1","jackobs2","shapes0","shapes1","shapes2","dighe1","dighe2","albano","dagli","mao","marques","shirts","swim","trousers"]


    ins = instancias[0]
    with open(f"nfp_{ins}.txt", "r") as f:
        conteudo = f.read()
    dict_nfp = ast.literal_eval(conteudo)
    env = CSP(dataset=ins,render=render, plot=render, pre_processar=False,tabela=dict_nfp, margem=0)
    start_time = time.time()
    env.GRASP(regra='BLF')
    print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")

    for ins in instancias:

        caminho = f"nfp_{ins}.txt"
        if not os.path.exists(caminho):
            start_time = time.time()
            print(f"\nProcessando instância: {ins}")
            env = CSP(dataset=ins,render=render, plot=render, pre_processar=True, margem=0)
            end_time = time.time()
            print(f"\nTempo de processamento: {end_time - start_time} segundos\n")
            with open(caminho, 'w') as f:
                f.write(str(env.tabela_nfps))
    # tempos = []
    # for i in range(10):
    #     start = time.time()
    #     env.GRASP()
    #     end = time.time()
    #     print(f"Tempo de execução: {end - start:.2f} segundos")
    #     tempos.append(end - start)
        
    # print(f"Tempo médio de execução: {sum(tempos)/len(tempos):.2f} segundos")
    env.click()





