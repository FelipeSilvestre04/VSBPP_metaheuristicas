import os
import numpy as np
import random
import copy
from VSBPP import VSBPP 

hs_instances = ['H&Sconc100-1-1.txt', 'H&Sconc100-1-10.txt', 'H&Sconc100-1-2.txt', 'H&Sconc100-1-3.txt', 'H&Sconc100-1-4.txt', 'H&Sconc100-1-5.txt', 'H&Sconc100-1-6.txt', 'H&Sconc100-1-7.txt', 'H&Sconc100-1-8.txt', 'H&Sconc100-1-9.txt', 'H&Sconc100-2-1.txt', 'H&Sconc100-2-10.txt', 'H&Sconc100-2-2.txt', 'H&Sconc100-2-3.txt', 'H&Sconc100-2-4.txt', 'H&Sconc100-2-5.txt', 'H&Sconc100-2-6.txt', 'H&Sconc100-2-7.txt', 'H&Sconc100-2-8.txt', 'H&Sconc100-2-9.txt', 'H&Sconc100-3-1.txt', 'H&Sconc100-3-10.txt', 'H&Sconc100-3-2.txt', 'H&Sconc100-3-3.txt', 'H&Sconc100-3-4.txt', 'H&Sconc100-3-5.txt', 'H&Sconc100-3-6.txt', 'H&Sconc100-3-7.txt', 'H&Sconc100-3-8.txt', 'H&Sconc100-3-9.txt', 'H&Sconc1000-1-1.txt', 'H&Sconc1000-1-10.txt', 'H&Sconc1000-1-2.txt', 'H&Sconc1000-1-3.txt', 'H&Sconc1000-1-4.txt', 'H&Sconc1000-1-5.txt', 'H&Sconc1000-1-6.txt', 'H&Sconc1000-1-7.txt', 'H&Sconc1000-1-8.txt', 'H&Sconc1000-1-9.txt', 'H&Sconc1000-2-1.txt', 'H&Sconc1000-2-10.txt', 'H&Sconc1000-2-2.txt', 'H&Sconc1000-2-3.txt', 'H&Sconc1000-2-4.txt', 'H&Sconc1000-2-5.txt', 'H&Sconc1000-2-6.txt', 'H&Sconc1000-2-7.txt', 'H&Sconc1000-2-8.txt', 'H&Sconc1000-2-9.txt', 'H&Sconc1000-3-1.txt', 'H&Sconc1000-3-10.txt', 'H&Sconc1000-3-2.txt', 'H&Sconc1000-3-3.txt', 'H&Sconc1000-3-4.txt', 'H&Sconc1000-3-5.txt', 'H&Sconc1000-3-6.txt', 'H&Sconc1000-3-7.txt', 'H&Sconc1000-3-8.txt', 'H&Sconc1000-3-9.txt', 'H&Sconc200-1-1.txt', 'H&Sconc200-1-10.txt', 'H&Sconc200-1-2.txt', 'H&Sconc200-1-3.txt', 'H&Sconc200-1-4.txt', 'H&Sconc200-1-5.txt', 'H&Sconc200-1-6.txt', 'H&Sconc200-1-7.txt', 'H&Sconc200-1-8.txt', 'H&Sconc200-1-9.txt', 'H&Sconc200-2-1.txt', 'H&Sconc200-2-10.txt', 'H&Sconc200-2-2.txt', 'H&Sconc200-2-3.txt', 'H&Sconc200-2-4.txt', 'H&Sconc200-2-5.txt', 'H&Sconc200-2-6.txt', 'H&Sconc200-2-7.txt', 'H&Sconc200-2-8.txt', 'H&Sconc200-2-9.txt', 'H&Sconc200-3-1.txt', 'H&Sconc200-3-10.txt', 'H&Sconc200-3-2.txt', 'H&Sconc200-3-3.txt', 'H&Sconc200-3-4.txt', 'H&Sconc200-3-5.txt', 'H&Sconc200-3-6.txt', 'H&Sconc200-3-7.txt', 'H&Sconc200-3-8.txt', 'H&Sconc200-3-9.txt', 'H&Sconc2000-1-1.txt', 'H&Sconc2000-1-10.txt', 'H&Sconc2000-1-2.txt', 'H&Sconc2000-1-3.txt', 'H&Sconc2000-1-4.txt', 'H&Sconc2000-1-5.txt', 'H&Sconc2000-1-6.txt', 'H&Sconc2000-1-7.txt', 'H&Sconc2000-1-8.txt', 'H&Sconc2000-1-9.txt', 'H&Sconc2000-2-1.txt', 'H&Sconc2000-2-10.txt', 'H&Sconc2000-2-2.txt', 'H&Sconc2000-2-3.txt', 'H&Sconc2000-2-4.txt', 'H&Sconc2000-2-5.txt', 'H&Sconc2000-2-6.txt', 'H&Sconc2000-2-7.txt', 'H&Sconc2000-2-8.txt', 'H&Sconc2000-2-9.txt', 'H&Sconc2000-3-1.txt', 'H&Sconc2000-3-10.txt', 'H&Sconc2000-3-2.txt', 'H&Sconc2000-3-3.txt', 'H&Sconc2000-3-4.txt', 'H&Sconc2000-3-5.txt', 'H&Sconc2000-3-6.txt', 'H&Sconc2000-3-7.txt', 'H&Sconc2000-3-8.txt', 'H&Sconc2000-3-9.txt', 'H&Sconc500-1-1.txt', 'H&Sconc500-1-10.txt', 'H&Sconc500-1-2.txt', 'H&Sconc500-1-3.txt', 'H&Sconc500-1-4.txt', 'H&Sconc500-1-5.txt', 'H&Sconc500-1-6.txt', 'H&Sconc500-1-7.txt', 'H&Sconc500-1-8.txt', 'H&Sconc500-1-9.txt', 'H&Sconc500-2-1.txt', 'H&Sconc500-2-10.txt', 'H&Sconc500-2-2.txt', 'H&Sconc500-2-3.txt', 'H&Sconc500-2-4.txt', 'H&Sconc500-2-5.txt', 'H&Sconc500-2-6.txt', 'H&Sconc500-2-7.txt', 'H&Sconc500-2-8.txt', 'H&Sconc500-2-9.txt', 'H&Sconc500-3-1.txt', 'H&Sconc500-3-10.txt', 'H&Sconc500-3-2.txt', 'H&Sconc500-3-3.txt', 'H&Sconc500-3-4.txt', 'H&Sconc500-3-5.txt', 'H&Sconc500-3-6.txt', 'H&Sconc500-3-7.txt', 'H&Sconc500-3-8.txt', 'H&Sconc500-3-9.txt', 'H&Sconv100-1-1.txt', 'H&Sconv100-1-10.txt', 'H&Sconv100-1-2.txt', 'H&Sconv100-1-3.txt', 'H&Sconv100-1-4.txt', 'H&Sconv100-1-5.txt', 'H&Sconv100-1-6.txt', 'H&Sconv100-1-7.txt', 'H&Sconv100-1-8.txt', 'H&Sconv100-1-9.txt', 'H&Sconv100-2-1.txt', 'H&Sconv100-2-10.txt', 'H&Sconv100-2-2.txt', 'H&Sconv100-2-3.txt', 'H&Sconv100-2-4.txt', 'H&Sconv100-2-5.txt', 'H&Sconv100-2-6.txt', 'H&Sconv100-2-7.txt', 'H&Sconv100-2-8.txt', 'H&Sconv100-2-9.txt', 'H&Sconv100-3-1.txt', 'H&Sconv100-3-10.txt', 'H&Sconv100-3-2.txt', 'H&Sconv100-3-3.txt', 'H&Sconv100-3-4.txt', 'H&Sconv100-3-5.txt', 'H&Sconv100-3-6.txt', 'H&Sconv100-3-7.txt', 'H&Sconv100-3-8.txt', 'H&Sconv100-3-9.txt', 'H&Sconv1000-1-1.txt', 'H&Sconv1000-1-10.txt', 'H&Sconv1000-1-2.txt', 'H&Sconv1000-1-3.txt', 'H&Sconv1000-1-4.txt', 'H&Sconv1000-1-5.txt', 'H&Sconv1000-1-6.txt', 'H&Sconv1000-1-7.txt', 'H&Sconv1000-1-8.txt', 'H&Sconv1000-1-9.txt', 'H&Sconv1000-2-1.txt', 'H&Sconv1000-2-10.txt', 'H&Sconv1000-2-2.txt', 'H&Sconv1000-2-3.txt', 'H&Sconv1000-2-4.txt', 'H&Sconv1000-2-5.txt', 'H&Sconv1000-2-6.txt', 'H&Sconv1000-2-7.txt', 'H&Sconv1000-2-8.txt', 'H&Sconv1000-2-9.txt', 'H&Sconv1000-3-1.txt', 'H&Sconv1000-3-10.txt', 'H&Sconv1000-3-2.txt', 'H&Sconv1000-3-3.txt', 'H&Sconv1000-3-4.txt', 'H&Sconv1000-3-5.txt', 'H&Sconv1000-3-6.txt', 'H&Sconv1000-3-7.txt', 'H&Sconv1000-3-8.txt', 'H&Sconv1000-3-9.txt', 'H&Sconv200-1-1.txt', 'H&Sconv200-1-10.txt', 'H&Sconv200-1-2.txt', 'H&Sconv200-1-3.txt', 'H&Sconv200-1-4.txt', 'H&Sconv200-1-5.txt', 'H&Sconv200-1-6.txt', 'H&Sconv200-1-7.txt', 'H&Sconv200-1-8.txt', 'H&Sconv200-1-9.txt', 'H&Sconv200-2-1.txt', 'H&Sconv200-2-10.txt', 'H&Sconv200-2-2.txt', 'H&Sconv200-2-3.txt', 'H&Sconv200-2-4.txt', 'H&Sconv200-2-5.txt', 'H&Sconv200-2-6.txt', 'H&Sconv200-2-7.txt', 'H&Sconv200-2-8.txt', 'H&Sconv200-2-9.txt', 'H&Sconv200-3-1.txt', 'H&Sconv200-3-10.txt', 'H&Sconv200-3-2.txt', 'H&Sconv200-3-3.txt', 'H&Sconv200-3-4.txt', 'H&Sconv200-3-5.txt', 'H&Sconv200-3-6.txt', 'H&Sconv200-3-7.txt', 'H&Sconv200-3-8.txt', 'H&Sconv200-3-9.txt', 'H&Sconv2000-1-1.txt', 'H&Sconv2000-1-10.txt', 'H&Sconv2000-1-2.txt', 'H&Sconv2000-1-3.txt', 'H&Sconv2000-1-4.txt', 'H&Sconv2000-1-5.txt', 'H&Sconv2000-1-6.txt', 'H&Sconv2000-1-7.txt', 'H&Sconv2000-1-8.txt', 'H&Sconv2000-1-9.txt', 'H&Sconv2000-2-1.txt', 'H&Sconv2000-2-10.txt', 'H&Sconv2000-2-2.txt', 'H&Sconv2000-2-3.txt', 'H&Sconv2000-2-4.txt', 'H&Sconv2000-2-5.txt', 'H&Sconv2000-2-6.txt', 'H&Sconv2000-2-7.txt', 'H&Sconv2000-2-8.txt', 'H&Sconv2000-2-9.txt', 'H&Sconv2000-3-1.txt', 'H&Sconv2000-3-10.txt', 'H&Sconv2000-3-2.txt', 'H&Sconv2000-3-3.txt', 'H&Sconv2000-3-4.txt', 'H&Sconv2000-3-5.txt', 'H&Sconv2000-3-6.txt', 'H&Sconv2000-3-7.txt', 'H&Sconv2000-3-8.txt', 'H&Sconv2000-3-9.txt', 'H&Sconv500-1-1.txt', 'H&Sconv500-1-10.txt', 'H&Sconv500-1-2.txt', 'H&Sconv500-1-3.txt', 'H&Sconv500-1-4.txt', 'H&Sconv500-1-5.txt', 'H&Sconv500-1-6.txt', 'H&Sconv500-1-7.txt', 'H&Sconv500-1-8.txt', 'H&Sconv500-1-9.txt', 'H&Sconv500-2-1.txt', 'H&Sconv500-2-10.txt', 'H&Sconv500-2-2.txt', 'H&Sconv500-2-3.txt', 'H&Sconv500-2-4.txt', 'H&Sconv500-2-5.txt', 'H&Sconv500-2-6.txt', 'H&Sconv500-2-7.txt', 'H&Sconv500-2-8.txt', 'H&Sconv500-2-9.txt', 'H&Sconv500-3-1.txt', 'H&Sconv500-3-10.txt', 'H&Sconv500-3-2.txt', 'H&Sconv500-3-3.txt', 'H&Sconv500-3-4.txt', 'H&Sconv500-3-5.txt', 'H&Sconv500-3-6.txt', 'H&Sconv500-3-7.txt', 'H&Sconv500-3-8.txt', 'H&Sconv500-3-9.txt', 'H&Slin100-1-1.txt', 'H&Slin100-1-10.txt', 'H&Slin100-1-2.txt', 'H&Slin100-1-3.txt', 'H&Slin100-1-4.txt', 'H&Slin100-1-5.txt', 'H&Slin100-1-6.txt', 'H&Slin100-1-7.txt', 'H&Slin100-1-8.txt', 'H&Slin100-1-9.txt', 'H&Slin100-2-1.txt', 'H&Slin100-2-10.txt', 'H&Slin100-2-2.txt', 'H&Slin100-2-3.txt', 'H&Slin100-2-4.txt', 'H&Slin100-2-5.txt', 'H&Slin100-2-6.txt', 'H&Slin100-2-7.txt', 'H&Slin100-2-8.txt', 'H&Slin100-2-9.txt', 'H&Slin100-3-1.txt', 'H&Slin100-3-10.txt', 'H&Slin100-3-2.txt', 'H&Slin100-3-3.txt', 'H&Slin100-3-4.txt', 'H&Slin100-3-5.txt', 'H&Slin100-3-6.txt', 'H&Slin100-3-7.txt', 'H&Slin100-3-8.txt', 'H&Slin100-3-9.txt', 'H&Slin1000-1-1.txt', 'H&Slin1000-1-10.txt', 'H&Slin1000-1-2.txt', 'H&Slin1000-1-3.txt', 'H&Slin1000-1-4.txt', 'H&Slin1000-1-5.txt', 'H&Slin1000-1-6.txt', 'H&Slin1000-1-7.txt', 'H&Slin1000-1-8.txt', 'H&Slin1000-1-9.txt', 'H&Slin1000-2-1.txt', 'H&Slin1000-2-10.txt', 'H&Slin1000-2-2.txt', 'H&Slin1000-2-3.txt', 'H&Slin1000-2-4.txt', 'H&Slin1000-2-5.txt', 'H&Slin1000-2-6.txt', 'H&Slin1000-2-7.txt', 'H&Slin1000-2-8.txt', 'H&Slin1000-2-9.txt', 'H&Slin1000-3-1.txt', 'H&Slin1000-3-10.txt', 'H&Slin1000-3-2.txt', 'H&Slin1000-3-3.txt', 'H&Slin1000-3-4.txt', 'H&Slin1000-3-5.txt', 'H&Slin1000-3-6.txt', 'H&Slin1000-3-7.txt', 'H&Slin1000-3-8.txt', 'H&Slin1000-3-9.txt', 'H&Slin200-1-1.txt', 'H&Slin200-1-10.txt', 'H&Slin200-1-2.txt', 'H&Slin200-1-3.txt', 'H&Slin200-1-4.txt', 'H&Slin200-1-5.txt', 'H&Slin200-1-6.txt', 'H&Slin200-1-7.txt', 'H&Slin200-1-8.txt', 'H&Slin200-1-9.txt', 'H&Slin200-2-1.txt', 'H&Slin200-2-10.txt', 'H&Slin200-2-2.txt', 'H&Slin200-2-3.txt', 'H&Slin200-2-4.txt', 'H&Slin200-2-5.txt', 'H&Slin200-2-6.txt', 'H&Slin200-2-7.txt', 'H&Slin200-2-8.txt', 'H&Slin200-2-9.txt', 'H&Slin200-3-1.txt', 'H&Slin200-3-10.txt', 'H&Slin200-3-2.txt', 'H&Slin200-3-3.txt', 'H&Slin200-3-4.txt', 'H&Slin200-3-5.txt', 'H&Slin200-3-6.txt', 'H&Slin200-3-7.txt', 'H&Slin200-3-8.txt', 'H&Slin200-3-9.txt', 'H&Slin2000-1-1.txt', 'H&Slin2000-1-10.txt', 'H&Slin2000-1-2.txt', 'H&Slin2000-1-3.txt', 'H&Slin2000-1-4.txt', 'H&Slin2000-1-5.txt', 'H&Slin2000-1-6.txt', 'H&Slin2000-1-7.txt', 'H&Slin2000-1-8.txt', 'H&Slin2000-1-9.txt', 'H&Slin2000-2-1.txt', 'H&Slin2000-2-10.txt', 'H&Slin2000-2-2.txt', 'H&Slin2000-2-3.txt', 'H&Slin2000-2-4.txt', 'H&Slin2000-2-5.txt', 'H&Slin2000-2-6.txt', 'H&Slin2000-2-7.txt', 'H&Slin2000-2-8.txt', 'H&Slin2000-2-9.txt', 'H&Slin2000-3-1.txt', 'H&Slin2000-3-10.txt', 'H&Slin2000-3-2.txt', 'H&Slin2000-3-3.txt', 'H&Slin2000-3-4.txt', 'H&Slin2000-3-5.txt', 'H&Slin2000-3-6.txt', 'H&Slin2000-3-7.txt', 'H&Slin2000-3-8.txt', 'H&Slin2000-3-9.txt', 'H&Slin500-1-1.txt', 'H&Slin500-1-10.txt', 'H&Slin500-1-2.txt', 'H&Slin500-1-3.txt', 'H&Slin500-1-4.txt', 'H&Slin500-1-5.txt', 'H&Slin500-1-6.txt', 'H&Slin500-1-7.txt', 'H&Slin500-1-8.txt', 'H&Slin500-1-9.txt', 'H&Slin500-2-1.txt', 'H&Slin500-2-10.txt', 'H&Slin500-2-2.txt', 'H&Slin500-2-3.txt', 'H&Slin500-2-4.txt', 'H&Slin500-2-5.txt', 'H&Slin500-2-6.txt', 'H&Slin500-2-7.txt', 'H&Slin500-2-8.txt', 'H&Slin500-2-9.txt', 'H&Slin500-3-1.txt', 'H&Slin500-3-10.txt', 'H&Slin500-3-2.txt', 'H&Slin500-3-3.txt', 'H&Slin500-3-4.txt', 'H&Slin500-3-5.txt', 'H&Slin500-3-6.txt', 'H&Slin500-3-7.txt', 'H&Slin500-3-8.txt', 'H&Slin500-3-9.txt']
monacci_instances = ['prob_100_1.txt', 'prob_100_10.txt', 'prob_100_2.txt', 'prob_100_3.txt', 'prob_100_4.txt', 'prob_100_5.txt', 'prob_100_6.txt', 'prob_100_7.txt', 'prob_100_8.txt', 'prob_100_9.txt', 'prob_200_1.txt', 'prob_200_10.txt', 'prob_200_2.txt', 'prob_200_3.txt', 'prob_200_4.txt', 'prob_200_5.txt', 'prob_200_6.txt', 'prob_200_7.txt', 'prob_200_8.txt', 'prob_200_9.txt', 'prob_25_1.txt', 'prob_25_10.txt', 'prob_25_2.txt', 'prob_25_3.txt', 'prob_25_4.txt', 'prob_25_5.txt', 'prob_25_6.txt', 'prob_25_7.txt', 'prob_25_8.txt', 'prob_25_9.txt', 'prob_500_1.txt', 'prob_500_10.txt', 'prob_500_2.txt', 'prob_500_3.txt', 'prob_500_4.txt', 'prob_500_5.txt', 'prob_500_6.txt', 'prob_500_7.txt', 'prob_500_8.txt', 'prob_500_9.txt', 'prob_50_1.txt', 'prob_50_10.txt', 'prob_50_2.txt', 'prob_50_3.txt', 'prob_50_4.txt', 'prob_50_5.txt', 'prob_50_6.txt', 'prob_50_7.txt', 'prob_50_8.txt', 'prob_50_9.txt'] 



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
            random_keys = self.random_keys()
            ini_solution = self.env.decoder(random_keys)
            ini_cost = self.env.cost(ini_solution)
            if ini_cost < best_ini_cost:
                best_ini_cost = ini_cost
            
            keys = self.LocSearch(random_keys,x)

            solution = self.env.decoder(keys)
            cost = self.env.cost(solution)
            
            print(f"Iteração {_ + 1}, Custo Inicial: {ini_cost}, Custo Final: {cost}")
            
            if cost < best_cost:
                best_cost = cost
                best_keys = keys
        
        print(f"Melhor Custo: {best_cost}, Melhor Custo Inicial: {best_ini_cost}")  
        print(f"Melhor Solução: {self.env.decoder(best_keys)}")
        return best_keys, best_cost
        
        
env = VSBPP(hs_instances[0])
solver = Solvers(env)
Solvers.MultiStart(solver, 10000, 1000)