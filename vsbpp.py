import os

CAPACITY = 0
COST = 1

hs_instances = ['H&Sconc100-1-1.txt', 'H&Sconc100-1-10.txt', 'H&Sconc100-1-2.txt', 'H&Sconc100-1-3.txt', 'H&Sconc100-1-4.txt', 'H&Sconc100-1-5.txt', 'H&Sconc100-1-6.txt', 'H&Sconc100-1-7.txt', 'H&Sconc100-1-8.txt', 'H&Sconc100-1-9.txt', 'H&Sconc100-2-1.txt', 'H&Sconc100-2-10.txt', 'H&Sconc100-2-2.txt', 'H&Sconc100-2-3.txt', 'H&Sconc100-2-4.txt', 'H&Sconc100-2-5.txt', 'H&Sconc100-2-6.txt', 'H&Sconc100-2-7.txt', 'H&Sconc100-2-8.txt', 'H&Sconc100-2-9.txt', 'H&Sconc100-3-1.txt', 'H&Sconc100-3-10.txt', 'H&Sconc100-3-2.txt', 'H&Sconc100-3-3.txt', 'H&Sconc100-3-4.txt', 'H&Sconc100-3-5.txt', 'H&Sconc100-3-6.txt', 'H&Sconc100-3-7.txt', 'H&Sconc100-3-8.txt', 'H&Sconc100-3-9.txt', 'H&Sconc1000-1-1.txt', 'H&Sconc1000-1-10.txt', 'H&Sconc1000-1-2.txt', 'H&Sconc1000-1-3.txt', 'H&Sconc1000-1-4.txt', 'H&Sconc1000-1-5.txt', 'H&Sconc1000-1-6.txt', 'H&Sconc1000-1-7.txt', 'H&Sconc1000-1-8.txt', 'H&Sconc1000-1-9.txt', 'H&Sconc1000-2-1.txt', 'H&Sconc1000-2-10.txt', 'H&Sconc1000-2-2.txt', 'H&Sconc1000-2-3.txt', 'H&Sconc1000-2-4.txt', 'H&Sconc1000-2-5.txt', 'H&Sconc1000-2-6.txt', 'H&Sconc1000-2-7.txt', 'H&Sconc1000-2-8.txt', 'H&Sconc1000-2-9.txt', 'H&Sconc1000-3-1.txt', 'H&Sconc1000-3-10.txt', 'H&Sconc1000-3-2.txt', 'H&Sconc1000-3-3.txt', 'H&Sconc1000-3-4.txt', 'H&Sconc1000-3-5.txt', 'H&Sconc1000-3-6.txt', 'H&Sconc1000-3-7.txt', 'H&Sconc1000-3-8.txt', 'H&Sconc1000-3-9.txt', 'H&Sconc200-1-1.txt', 'H&Sconc200-1-10.txt', 'H&Sconc200-1-2.txt', 'H&Sconc200-1-3.txt', 'H&Sconc200-1-4.txt', 'H&Sconc200-1-5.txt', 'H&Sconc200-1-6.txt', 'H&Sconc200-1-7.txt', 'H&Sconc200-1-8.txt', 'H&Sconc200-1-9.txt', 'H&Sconc200-2-1.txt', 'H&Sconc200-2-10.txt', 'H&Sconc200-2-2.txt', 'H&Sconc200-2-3.txt', 'H&Sconc200-2-4.txt', 'H&Sconc200-2-5.txt', 'H&Sconc200-2-6.txt', 'H&Sconc200-2-7.txt', 'H&Sconc200-2-8.txt', 'H&Sconc200-2-9.txt', 'H&Sconc200-3-1.txt', 'H&Sconc200-3-10.txt', 'H&Sconc200-3-2.txt', 'H&Sconc200-3-3.txt', 'H&Sconc200-3-4.txt', 'H&Sconc200-3-5.txt', 'H&Sconc200-3-6.txt', 'H&Sconc200-3-7.txt', 'H&Sconc200-3-8.txt', 'H&Sconc200-3-9.txt', 'H&Sconc2000-1-1.txt', 'H&Sconc2000-1-10.txt', 'H&Sconc2000-1-2.txt', 'H&Sconc2000-1-3.txt', 'H&Sconc2000-1-4.txt', 'H&Sconc2000-1-5.txt', 'H&Sconc2000-1-6.txt', 'H&Sconc2000-1-7.txt', 'H&Sconc2000-1-8.txt', 'H&Sconc2000-1-9.txt', 'H&Sconc2000-2-1.txt', 'H&Sconc2000-2-10.txt', 'H&Sconc2000-2-2.txt', 'H&Sconc2000-2-3.txt', 'H&Sconc2000-2-4.txt', 'H&Sconc2000-2-5.txt', 'H&Sconc2000-2-6.txt', 'H&Sconc2000-2-7.txt', 'H&Sconc2000-2-8.txt', 'H&Sconc2000-2-9.txt', 'H&Sconc2000-3-1.txt', 'H&Sconc2000-3-10.txt', 'H&Sconc2000-3-2.txt', 'H&Sconc2000-3-3.txt', 'H&Sconc2000-3-4.txt', 'H&Sconc2000-3-5.txt', 'H&Sconc2000-3-6.txt', 'H&Sconc2000-3-7.txt', 'H&Sconc2000-3-8.txt', 'H&Sconc2000-3-9.txt', 'H&Sconc500-1-1.txt', 'H&Sconc500-1-10.txt', 'H&Sconc500-1-2.txt', 'H&Sconc500-1-3.txt', 'H&Sconc500-1-4.txt', 'H&Sconc500-1-5.txt', 'H&Sconc500-1-6.txt', 'H&Sconc500-1-7.txt', 'H&Sconc500-1-8.txt', 'H&Sconc500-1-9.txt', 'H&Sconc500-2-1.txt', 'H&Sconc500-2-10.txt', 'H&Sconc500-2-2.txt', 'H&Sconc500-2-3.txt', 'H&Sconc500-2-4.txt', 'H&Sconc500-2-5.txt', 'H&Sconc500-2-6.txt', 'H&Sconc500-2-7.txt', 'H&Sconc500-2-8.txt', 'H&Sconc500-2-9.txt', 'H&Sconc500-3-1.txt', 'H&Sconc500-3-10.txt', 'H&Sconc500-3-2.txt', 'H&Sconc500-3-3.txt', 'H&Sconc500-3-4.txt', 'H&Sconc500-3-5.txt', 'H&Sconc500-3-6.txt', 'H&Sconc500-3-7.txt', 'H&Sconc500-3-8.txt', 'H&Sconc500-3-9.txt', 'H&Sconv100-1-1.txt', 'H&Sconv100-1-10.txt', 'H&Sconv100-1-2.txt', 'H&Sconv100-1-3.txt', 'H&Sconv100-1-4.txt', 'H&Sconv100-1-5.txt', 'H&Sconv100-1-6.txt', 'H&Sconv100-1-7.txt', 'H&Sconv100-1-8.txt', 'H&Sconv100-1-9.txt', 'H&Sconv100-2-1.txt', 'H&Sconv100-2-10.txt', 'H&Sconv100-2-2.txt', 'H&Sconv100-2-3.txt', 'H&Sconv100-2-4.txt', 'H&Sconv100-2-5.txt', 'H&Sconv100-2-6.txt', 'H&Sconv100-2-7.txt', 'H&Sconv100-2-8.txt', 'H&Sconv100-2-9.txt', 'H&Sconv100-3-1.txt', 'H&Sconv100-3-10.txt', 'H&Sconv100-3-2.txt', 'H&Sconv100-3-3.txt', 'H&Sconv100-3-4.txt', 'H&Sconv100-3-5.txt', 'H&Sconv100-3-6.txt', 'H&Sconv100-3-7.txt', 'H&Sconv100-3-8.txt', 'H&Sconv100-3-9.txt', 'H&Sconv1000-1-1.txt', 'H&Sconv1000-1-10.txt', 'H&Sconv1000-1-2.txt', 'H&Sconv1000-1-3.txt', 'H&Sconv1000-1-4.txt', 'H&Sconv1000-1-5.txt', 'H&Sconv1000-1-6.txt', 'H&Sconv1000-1-7.txt', 'H&Sconv1000-1-8.txt', 'H&Sconv1000-1-9.txt', 'H&Sconv1000-2-1.txt', 'H&Sconv1000-2-10.txt', 'H&Sconv1000-2-2.txt', 'H&Sconv1000-2-3.txt', 'H&Sconv1000-2-4.txt', 'H&Sconv1000-2-5.txt', 'H&Sconv1000-2-6.txt', 'H&Sconv1000-2-7.txt', 'H&Sconv1000-2-8.txt', 'H&Sconv1000-2-9.txt', 'H&Sconv1000-3-1.txt', 'H&Sconv1000-3-10.txt', 'H&Sconv1000-3-2.txt', 'H&Sconv1000-3-3.txt', 'H&Sconv1000-3-4.txt', 'H&Sconv1000-3-5.txt', 'H&Sconv1000-3-6.txt', 'H&Sconv1000-3-7.txt', 'H&Sconv1000-3-8.txt', 'H&Sconv1000-3-9.txt', 'H&Sconv200-1-1.txt', 'H&Sconv200-1-10.txt', 'H&Sconv200-1-2.txt', 'H&Sconv200-1-3.txt', 'H&Sconv200-1-4.txt', 'H&Sconv200-1-5.txt', 'H&Sconv200-1-6.txt', 'H&Sconv200-1-7.txt', 'H&Sconv200-1-8.txt', 'H&Sconv200-1-9.txt', 'H&Sconv200-2-1.txt', 'H&Sconv200-2-10.txt', 'H&Sconv200-2-2.txt', 'H&Sconv200-2-3.txt', 'H&Sconv200-2-4.txt', 'H&Sconv200-2-5.txt', 'H&Sconv200-2-6.txt', 'H&Sconv200-2-7.txt', 'H&Sconv200-2-8.txt', 'H&Sconv200-2-9.txt', 'H&Sconv200-3-1.txt', 'H&Sconv200-3-10.txt', 'H&Sconv200-3-2.txt', 'H&Sconv200-3-3.txt', 'H&Sconv200-3-4.txt', 'H&Sconv200-3-5.txt', 'H&Sconv200-3-6.txt', 'H&Sconv200-3-7.txt', 'H&Sconv200-3-8.txt', 'H&Sconv200-3-9.txt', 'H&Sconv2000-1-1.txt', 'H&Sconv2000-1-10.txt', 'H&Sconv2000-1-2.txt', 'H&Sconv2000-1-3.txt', 'H&Sconv2000-1-4.txt', 'H&Sconv2000-1-5.txt', 'H&Sconv2000-1-6.txt', 'H&Sconv2000-1-7.txt', 'H&Sconv2000-1-8.txt', 'H&Sconv2000-1-9.txt', 'H&Sconv2000-2-1.txt', 'H&Sconv2000-2-10.txt', 'H&Sconv2000-2-2.txt', 'H&Sconv2000-2-3.txt', 'H&Sconv2000-2-4.txt', 'H&Sconv2000-2-5.txt', 'H&Sconv2000-2-6.txt', 'H&Sconv2000-2-7.txt', 'H&Sconv2000-2-8.txt', 'H&Sconv2000-2-9.txt', 'H&Sconv2000-3-1.txt', 'H&Sconv2000-3-10.txt', 'H&Sconv2000-3-2.txt', 'H&Sconv2000-3-3.txt', 'H&Sconv2000-3-4.txt', 'H&Sconv2000-3-5.txt', 'H&Sconv2000-3-6.txt', 'H&Sconv2000-3-7.txt', 'H&Sconv2000-3-8.txt', 'H&Sconv2000-3-9.txt', 'H&Sconv500-1-1.txt', 'H&Sconv500-1-10.txt', 'H&Sconv500-1-2.txt', 'H&Sconv500-1-3.txt', 'H&Sconv500-1-4.txt', 'H&Sconv500-1-5.txt', 'H&Sconv500-1-6.txt', 'H&Sconv500-1-7.txt', 'H&Sconv500-1-8.txt', 'H&Sconv500-1-9.txt', 'H&Sconv500-2-1.txt', 'H&Sconv500-2-10.txt', 'H&Sconv500-2-2.txt', 'H&Sconv500-2-3.txt', 'H&Sconv500-2-4.txt', 'H&Sconv500-2-5.txt', 'H&Sconv500-2-6.txt', 'H&Sconv500-2-7.txt', 'H&Sconv500-2-8.txt', 'H&Sconv500-2-9.txt', 'H&Sconv500-3-1.txt', 'H&Sconv500-3-10.txt', 'H&Sconv500-3-2.txt', 'H&Sconv500-3-3.txt', 'H&Sconv500-3-4.txt', 'H&Sconv500-3-5.txt', 'H&Sconv500-3-6.txt', 'H&Sconv500-3-7.txt', 'H&Sconv500-3-8.txt', 'H&Sconv500-3-9.txt', 'H&Slin100-1-1.txt', 'H&Slin100-1-10.txt', 'H&Slin100-1-2.txt', 'H&Slin100-1-3.txt', 'H&Slin100-1-4.txt', 'H&Slin100-1-5.txt', 'H&Slin100-1-6.txt', 'H&Slin100-1-7.txt', 'H&Slin100-1-8.txt', 'H&Slin100-1-9.txt', 'H&Slin100-2-1.txt', 'H&Slin100-2-10.txt', 'H&Slin100-2-2.txt', 'H&Slin100-2-3.txt', 'H&Slin100-2-4.txt', 'H&Slin100-2-5.txt', 'H&Slin100-2-6.txt', 'H&Slin100-2-7.txt', 'H&Slin100-2-8.txt', 'H&Slin100-2-9.txt', 'H&Slin100-3-1.txt', 'H&Slin100-3-10.txt', 'H&Slin100-3-2.txt', 'H&Slin100-3-3.txt', 'H&Slin100-3-4.txt', 'H&Slin100-3-5.txt', 'H&Slin100-3-6.txt', 'H&Slin100-3-7.txt', 'H&Slin100-3-8.txt', 'H&Slin100-3-9.txt', 'H&Slin1000-1-1.txt', 'H&Slin1000-1-10.txt', 'H&Slin1000-1-2.txt', 'H&Slin1000-1-3.txt', 'H&Slin1000-1-4.txt', 'H&Slin1000-1-5.txt', 'H&Slin1000-1-6.txt', 'H&Slin1000-1-7.txt', 'H&Slin1000-1-8.txt', 'H&Slin1000-1-9.txt', 'H&Slin1000-2-1.txt', 'H&Slin1000-2-10.txt', 'H&Slin1000-2-2.txt', 'H&Slin1000-2-3.txt', 'H&Slin1000-2-4.txt', 'H&Slin1000-2-5.txt', 'H&Slin1000-2-6.txt', 'H&Slin1000-2-7.txt', 'H&Slin1000-2-8.txt', 'H&Slin1000-2-9.txt', 'H&Slin1000-3-1.txt', 'H&Slin1000-3-10.txt', 'H&Slin1000-3-2.txt', 'H&Slin1000-3-3.txt', 'H&Slin1000-3-4.txt', 'H&Slin1000-3-5.txt', 'H&Slin1000-3-6.txt', 'H&Slin1000-3-7.txt', 'H&Slin1000-3-8.txt', 'H&Slin1000-3-9.txt', 'H&Slin200-1-1.txt', 'H&Slin200-1-10.txt', 'H&Slin200-1-2.txt', 'H&Slin200-1-3.txt', 'H&Slin200-1-4.txt', 'H&Slin200-1-5.txt', 'H&Slin200-1-6.txt', 'H&Slin200-1-7.txt', 'H&Slin200-1-8.txt', 'H&Slin200-1-9.txt', 'H&Slin200-2-1.txt', 'H&Slin200-2-10.txt', 'H&Slin200-2-2.txt', 'H&Slin200-2-3.txt', 'H&Slin200-2-4.txt', 'H&Slin200-2-5.txt', 'H&Slin200-2-6.txt', 'H&Slin200-2-7.txt', 'H&Slin200-2-8.txt', 'H&Slin200-2-9.txt', 'H&Slin200-3-1.txt', 'H&Slin200-3-10.txt', 'H&Slin200-3-2.txt', 'H&Slin200-3-3.txt', 'H&Slin200-3-4.txt', 'H&Slin200-3-5.txt', 'H&Slin200-3-6.txt', 'H&Slin200-3-7.txt', 'H&Slin200-3-8.txt', 'H&Slin200-3-9.txt', 'H&Slin2000-1-1.txt', 'H&Slin2000-1-10.txt', 'H&Slin2000-1-2.txt', 'H&Slin2000-1-3.txt', 'H&Slin2000-1-4.txt', 'H&Slin2000-1-5.txt', 'H&Slin2000-1-6.txt', 'H&Slin2000-1-7.txt', 'H&Slin2000-1-8.txt', 'H&Slin2000-1-9.txt', 'H&Slin2000-2-1.txt', 'H&Slin2000-2-10.txt', 'H&Slin2000-2-2.txt', 'H&Slin2000-2-3.txt', 'H&Slin2000-2-4.txt', 'H&Slin2000-2-5.txt', 'H&Slin2000-2-6.txt', 'H&Slin2000-2-7.txt', 'H&Slin2000-2-8.txt', 'H&Slin2000-2-9.txt', 'H&Slin2000-3-1.txt', 'H&Slin2000-3-10.txt', 'H&Slin2000-3-2.txt', 'H&Slin2000-3-3.txt', 'H&Slin2000-3-4.txt', 'H&Slin2000-3-5.txt', 'H&Slin2000-3-6.txt', 'H&Slin2000-3-7.txt', 'H&Slin2000-3-8.txt', 'H&Slin2000-3-9.txt', 'H&Slin500-1-1.txt', 'H&Slin500-1-10.txt', 'H&Slin500-1-2.txt', 'H&Slin500-1-3.txt', 'H&Slin500-1-4.txt', 'H&Slin500-1-5.txt', 'H&Slin500-1-6.txt', 'H&Slin500-1-7.txt', 'H&Slin500-1-8.txt', 'H&Slin500-1-9.txt', 'H&Slin500-2-1.txt', 'H&Slin500-2-10.txt', 'H&Slin500-2-2.txt', 'H&Slin500-2-3.txt', 'H&Slin500-2-4.txt', 'H&Slin500-2-5.txt', 'H&Slin500-2-6.txt', 'H&Slin500-2-7.txt', 'H&Slin500-2-8.txt', 'H&Slin500-2-9.txt', 'H&Slin500-3-1.txt', 'H&Slin500-3-10.txt', 'H&Slin500-3-2.txt', 'H&Slin500-3-3.txt', 'H&Slin500-3-4.txt', 'H&Slin500-3-5.txt', 'H&Slin500-3-6.txt', 'H&Slin500-3-7.txt', 'H&Slin500-3-8.txt', 'H&Slin500-3-9.txt']
monacci_instances = ['prob_100_1.txt', 'prob_100_10.txt', 'prob_100_2.txt', 'prob_100_3.txt', 'prob_100_4.txt', 'prob_100_5.txt', 'prob_100_6.txt', 'prob_100_7.txt', 'prob_100_8.txt', 'prob_100_9.txt', 'prob_200_1.txt', 'prob_200_10.txt', 'prob_200_2.txt', 'prob_200_3.txt', 'prob_200_4.txt', 'prob_200_5.txt', 'prob_200_6.txt', 'prob_200_7.txt', 'prob_200_8.txt', 'prob_200_9.txt', 'prob_25_1.txt', 'prob_25_10.txt', 'prob_25_2.txt', 'prob_25_3.txt', 'prob_25_4.txt', 'prob_25_5.txt', 'prob_25_6.txt', 'prob_25_7.txt', 'prob_25_8.txt', 'prob_25_9.txt', 'prob_500_1.txt', 'prob_500_10.txt', 'prob_500_2.txt', 'prob_500_3.txt', 'prob_500_4.txt', 'prob_500_5.txt', 'prob_500_6.txt', 'prob_500_7.txt', 'prob_500_8.txt', 'prob_500_9.txt', 'prob_50_1.txt', 'prob_50_10.txt', 'prob_50_2.txt', 'prob_50_3.txt', 'prob_50_4.txt', 'prob_50_5.txt', 'prob_50_6.txt', 'prob_50_7.txt', 'prob_50_8.txt', 'prob_50_9.txt'] 

def read_instance(path):
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
                    bins.append((int(linha[2*i]), int(linha[2*i + 1]))) # bins = [(capacidade, valor), ..]                  
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
        full_path = path + "\Datasets\\" + instance_name 
        
      

        pieces, bins = read_instance(full_path) # pieces = lista de itens, representados pelo se peso || bins = lista de bins, representados por uma lista de tuplas (valor, capacidade)
        
        # print("Pieces: ", pieces)
        # print("Bins: ", bins)
        self.__NUM_PIECES = len(pieces)
        self.__NUM_BINS = len(bins)
        self.__MAX_BINS = self.NUM_PIECES
        self.__pieces = pieces
        self.__bins = bins

for ins in hs_instances:
    env = VSBPP(ins)
    
for ins in monacci_instances:
    env = VSBPP(ins)
