import os
import numpy as np
import random
import copy

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
    def __init__(self, instance_name, dict_best = None):
        self.dict_best = dict_best
        
        self.instance_name = instance_name
        
        self.bins_usados = []
        
        path = os.path.dirname(__file__)
        full_path = path + "\Datasets" + "\VSBPP\\" + instance_name 


        
      

        pieces, bins = read_instance(full_path) # pieces = lista de itens, representados pelo se peso || bins = lista de bins, representados por uma lista de tuplas (valor, capacidade)
        
        # print("Pieces: ", pieces)
        # print("Bins: ", bins)
        self.__NUM_PIECES = len(pieces)
        self.__NUM_BINS = len(bins)
        self.__MAX_BINS = self.__NUM_PIECES
        self.__pieces = pieces
        self.__bins = bins
        
        self.tam_solution = 2*self.__NUM_PIECES 
        
    def check_valid(self, solution: list[int]):
        # gera um dict com a capacidade atual de cada bin
        bins_capaity = { idx: self.__bins[tp][CAPACITY] for idx, tp in enumerate(solution[self.__NUM_PIECES:])}
        for i in range(self.__NUM_PIECES):
            idx_bin = solution[i]
            piece_weight = self.__pieces[i] # busca o peso da peça
            if piece_weight > bins_capaity[idx_bin]: # verifica se o peso da peça cabe no bin
                return False
            bins_capaity[idx_bin] -= piece_weight # preenche o bin com o peso da pesa
        return True
    
    def ssp3(self):
        """
        Implements SSP3 and builds Random-Key encoding for the existing decoder:
        1) Collects `sequence` of item indices in pack order
        2) Collects `type_bins` flags (best_type/num_bins for first in each bin, else 0)
        3) Calls encoder_from_solution(sequence, type_bins) to compute keys
        Returns (total_cost, keys)
        """
        N = len(self.__pieces)
        num_bins = len(self.__bins)
        # lists to record the exact placement order and bin decisions
        sequence = []    # order of item indices
        type_bins = []   # per position, bin_type/num_bins or 0

        J_bar = list(range(N))
        bins = []  # list of [load, capacity]
        total_cost = 0

        while J_bar:
            # force largest remaining item
            j0 = max(J_bar, key=lambda j: self.__pieces[j])
            w0 = self.__pieces[j0]
            # subset-sum search among feasible bin types
            best_ratio = float('inf')
            best_S = None
            best_type = None
            best_cap = None
            for t, (cap, cost) in enumerate(self.__bins):
                if cap < w0: continue
                cap_rem = cap - w0
                dp = {0: []}
                for j in J_bar:
                    if j == j0: continue
                    wj = self.__pieces[j]
                    for s, subset in list(dp.items()):
                        ns = s + wj
                        if ns <= cap_rem and ns not in dp:
                            dp[ns] = subset + [j]
                max_s = max(dp)
                subset = [j0] + dp[max_s]  # forced item first, then subset
                load = w0 + max_s
                ratio = cost / load
                if ratio < best_ratio:
                    best_ratio, best_S, best_type, best_cap = ratio,  subset, t, cap
            # pack into new bin
            bins.append([sum(self.__pieces[j] for j in best_S), best_cap])
            total_cost += self.__bins[best_type][COST]
            # record sequence and bin keys
            for idx_in_bin, j in enumerate(best_S):
                sequence.append(j)
                if idx_in_bin == 0:
                    feasible = [t for t,(cap,_) in enumerate(self.__bins) if cap >= w0]
                    pos_in_feasible = feasible.index(best_type)
                    type_bins.append(pos_in_feasible / len(feasible))
                else:
                    type_bins.append(0.00000000000000001)
                J_bar.remove(j)

      
        # now encode via helper
        keys = self.encoder_from_solution(sequence, type_bins)
        # report
        best_known = self.dict_best.get(self.instance_name)
        # if best_known is not None:
        #     gap = round((total_cost - best_known) / best_known * 100, 2)
        #     print(f"ins: {self.instance_name} - cost: {total_cost} - best: {best_known} - gap:{gap}%")
        #     # if total_cost == self.cost(self.decoder(keys)):
        #         # print("Solution is feasible")
        # else:
        #     print(f"ins: {self.instance_name} - cost: {total_cost}")
        return total_cost, keys

    def encoder_from_solution(self, sequence, type_bins):
        N = self.__NUM_PIECES
        M = len(self.__bins)
        # piece_keys[j] = posição de j em `sequence` normalizada
        piece_keys = [0]*N
        for pos, j in enumerate(sequence):
            piece_keys[j] = (pos+1)/(N+1)
        # bin_keys já estão em [0,1)
        bin_keys = type_bins
        return piece_keys + bin_keys


    def greedy_solution_cost(self, p):
        max_itens = len(self.__pieces)
        itr = 0
        bins = []           # [load, capacity]
        sequence = []       # ordem de colocação
        type_bins = []      # flags de bin
        total_cost = 0

        # ordenar índices por peso decrescente
        maiores = sorted(range(max_itens), key=lambda j: self.__pieces[j], reverse=True)

        for idx in maiores:
            itr += 1
            # print(f"\r{100*(itr/max_itens):.1f}%", end="")

            # busca bins onde cabe
            bins_possiveis = [b for b in bins if b[0] + self.__pieces[idx] <= b[1]]

            if bins_possiveis:
                # escolhe bin com maior fill ratio após inserir
                melhor_ratio = -1
                melhor_bin = None
                for b in bins_possiveis:
                    ratio = (b[0] + self.__pieces[idx]) / b[1]
                    if ratio > melhor_ratio:
                        melhor_ratio = ratio
                        melhor_bin = b
                # atualiza carga
                i = bins.index(melhor_bin)
                bins[i][0] += self.__pieces[idx]
                # registro: não é início de bin
                sequence.append(idx)
                type_bins.append(1e-17)
            else:
                # abre novo bin
                t = self.best_bin_cost(self.__pieces[idx])
                cap = self.__bins[t][CAPACITY]
                cost = self.__bins[t][COST]
                bins.append([self.__pieces[idx], cap])
                total_cost += cost
                # registro: início de bin
                # lista tipos que cabem
                feas = [i for i,(c,_) in enumerate(self.__bins) if c >= self.__pieces[idx]]
                pos = feas.index(t)
                sequence.append(idx)
                type_bins.append(pos/len(feas))

        # chama encoder
        keys = self.encoder_from_solution(sequence, type_bins)

        # relatório
        # best = self.dict_best.get(self.instance_name, None)
        # if best is not None:
        #     gap = round((total_cost - best)/best*100, 2)
        #     print(f"\nins: {self.instance_name} - cost:{total_cost} - best:{best} - gap:{gap}%")
        # else:
        #     print(f"\nins: {self.instance_name} - cost:{total_cost}")

        return total_cost, keys

    def greedy_solution_capacity(self, p):
        max_itens = len(self.__pieces)
        itr = 0
        bins = []           # [load, capacity]
        sequence = []       # ordem de colocação
        type_bins = []      # flags de bin
        total_cost = 0

        # ordenar índices por peso decrescente
        maiores = sorted(range(max_itens), key=lambda j: self.__pieces[j], reverse=True)

        for idx in maiores:
            itr += 1
            # print(f"\r{100*(itr/max_itens):.1f}%", end="")

            # busca bins onde cabe
            bins_possiveis = [b for b in bins if b[0] + self.__pieces[idx] <= b[1]]

            if bins_possiveis:
                # escolhe bin com maior fill ratio após inserir
                melhor_ratio = -1
                melhor_bin = None
                for b in bins_possiveis:
                    ratio = (b[0] + self.__pieces[idx]) / b[1]
                    if ratio > melhor_ratio:
                        melhor_ratio = ratio
                        melhor_bin = b
                # atualiza carga
                i = bins.index(melhor_bin)
                bins[i][0] += self.__pieces[idx]
                # registro: não é início de bin
                sequence.append(idx)
                type_bins.append(1e-17)
            else:
                # abre novo bin com base na capacidade
                t = self.best_bin_capacity(self.__pieces[idx])
                cap = self.__bins[t][CAPACITY]
                cost = self.__bins[t][COST]
                bins.append([self.__pieces[idx], cap])
                total_cost += cost
                # registro: início de bin
                feas = [i for i,(c,_) in enumerate(self.__bins) if c >= self.__pieces[idx]]
                pos = feas.index(t)
                sequence.append(idx)
                type_bins.append(pos/len(feas))

        # chama encoder
        keys = self.encoder_from_solution(sequence, type_bins)

        # relatório
        # best = self.dict_best.get(self.instance_name, None)
        # if best is not None:
        #     gap = round((total_cost - best)/best*100, 2)
        #     print(f"\nins: {self.instance_name} - cost:{total_cost} - best:{best} - gap:{gap}%")
        # else:
        #     print(f"\nins: {self.instance_name} - cost:{total_cost}")

        return total_cost, keys
  
            
    def best_bin_cost(self,  size_piece):
        bins_possiveis = []
        best_bin = None
        best_fit = 2000000    
        for bin in self.__bins:
            if bin[CAPACITY] >= size_piece:
                ratio = bin[COST] 
                bins_possiveis.append(bin[COST])
                if ratio < best_fit:
                    best_fit = ratio
                    best_bin = bin
        return self.__bins.index(best_bin) 
    
    def best_bin_capacity(self,  size_piece):
        bins_possiveis = []
        best_bin = None
        best_fit = 0    
        for bin in self.__bins:
            if bin[CAPACITY] >= size_piece:
                ratio = bin[CAPACITY]
                bins_possiveis.append(bin[COST])
                if ratio > best_fit:
                    best_fit = ratio
                    best_bin = bin
            
      
 
        return self.__bins.index(best_bin) 
         
    def decoder(self, keys): 
        # Divide as chaves em peças e bins
        piece_keys = keys[:self.__NUM_PIECES]  # pega os primeiros N valores, que são os itens
        bin_keys = keys[self.__NUM_PIECES:]    # pega os N seguintes, que são os bins

        # Ordena as peças com base nas chaves
        sequence_pieces = np.argsort(piece_keys).tolist()  # Converte para lista

        # Determina os tipos de bins
        type_bins = [key for key in bin_keys]

        # Junta os dois vetores para gerar a solução final
        solution = sequence_pieces + type_bins
        return solution       
    def cost(self, solution: list[int], final = False):
        total_cost = 0       
        bins = []
        
        for idx in range(self.__NUM_PIECES):
            idx_bin_atual = idx + self.__NUM_PIECES 
            bins_possiveis = []
                
            for bin in bins: 
                if bin[0] + self.__pieces[solution[idx]] <=  bin[1]: 
                    bins_possiveis.append(bin) 
                    
            if len(bins_possiveis) > 0:  
                melhor_ratio = 0
                melhor_bin = None
                for bin in bins_possiveis:  
                    ratio = (bin[0] + self.__pieces[solution[idx]]) / bin[1] 
                    if ratio > melhor_ratio:
                        melhor_ratio = ratio
                        melhor_bin = copy.deepcopy(bin)  
                

                # numero_bins = len(bins_possiveis)
                # ratio = 1/numero_bins
                # key = solution[idx_bin_atual] 
                
                # idx_bin = int(key/ratio)
                
                # bin = bins_possiveis[idx_bin] 
                # melhor_bin = copy.deepcopy(bin) 

                
                index = bins.index(melhor_bin)
                bins[index] = (bins[index][0] + self.__pieces[solution[idx]], bins[index][1])
            else:
                capacidade_bin = self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[idx]])][CAPACITY]                
                capacidade_atual = self.__pieces[solution[idx]] 
                bins.append([capacidade_atual, capacidade_bin]) 
                total_cost += self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[idx]])][COST]   
            
     

           
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
    
    def key_to_bin(self, key, piece_size):
        feasible = [i for i, (cap, _) in enumerate(self.__bins) if cap >= piece_size]
        idx = min(int(key * len(feasible)), len(feasible) - 1)
        return feasible[idx]

   


    def decoder_2(self, keys): 
        
        piece_keys = keys
       
       
        sequence_pieces = np.argsort(piece_keys).tolist()  


      
        solution = sequence_pieces 
        return solution
    
    def cost_2(self, solution: list[int], final = False):
        total_cost = 0       
        bins = []
        
        for idx in range(self.__NUM_PIECES):
            
            bins_possiveis = []
                
            for bin in bins: 
                if bin[0] + self.__pieces[solution[idx]] <=  bin[1]: 
                    bins_possiveis.append(bin) 
                    
            if len(bins_possiveis) > 0:  
                melhor_ratio = 0
                melhor_bin = None
                for bin in bins_possiveis:  
                    ratio = (bin[0] + self.__pieces[solution[idx]]) / bin[1] 
                    if ratio > melhor_ratio:
                        melhor_ratio = ratio
                        melhor_bin = copy.deepcopy(bin)  
                

                # numero_bins = len(bins_possiveis)
                # ratio = 1/numero_bins
                # key = solution[idx_bin_atual] 
                
                # idx_bin = int(key/ratio)
                
                # bin = bins_possiveis[idx_bin] 
                # melhor_bin = copy.deepcopy(bin) 

                
                index = bins.index(melhor_bin)
                bins[index] = (bins[index][0] + self.__pieces[solution[idx]], bins[index][1])
            else:
                capacidade_bin = self.__bins[self.best_bin(self.__pieces[solution[idx]])][CAPACITY]                
                capacidade_atual = self.__pieces[solution[idx]] 
                bins.append([capacidade_atual, capacidade_bin]) 
                total_cost += self.__bins[self.best_bin(self.__pieces[solution[idx]])][COST]   
            
     

           
        if final:    
            print(bins)
            self.bins_usados = bins
        return total_cost
    
    
    


    