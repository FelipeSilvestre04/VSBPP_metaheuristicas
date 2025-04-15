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
        
        
        path = os.path.dirname(__file__)
        full_path = path + "\Datasets\\" + instance_name 
        
      

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
    
    def cost(self, solution: list[int]):
        total_cost = 0
        
        idx_bin_atual = self.__NUM_PIECES
        capacidade_bin = self.__bins[solution[idx_bin_atual]][CAPACITY] 
        capacidade_atual = 0
        total_cost += self.__bins[solution[idx_bin_atual]][COST]    # Primeiro bin sempre começa aberto

        for idx in solution[0:self.__NUM_PIECES]: 
            
                        
            if capacidade_atual + self.__pieces[idx] <  capacidade_bin: #Se a peça cabe no bin atual, adiciona ela ao bin atual
                
                capacidade_atual += self.__pieces[idx] # soma o peso da peça atual ao bin atual 
            
            else: # Se não cabe, fecha o bin atual e abre um novo bin

                idx_bin_atual += 1
                capacidade_bin = self.__bins[solution[idx_bin_atual]][CAPACITY] # pega a capacidade do novo bin atual
                capacidade_atual = 0 # zera a capacidade atual, para o proximo bin
                capacidade_atual += self.__pieces[idx] # soma o peso da peça atual ao bin atual
                
                total_cost += self.__bins[solution[idx_bin_atual]][COST]    #Adiciona o custo do novo bin aberto 


           
            
            
        return total_cost
    
    def tipo_bin(self, key):
        ratio = 1/self.__NUM_BINS
        bin = 0
        for i in range(self.__NUM_BINS):
            if key < (i+1)*ratio:             
                bin = i
                break    
        return bin
    def decoder(self, keys): 
        # Divide as chaves em peças e bins
        piece_keys = keys[:self.__NUM_PIECES]  # pega os primeiros N valores, que são os itens
        bin_keys = keys[self.__NUM_PIECES:]    # pega os N seguintes, que são os bins

        # Ordena as peças com base nas chaves
        sequence_pieces = np.argsort(piece_keys).tolist()  # Converte para lista

        # Determina os tipos de bins
        type_bins = [self.tipo_bin(key) for key in bin_keys]

        # Junta os dois vetores para gerar a solução final
        solution = sequence_pieces + type_bins
        return solution

class Solvers():
    def __init__(self, env):
        self.env = env
        self.__MAX_KEYS = self.env.tam_solution
        
    
    def random_keys(self):
        return np.random.random(self.__MAX_KEYS)
    
    def vizinhos(self, keys): #Realiza perturbações nas chaves, gerando vizinhos, soluções proximas/parecidas, para a solução atual.
        new_keys = copy.deepcopy(keys)
        prob = random.random()
        if  prob > 0.5:     
            for i, key in enumerate(new_keys):
                if random.random() > 0.5:
                    new_keys[i] = key + random.uniform(-0.5*key, 0.5*(1-key)) # aumenta ou diminui metade das chaves, mas com valores baixos
            
        else:
            
            for i, key in enumerate(new_keys):
                if random.random() > 0.7: # gera aleatouramente novos valores para 30% das chaves
                    new_keys[i] = random.random()
                    
        return new_keys
    
    def LocSearch(self, keys, x): # Busca local, recebe uma chave/solução e busca ao redor dela outras soluções, para ver se existe algum solução melhor
        iter = 0
        best_keys = keys
        solution = self.env.decoder(keys)
        best_cost = self.env.cost(solution)
        while iter < x:
            new_keys = self.vizinhos(best_keys)
            new_solution = self.env.decoder(new_keys)           
            new_cost = self.env.cost(new_solution)
            # print(f"x {iter}, Custo: {new_cost}")
            
            if new_cost < best_cost:
                best_keys = new_keys
                best_cost = new_cost
                iter = 0
            else:
                iter += 1
        
        return best_keys
    
    def MultiStart(self,max_iter,x): # Multi Start, gera várias soluções aleatórias e aplica a busca local em cada uma delas, retornando a melhor solução encontrada
        best_keys = None
        best_cost = float('inf')
        best_ini_cost = float('inf')
        for _ in range(max_iter):
            random_keys = self.random_keys() #Gera uma solução inicial aleatoria
            ini_solution = self.env.decoder(random_keys) 
            ini_cost = self.env.cost(ini_solution)
            if ini_cost < best_ini_cost:
                best_ini_cost = ini_cost
            
            keys = self.LocSearch(random_keys,x) # Refina a solução aleatoria com a Busca Local

            solution = self.env.decoder(keys)
            cost = self.env.cost(solution)
            
            print(f"Iteração {_ + 1}, Custo Inicial: {ini_cost}, Custo Final: {cost}")
            
            if cost < best_cost: # Salva a melhor solução
                best_cost = cost
                best_keys = keys
        
        print(f"Melhor Custo: {best_cost}, Melhor Custo Inicial: {best_ini_cost}")  
        print(f"Melhor Solução: {self.env.decoder(best_keys)}")
        return best_keys, best_cost
        
        
env = VSBPP(hs_instances[0])
solver = Solvers(env)
Solvers.MultiStart(solver, 100, 1000)
