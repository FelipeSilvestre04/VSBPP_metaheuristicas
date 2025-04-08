import os

def ler_instance(path):
    pieces = []
    bins = []
    
    
    line_count = 0
    with open(path, 'r') as file:
        for line in file:
            linha = line.strip()
            linha = linha.split()
            
            if line_count == 0:
                n_pieces = int(linha[0]) # número de peças
                n_bins = int(linha[1]) # número de bins
            elif line_count == 1:
                for i in range(n_bins):
                    bins.append((int(linha[2*i]), int(linha[2*i + 1]))) # bins = [(valor, capacidade),                    
                if len(bins) != n_bins:
                    raise ValueError("Número de bins lido não confere com o número de bins esperado.")
                
            elif line_count == 2:
                for piece in linha:
                    pieces.append(int(piece))
                    
                if len(pieces) != n_pieces:
                    raise ValueError("Número de peças lido não confere com o número de peças esperado.")
            
            
            line_count += 1
            
            
        
            
    return pieces, bins

class VSBPP:
    def __init__(self, instance_name):
        
        
        path = os.path.dirname(__file__)
        full_path = path + "\Datasets\\" + instance_name + ".txt"

        pieces, bins = ler_instance(full_path) # pieces = lista de itens, representados pelo se peso || bins = lista de bins, representados por uma lista de tuplas (valor, capacidade)
        
        print("Pieces: ", pieces)
        print("Bins: ", bins)   
env = VSBPP("prob_25_1")