from One_Bin import CSP
import numpy as np
import copy
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPolygon
from RKO import RKO
import math
from shapely import Polygon


CAPACITY = 0
COST = 1

arquivos_bpp = [
    f"Dataset_2D\\2005PisingerSigurd{i}.bpp"
    for i in range(1, 501)
]

def draw_cutting_area(pieces, area_width, area_height, legenda = [], filename=None):
    """
    Desenha a área e peças sem flip nem espelhamento.

    pieces: lista de peças (listas de (x,y))
    area_width, area_height: tamanho do retângulo
    filename: opcional, salva em arquivo
    """
    # acha o mínimo de x e de y
    all_x = [x for p in pieces for x,_ in p]
    all_y = [y for p in pieces for _,y in p]
    min_x, min_y = min(all_x), min(all_y)

    # traduz só pra mover tudo pro canto (0,0)
    translated = [
        [(x - min_x, y - min_y) for x,y in p]
        for p in pieces
    ]

    fig, ax = plt.subplots()
    # retângulo da área
    ax.add_patch(Rectangle((0,0), area_width, area_height,
                           edgecolor='black', facecolor='white'))

    # desenha peças
    for verts in translated:
        color = (173/255, 216/255, 230/255)  # Azul bebê

        poly = MPolygon(verts, closed=True,
                        facecolor=color, edgecolor='black')
        ax.add_patch(poly)

    ax.set_xlim(0, area_width)
    ax.set_ylim(0, area_height)
    ax.set_aspect('equal')

    ax.set_title(legenda)
    plt.tight_layout()

    if filename:
        plt.savefig(filename, dpi=150)
    # plt.show()


import re

def ler_ins(path_arquivo):
    """
    Lê um arquivo de problema de bin packing no formato padrão e retorna:
    
    Returns:
        bins: [((h, w), lucro), …]
        pecas: [{'h': h, 'w': w, 'coords': [(0,0),(w,0),(w,h),(0,h)]}, …]
    """
    with open(path_arquivo, 'r') as f:
        lines = [ln.strip() for ln in f.readlines()]
    
    # Linha 1: número de itens e de bins
    parts = re.findall(r'\d+', lines[1])
    if len(parts) < 2:
        raise ValueError("Não achei nº de itens e bins na linha 1")
    n_items, n_bins = map(int, parts[:2])
    
    # Linha 3: dimensões dos bins (2*n_bins números)
    dims = list(map(int, re.findall(r'\d+', lines[3])))
    if len(dims) < 2 * n_bins:
        raise ValueError(f"Esperava {2*n_bins} números em linha 3, achei {len(dims)}")
    # agrupa de dois em dois: (h, w)
    pares_bins = [(dims[i], dims[i+1]) for i in range(0, 2*n_bins, 2)]
    
    # Linha 4: lucro de cada bin (n_bins números)
    profits = list(map(int, re.findall(r'\d+', lines[4])))
    if len(profits) < n_bins:
        raise ValueError(f"Esperava {n_bins} lucros na linha 4, achei {len(profits)}")
    
    # monta lista de bins: [((h, w), lucro), …]
    bins = [[[h, w], lucro] for (h, w), lucro in zip(pares_bins, profits)]
    
    # Linhas 5 a 5+n_items-1: cada uma com um par h, w da peça
    pecas = []
    for idx in range(5, 5 + n_items):
        if idx >= len(lines):
            raise ValueError(f"Arquivo terminou antes de ler todas as {n_items} peças")
        nums = re.findall(r'\d+', lines[idx])
        if len(nums) < 2:
            raise ValueError(f"Esperava H e W na linha {idx}, achei: {lines[idx]!r}")
        h, w = map(int, nums[:2])
        coords = [(0,0), (w,0), (w,h), (0,h)]
        pecas.append(coords)
    
    return bins, pecas

    
class VSBPP_2D():
    def __init__(self, ins, dict_best=None):
        self.dict_best = dict_best
        self.ins = ins
        self.instance_name = ins
        bins,pieces = ler_ins(ins)
        self.__NUM_PIECES = len(pieces)
        self.__NUM_BINS = len(bins)
        # print("Número de peças: ", self.__NUM_PIECES)
        # print("Número de bins: ", self.__NUM_BINS)
        self.__pieces = pieces
        self.__bins = bins
        bin_size = bins[0]   
        bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False, plot=False, pre_processar=True, margem=0)

        self.nfps = bin.tabela_nfps

        # print("Peças: ", self.__pieces)
        # print("Bins: ", self.__bins)
        self.tam_solution = 2*self.__NUM_PIECES
        self.greedy = False 
 


    def greedy_solution(self, type=0):
        
        if type == 0:
            pieces = copy.deepcopy(self.__pieces)
            bins_type = []
            pieces.sort(key=lambda x: Polygon(x).area, reverse=True)
            
            bins = []
            total_cost = 0  
            for peca in pieces:
                
                bins_possiveis = []
                
                for bin in bins:
                    for grau in [0,1]:
                        peca_idx = bin.lista.index(peca) 
                        nfp = bin.nfp(peca_idx, grau)
                    
                        if len(nfp) > 0:  
                            bins_possiveis.append([bin,grau])
                    
                if len(bins_possiveis) > 0:  
                    melhor_ratio = 0
                    melhor_bin = None
                    for bin in bins_possiveis:  
                        ratio = bin[0].area_usada() + (Polygon(peca).area/bin[0].area)
                        if ratio > melhor_ratio:
                            peca_idx = bin[0].lista.index(peca)
                            melhor_ratio = ratio
                            melhor_bin = bin  
                                
                    index = bins.index(melhor_bin[0])
                    bins[index].posicionar(bins[index].BLF(peca_idx, melhor_bin[1]))
                else:
                    idx,grau,key = self.best_bin( peca)
                    bins_type.append(key)
                    bin_size = self.__bins[idx]
                    
                    bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False, plot=False, tabela=self.nfps, margem=0)
                    peca_idx = bin.lista.index(peca)
                    # nfp = bin.nfp(peca_idx, 0)
                    # print(len(nfp))
                    pos = bin.BLF(peca_idx, grau)
                    # print("Pos: ", pos)
                    bin.posicionar(pos)
                    # bin.click()
                    bins.append(bin) 

                    total_cost += bin_size[1]
                    
            keys = self.encoder(pieces, bins_type)
            print([bin.area_usada() for bin in bins], total_cost)
            return keys
        elif type ==1:
            pieces = copy.deepcopy(self.__pieces)
            pieces.sort(key=lambda x: Polygon(x).area, reverse=True)
            
            bins = []
            total_cost = 0  
            for peca in pieces:
                
                bins_possiveis = []
                
                for bin in bins:
                    for grau in [0,1]:
                        peca_idx = bin.lista.index(peca) 
                        nfp = bin.nfp(peca_idx, grau)
                    
                        if len(nfp) > 0:  
                            bins_possiveis.append([bin,grau])
                    
                if len(bins_possiveis) > 0:  
                    melhor_ratio = 0
                    melhor_bin = None
                    for bin in bins_possiveis:  
                        ratio = bin[0].area_usada() + (Polygon(peca).area/bin[0].area)
                        if ratio > melhor_ratio:
                            peca_idx = bin[0].lista.index(peca)
                            melhor_ratio = ratio
                            melhor_bin = bin  
                                
                    index = bins.index(melhor_bin[0])
                    bins[index].posicionar(bins[index].BLF(peca_idx, melhor_bin[1]))
                else:
                    idx,grau = self.best_bin_2( peca)
                    bins_type.append((idx,grau))
                    bin_size = self.__bins[idx]
                    
                    bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False, plot=False, tabela=self.nfps, margem=0)
                    peca_idx = bin.lista.index(peca)
                    # nfp = bin.nfp(peca_idx, 0)
                    # print(len(nfp))
                    pos = bin.BLF(peca_idx, grau)
                    # print("Pos: ", pos)
                    bin.posicionar(pos)
                    # bin.click()
                    bins.append(bin) 

                    total_cost += bin_size[1]
                    
            print([bin.area_usada() for bin in bins], total_cost)

    def encoder(self, pieces, bins):
        keys = []
        for piece in pieces:
            key = self.__pieces.index(piece)/self.__NUM_PIECES
            keys.append(key)
        
        keys = keys + bins
        for i in range(self.tam_solution - len(keys)):
            keys.append(np.random.rand())
        return keys
    def decoder(self, keys):   
        piece_keys = keys[:self.__NUM_PIECES]  
        bin_keys = keys[self.__NUM_PIECES:]  
        
        sequence_pieces = np.argsort(piece_keys).tolist()    
        type_bins = [key for key in bin_keys]
        
        solution = sequence_pieces + type_bins
        # print("Solução: ", solution)
        return solution
    
    def cost(self, solution: list[int], final = False):
        total_cost = 0       
        bins = []
        
        for idx in range(self.__NUM_PIECES):
            # print(solution)
            # print("idx: ", idx)
            # print(solution[idx])
            peca = self.__pieces[solution[idx]]
           
            idx_bin_atual = idx + self.__NUM_PIECES 
            bins_possiveis = []
                
            for bin in bins:
                for grau in [0,1]:
                    peca_idx = bin.lista.index(peca) 
                    nfp = bin.nfp(peca_idx, grau)
                    # print(len(nfp))
                    if len(nfp) > 0:  
                        bins_possiveis.append([bin,grau])
                    
            if len(bins_possiveis) > 0:  
                melhor_ratio = 0
                melhor_bin = None
                for bin in bins_possiveis:  
                    ratio = bin[0].area_usada()
                    if ratio > melhor_ratio:
                        peca_idx = bin[0].lista.index(peca)
                        melhor_ratio = ratio
                        melhor_bin = bin  
                              
                index = bins.index(melhor_bin[0])
                bins[index].posicionar(bins[index].BLF(peca_idx, melhor_bin[1]))
            else:
                idx,grau = self.key_to_bin(solution[idx_bin_atual], peca)
                bin_size = self.__bins[idx]
                
                bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False, plot=False, tabela=self.nfps, margem=0)
                peca_idx = bin.lista.index(peca)
                # nfp = bin.nfp(peca_idx, 0)
                # print(len(nfp))
                pos = bin.BLF(peca_idx, grau)
                # print("Pos: ", pos)
                bin.posicionar(pos)
                # bin.click()
                bins.append(bin) 

                total_cost += bin_size[1]
            
        
     

           
        if final:    

            print([bin.area_usada() for bin in bins], total_cost)   
            self.bins_usados = bins
        # print(len(bins), total_cost)
        i = 0
        # for bin in bins:
        #     i += 1
        #     # print(bin.area_usada())
        #     draw_cutting_area(bin.pecas_posicionadas, bin.base, bin.altura, filename=self.ins + f"_{i}.png")
        return total_cost
    
    def _compute_lower_bounds(self):
        pieces = self.__pieces               # lista de peças: cada peça é [(w,h), ...]?
        bins    = self.__bins                 # lista de bins: cada bin é ((W,H), cost)

        # 1) L_a: bound de área
        total_area = sum(max(x for x,y in p) * max(y for x,y in p) for p in pieces)
        max_bin_area = max(W*H for (W,H),c in bins)
        L_a = math.ceil(total_area / max_bin_area)

        # 2) L_2w: item mais caro
        # para cada peça, encontre o bin mínimo que caiba e pegue o custo
        item_costs = []
        for p in pieces:
            w_i, h_i = max(x for x,y in p), max(y for x,y in p)
            feasible = [c for (W,H),c in bins if W>=w_i and H>=h_i]
            if not feasible:
                raise ValueError("Peça não cabe em nenhum bin!")
            item_costs.append(min(feasible))
        L_2w = math.ceil(max(item_costs))

        # 3) L'_2c: contínuo custo/área
        # calcule c_k/(W_k*H_k) para cada bin e escolha o melhor para cada peça
        cost_per_area = [c/(W*H) for (W,H),c in bins]
        L_2c_frac = 0
        for p in pieces:
            w_i, h_i = max(x for x,y in p), max(y for x,y in p)
            # escolha bin com menor c/(W*H) dentre os que cabem
            best = min((c_pa, (W,H), c) 
                       for (W,H),c, c_pa in zip([b[0] for b in bins],
                                               [b[1] for b in bins],
                                               cost_per_area)
                       if W>=w_i and H>=h_i)
            c_pa, (Wb,Hb), cb = best
            L_2c_frac += (w_i*h_i)/(Wb*Hb)*cb
        L_2c = L_2c_frac  # não arredonda, pois é bound contínuo

        # 4) Bound combinado
        return  [L_a, L_2w, L_2c, max(L_a, L_2w, L_2c)]
    def tipo_bin(self, key):
        ratio = 1/self.__NUM_BINS
        bin = 0
        for i in range(self.__NUM_BINS):
            if key < (i+1)*ratio:             
                bin = i
                break    
        return bin
    
    def best_bin(self, peca):
        area_peca = max([x for x,y in peca]) * max([y for x,y in peca])
        bins_possiveis = []
        for bin_size in self.__bins:
            for grau in [0,1]:
        
                bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False,plot=False, tabela=self.nfps, margem=0)

                peca_idx = bin.lista.index(peca) 
                nfp = bin.nfp(peca_idx,grau)
            # print(len(nfp))
                if len(nfp) > 0: 
                    bins_possiveis.append([bin_size,grau,bin_size[1]])
                    
            
                
            
     

        
        idx = bins_possiveis.index(min(bins_possiveis, key=lambda x: x[2]))
        return self.__bins.index(bins_possiveis[idx][0]), bins_possiveis[idx][1], idx/len(bins_possiveis)
    
    def best_bin_2(self, peca):
        area_peca = max([x for x,y in peca]) * max([y for x,y in peca])
        bins_possiveis = []
        for bin_size in self.__bins:
            for grau in [0,1]:
        
                bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False,plot=False, tabela=self.nfps, margem=0)

                peca_idx = bin.lista.index(peca) 
                nfp = bin.nfp(peca_idx,grau)
            # print(len(nfp))
                if len(nfp) > 0: 
                    bins_possiveis.append([bin_size,grau,bin_size[0][0]*bin_size[0][1]])
        idx = bins_possiveis.index(max(bins_possiveis, key=lambda x: x[2]))
        return self.__bins.index(bins_possiveis[idx][0]), bins_possiveis[idx][1]
    def key_to_bin(self, key, peca):
        area_peca = max([x for x,y in peca]) * max([y for x,y in peca])
        bins_possiveis = []
        for bin_size in self.__bins:
            for grau in [0,1]:
        
                bin = CSP(self.ins, bin_size[0][0], bin_size[0][1], Escala=1, render=False,plot=False, tabela=self.nfps, margem=0)

                peca_idx = bin.lista.index(peca) 
                nfp = bin.nfp(peca_idx,grau)
            # print(len(nfp))
                if len(nfp) > 0: 
                    bins_possiveis.append([bin_size,grau])
                
            
     
        bins = len(bins_possiveis)
        ratio = 1/bins
        
        idx = int(key/ratio)
        return self.__bins.index(bins_possiveis[idx][0]), bins_possiveis[idx][1]
import time   
if __name__ == "__main__":
    # ins = ler_ins(arquivos_bpp[0])
    # print(ins[0][0][0][0], ins[0][0][0][1])
    # env = CSP(arquivos_bpp[0], ins[0][-1][0][0], ins[0][-1][0][1], Escala=50, render=True, pre_processar=True, margem=0)
    # env.click()
    # for i in range(len(arquivos_bpp)):
    #     env = VSBPP_2D(arquivos_bpp[i])
    #     keys = env.greedy_solution(0)
    #     # print("Chave: ", keys)
    #     # env.gre(1)
    #     env.cost(env.decoder(keys), True)
    # k = 0
    # start_time = time.time()
    # while time.time() - start_time < 600:
    #     keys = np.random.rand(env.tam_solution)  # Chave aleatória para teste
    #     sol = env.decoder(keys)
    #     env.cost(sol,   True)
    #     k+=1
    #     print(k, time.time() - start_time)
    
    # print(k)


    brkga = 0
    sa = 0
    ms = 0
    vns = 0
    ils = 0
    for i in range(6):
        tipo = int(input(f"Selecione o tipo de algoritmo {i+1} (0: BRKGA, 1: SA, 2: MS, 3: VNS, 4: ILS): "))
        if tipo == 0:
            brkga += 1
        elif tipo == 1:
            sa += 1
        elif tipo == 2:
            ms += 1
        elif tipo == 3:
            vns += 1
        elif tipo == 4:
            ils += 1
        else:
            print("Tipo inválido. Usando BRKGA como padrão.")
            brkga += 1
    for ins in arquivos_bpp:

        print("Ins: ", ins)
        # ins = "Dataset_2D\\2005PisingerSigurd1.bpp"
        # ins = "Dataset_2D\\2005PisingerSigurd2.bpp"
        # ins = "Dataset_2D\\2005PisingerSigurd3.bpp"
        # ins = "Dataset_2D\\2005PisingerSigurd4.bpp"
        # ins = "Dataset_2D\\2005PisingerSigurd5.bpp"
        env = VSBPP_2D(ins)
        LB = env._compute_lower_bounds()[-1]
        # keys = np.random.rand(env2D.tam_solution)  # Chave aleatória para teste
        # sol = env2D.decoder(keys)
        # env2D.cost(sol)
        solver = RKO(env)
        out = solver.solve(
        pop_size=int(30),
        elite_pop=0.05 ,
        chance_elite=0.7,
        limit_time=600,       
        n_workers=6,
        brkga=brkga,
        ms=ms,
        sa=sa,
        vns=vns,
        ils=ils)

        sol = out[1]
        gap = ((sol - LB)/LB ) * 100

        with open("resultados.csv", "a") as f:
            f.write(f"{ins},{out[1]},{LB},{gap}\n")