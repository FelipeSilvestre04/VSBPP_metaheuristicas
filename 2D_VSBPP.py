from One_Bin import CSP
import numpy as np
import copy

CAPACITY = 0
COST = 1

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
    
class VSBPP_2D():
    def __init__(self, ins):
        self.ins = ins
        pieces,bins = ler_ins(ins)
        self.__NUM_PIECES = len(pieces)
        self.__NUM_BINS = len(bins)
        self.__pieces = pieces
        self.__bins = bins
        self.tam_solution = 2*self.__NUM_PIECES 
 





    def decoder(self, keys):   
        piece_keys = keys[:self.__NUM_PIECES]  
        bin_keys = keys[self.__NUM_PIECES:]  
        
        sequence_pieces = np.argsort(piece_keys).tolist()    
        type_bins = [key for key in bin_keys]
        
        solution = sequence_pieces + type_bins
        
        return solution
    
    def cost(self, solution: list[int], final = False):
        total_cost = 0       
        bins = []
        
        for idx in range(self.__NUM_PIECES):
            peca = self.__pieces[solution[idx]]
            peca_idx = bin.lista.index(peca)
            idx_bin_atual = idx + self.__NUM_PIECES 
            bins_possiveis = []
                
            for bin in bins: 
                nfp = bin.nfp(peca_idx, 0)
                if nfp is not None:  
                    bins_possiveis.append(bin)
                    
            if len(bins_possiveis) > 0:  
                melhor_ratio = 0
                melhor_bin = None
                for bin in bins_possiveis:  
                    ratio = bin.area_usada()
                    if ratio > melhor_ratio:
                        melhor_ratio = ratio
                        melhor_bin = copy.deepcopy(bin)  
                              
                index = bins.index(melhor_bin)
                bins[index].BLF(peca_idx, 0)
            else:
                bin_size = self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[idx]])]
                
                bin = CSP(self.ins, bin_size[0], bin_size[1])
                
                bins.append(bin) 
                total_cost += self.__bins[self.key_to_bin(solution[idx_bin_atual],idx)][COST]   
            
     

           
        if final:    
            # print(bins)
            self.bins_usados = bins
        return total_cost
    
    def tipo_bin(self, key):
        ratio = 1/self.__NUM_BINS
        bin = 0
        for i in range(self.__NUM_BINS):
            if key < (i+1)*ratio:             
                bin = i
                break    
        return bin
    
    def key_to_bin(self, key):
     
        bins = len(self.__bins)
        ratio = 1/bins
        
        idx = int(key/ratio)
        return idx