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
    def __init__(self, instance_name):
        
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
        
        self.tam_solution = 2 * self.__NUM_PIECES 
        
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
    
    def cost(self, solution: list[int], final = False):
        total_cost = 0       
        bins = []

  
        
        idx_bin_atual = self.__NUM_PIECES
        capacidade_bin = self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[0]])][CAPACITY]
        capacidade_atual = 0

        bins.append([capacidade_atual, capacidade_bin]) # Adiciona o primeiro bin aberto na lista de bins usados
        
        total_cost += self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[0]])][COST]   # Primeiro bin sempre começa aberto
        idx = 0
        while idx < self.__NUM_PIECES: # percorre todas as peças
            # print(bins)
            bins_possiveis = [] # lista de bins possiveis para a peça atual
            
            for bin in bins: # percorre todos os bins abertos
                if bin[0] + self.__pieces[solution[idx]] <=  bin[1]: #Se a peça cabe no bin atual, adiciona ela ao bin atual
                    # print(1)
                    bins_possiveis.append(bin) # adiciona o bin atual a lista de bins possiveis
                    
            if len(bins_possiveis) > 0:  # Se cabe, adiciona a peça ao bin atual
                melhor_ratio = 0
                melhor_bin = None

                for bin in bins_possiveis:  # percorre todos os bins abertos
                    ratio = bin[0] / bin[1]  # calcula a razão entre o peso atual e a capacidade do bin
                    if ratio >= melhor_ratio:
                        melhor_ratio = ratio
                        melhor_bin = copy.deepcopy(bin)  # pega o bin com a melhor razão

                # Atualiza o bin com a nova capacidade
                index = bins.index(melhor_bin)
                bins[index] = (bins[index][0] + self.__pieces[solution[idx]], bins[index][1])  # Atualiza o peso atual no bin
                idx += 1  # avança para a próxima peça

      
            
            else: # Se não cabe, abre um novo bin

          
                idx_bin_atual += 1
   
                capacidade_bin = self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[idx]])][CAPACITY] # pega a capacidade do novo bin atual # pega a capacidade do novo bin atual
                
                capacidade_atual = 0 # zera a capacidade atual, para o proximo bin
                bins.append([capacidade_atual, capacidade_bin]) # Adiciona o novo bin aberto na lista de bins usados
                total_cost += self.__bins[self.key_to_bin(solution[idx_bin_atual],self.__pieces[solution[idx]])][COST]    #Adiciona o custo do novo bin aberto 


           
        if final:    
            print(bins)
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
    
    def key_to_bin(self, key, size_piece):
        bins_possiveis = []
        for bin in self.__bins:
            if bin[CAPACITY] >= size_piece:
                bins_possiveis.append(bin)

        ratio = 1/len(bins_possiveis)
        bin = int(key/ratio) # pega o bin correspondente a chave
        return self.__bins.index(bins_possiveis[bin]) # retorna o índice do bin correspondente a chave
   
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