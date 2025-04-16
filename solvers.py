import os
import numpy as np
import time
import random
import copy
from vsbpp import VSBPP 
import math
import datetime


instances_conc = ["H&Sconc100-2-1.txt", "H&Sconc100-2-2.txt", "H&Sconc100-2-3.txt", "H&Sconc100-2-4.txt", "H&Sconc100-2-5.txt","H&Sconc100-2-6.txt", "H&Sconc100-2-7.txt", "H&Sconc100-2-8.txt", "H&Sconc100-2-9.txt", "H&Sconc100-2-10.txt","H&Sconc200-2-1.txt", "H&Sconc200-2-2.txt", "H&Sconc200-2-3.txt", "H&Sconc200-2-4.txt", "H&Sconc200-2-5.txt","H&Sconc200-2-6.txt", "H&Sconc200-2-7.txt", "H&Sconc200-2-8.txt", "H&Sconc200-2-9.txt", "H&Sconc200-2-10.txt","H&Sconc500-2-1.txt", "H&Sconc500-2-2.txt", "H&Sconc500-2-3.txt", "H&Sconc500-2-4.txt", "H&Sconc500-2-5.txt","H&Sconc500-2-6.txt", "H&Sconc500-2-7.txt", "H&Sconc500-2-8.txt", "H&Sconc500-2-9.txt", "H&Sconc500-2-10.txt","H&Sconc1000-2-1.txt", "H&Sconc1000-2-2.txt", "H&Sconc1000-2-3.txt", "H&Sconc1000-2-4.txt", "H&Sconc1000-2-5.txt","H&Sconc1000-2-6.txt", "H&Sconc1000-2-7.txt", "H&Sconc1000-2-8.txt", "H&Sconc1000-2-9.txt", "H&Sconc1000-2-10.txt","H&Sconc2000-2-1.txt", "H&Sconc2000-2-2.txt", "H&Sconc2000-2-3.txt", "H&Sconc2000-2-4.txt", "H&Sconc2000-2-5.txt","H&Sconc2000-2-6.txt", "H&Sconc2000-2-7.txt", "H&Sconc2000-2-8.txt", "H&Sconc2000-2-9.txt", "H&Sconc2000-2-10.txt"]
             
             
instances_conv = ["H&Sconv100-3-1.txt", "H&Sconv100-3-2.txt", "H&Sconv100-3-3.txt", "H&Sconv100-3-4.txt", "H&Sconv100-3-5.txt","H&Sconv100-3-6.txt", "H&Sconv100-3-7.txt", "H&Sconv100-3-8.txt", "H&Sconv100-3-9.txt", "H&Sconv100-3-10.txt","H&Sconv200-3-1.txt", "H&Sconv200-3-2.txt", "H&Sconv200-3-3.txt", "H&Sconv200-3-4.txt", "H&Sconv200-3-5.txt","H&Sconv200-3-6.txt", "H&Sconv200-3-7.txt", "H&Sconv200-3-8.txt", "H&Sconv200-3-9.txt", "H&Sconv200-3-10.txt",
"H&Sconv500-3-1.txt", "H&Sconv500-3-2.txt", "H&Sconv500-3-3.txt", "H&Sconv500-3-4.txt", "H&Sconv500-3-5.txt",
"H&Sconv500-3-6.txt", "H&Sconv500-3-7.txt", "H&Sconv500-3-8.txt", "H&Sconv500-3-9.txt", "H&Sconv500-3-10.txt",
"H&Sconv1000-3-1.txt", "H&Sconv1000-3-2.txt", "H&Sconv1000-3-3.txt", "H&Sconv1000-3-4.txt", "H&Sconv1000-3-5.txt",
"H&Sconv1000-3-6.txt", "H&Sconv1000-3-7.txt", "H&Sconv1000-3-8.txt", "H&Sconv1000-3-9.txt", "H&Sconv1000-3-10.txt",
"H&Sconv2000-3-1.txt", "H&Sconv2000-3-2.txt", "H&Sconv2000-3-3.txt", "H&Sconv2000-3-4.txt", "H&Sconv2000-3-5.txt",
"H&Sconv2000-3-6.txt", "H&Sconv2000-3-7.txt", "H&Sconv2000-3-8.txt", "H&Sconv2000-3-9.txt", "H&Sconv2000-3-10.txt"]


instances_slin = ["H&Slin100-1-1.txt", "H&Slin100-1-2.txt", "H&Slin100-1-3.txt", "H&Slin100-1-4.txt", "H&Slin100-1-5.txt",
"H&Slin100-1-6.txt", "H&Slin100-1-7.txt", "H&Slin100-1-8.txt", "H&Slin100-1-9.txt", "H&Slin100-1-10.txt",
"H&Slin200-1-1.txt", "H&Slin200-1-2.txt", "H&Slin200-1-3.txt", "H&Slin200-1-4.txt", "H&Slin200-1-5.txt",
"H&Slin200-1-6.txt", "H&Slin200-1-7.txt", "H&Slin200-1-8.txt", "H&Slin200-1-9.txt", "H&Slin200-1-10.txt",
"H&Slin500-1-1.txt", "H&Slin500-1-2.txt", "H&Slin500-1-3.txt", "H&Slin500-1-4.txt", "H&Slin500-1-5.txt",
"H&Slin500-1-6.txt", "H&Slin500-1-7.txt", "H&Slin500-1-8.txt", "H&Slin500-1-9.txt", "H&Slin500-1-10.txt",
"H&Slin1000-1-1.txt", "H&Slin1000-1-2.txt", "H&Slin1000-1-3.txt", "H&Slin1000-1-4.txt", "H&Slin1000-1-5.txt",
"H&Slin1000-1-6.txt", "H&Slin1000-1-7.txt", "H&Slin1000-1-8.txt", "H&Slin1000-1-9.txt", "H&Slin1000-1-10.txt",
"H&Slin2000-1-1.txt", "H&Slin2000-1-2.txt", "H&Slin2000-1-3.txt", "H&Slin2000-1-4.txt", "H&Slin2000-1-5.txt",
"H&Slin2000-1-6.txt", "H&Slin2000-1-7.txt", "H&Slin2000-1-8.txt", "H&Slin2000-1-9.txt", "H&Slin2000-1-10.txt"]

instances_prob = ["prob_25_1.txt", "prob_25_2.txt", "prob_25_3.txt", "prob_25_4.txt", "prob_25_5.txt",
"prob_25_6.txt", "prob_25_7.txt", "prob_25_8.txt", "prob_25_9.txt", "prob_25_10.txt",
"prob_50_1.txt", "prob_50_2.txt", "prob_50_3.txt", "prob_50_4.txt", "prob_50_5.txt",
"prob_50_6.txt", "prob_50_7.txt", "prob_50_8.txt", "prob_50_9.txt", "prob_50_10.txt",
"prob_100_1.txt", "prob_100_2.txt", "prob_100_3.txt", "prob_100_4.txt", "prob_100_5.txt",
"prob_100_6.txt", "prob_100_7.txt", "prob_100_8.txt", "prob_100_9.txt", "prob_100_10.txt",
"prob_200_1.txt", "prob_200_2.txt", "prob_200_3.txt", "prob_200_4.txt", "prob_200_5.txt",
"prob_200_6.txt", "prob_200_7.txt", "prob_200_8.txt", "prob_200_9.txt", "prob_200_10.txt",
"prob_500_1.txt", "prob_500_2.txt", "prob_500_3.txt", "prob_500_4.txt", "prob_500_5.txt",
"prob_500_6.txt", "prob_500_7.txt", "prob_500_8.txt", "prob_500_9.txt", "prob_500_10.txt"
]




class Solvers():
    def __init__(self, env):
        self.env = env
        self.__MAX_KEYS = self.env.tam_solution
        
    
    def random_keys(self):
        return np.random.random(self.__MAX_KEYS)
    
    def vizinhos(self, keys): #Realiza perturbações nas chaves, gerando vizinhos, soluções proximas/parecidas, para a solução atual.
        new_keys = copy.deepcopy(keys)
        prob = random.random()
        if prob < 0.5:
            alteracoes = math.ceil(self.__MAX_KEYS * 0.1) # altera 10% das chaves
            for _ in range(alteracoes):
                idx1, idx2 = random.sample(range(self.__MAX_KEYS), 2)  # Escolhe dois índices distintos aleatórios
                new_keys[idx1], new_keys[idx2] = new_keys[idx2], new_keys[idx1]  # Realiza o swap


        elif prob < 0.7:
            alteracoes = math.ceil(self.__MAX_KEYS * 0.25) # altera 25% das chaves
            for _ in range(alteracoes):
                idx1, idx2 = random.sample(range(self.__MAX_KEYS), 2)  # Escolhe dois índices distintos aleatórios
                new_keys[idx1], new_keys[idx2] = new_keys[idx2], new_keys[idx1]  # Realiza o swap


        elif  prob < 0.9:     
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
    
    def MultiStart(self,max_iter,x, tempo = None): # Multi Start, gera várias soluções aleatórias e aplica a busca local em cada uma delas, retornando a melhor solução encontrada
        best_keys = None
        best_cost = float('inf')
        best_ini_cost = float('inf')
        start_time = time.time()
        iter = 0
        while iter < max_iter and time.time() - start_time < tempo:
            
            
            iter += 1
            random_keys = self.random_keys()
            ini_solution = self.env.decoder(random_keys)
            ini_cost = self.env.cost(ini_solution)
            if ini_cost < best_ini_cost:
                best_ini_cost = ini_cost
            
            keys = self.LocSearch(random_keys,x)

            solution = self.env.decoder(keys)
            cost = self.env.cost(solution)
            
            print(f"Iteração {iter}, Custo Inicial: {ini_cost}, Custo Final: {cost}, tempo = {round(time.time() - start_time,2)}")
            
            if cost < best_cost:
                best_cost = cost
                best_keys = keys
        
        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)
        print(f"Melhor Custo: {best_cost}, Melhor Custo Inicial: {best_ini_cost}, tempo = {round(time.time() - start_time,2)}")  

        return self.env.bins_usados, best_cost
        

    def SimulatedAnnealing(self,SAmax,Temperatura,alpha, tempo_max):
        keys = self.random_keys()
        best_keys = keys
        
        solution = self.env.decoder(keys)
        cost = self.env.cost(solution)
        best_cost = cost
        
        start_time = time.time()
        
        T = Temperatura
        iter_total = 0
        iter = 0
        while time.time() - start_time < tempo_max:
            
            while iter < SAmax:
                print(f"\rTempo: {round(time.time() - start_time,2):.1f}s  -  Temperatura {T:.1f}  -  ", end="")
                iter+= 1
                iter_total += 1
                                
                new_keys = self.vizinhos(keys)
                                        
                new_solution = self.env.decoder(new_keys)
                new_cost = self.env.cost(new_solution)
                
                
                delta = new_cost - cost
                
                if new_cost < best_cost:
                    best_keys = new_keys
                    best_cost = new_cost
                    
                    print(f" NOVO MELHOR: {best_cost}")
                    
                               
                if delta <= 0:
                    keys = new_keys
                    cost = new_cost
                else:
                    if random.random() < math.exp(-delta/T):
                        keys = new_keys
                        cost = new_cost
                        
            iter = 0
            T = T * alpha
            
        print(f"Melhor Custo: {best_cost}, tempo = {round(time.time() - start_time,2)}")
        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)  
        
            
            
        return self.env.bins_usados, best_cost
        
        
    def GRASP(self,max_iter,x, tempo = None): # GRASP, gera várias soluções semi gulosas e aplica a busca local em cada uma delas, retornando a melhor solução encontrada
        best_keys = None
        best_cost = float('inf')
        best_ini_cost = float('inf')
        start_time = time.time()
        iter = 0
        while iter < max_iter or time.time() - start_time < tempo:
            iter += 1
            random_keys = self.env.greedy_solution(10)
            ini_solution = self.env.decoder(random_keys)
            ini_cost = self.env.cost(ini_solution)
            if ini_cost < best_ini_cost:
                best_ini_cost = ini_cost
            
            keys = self.LocSearch(random_keys,x)

            solution = self.env.decoder(keys)
            cost = self.env.cost(solution)
            
            print(f"Iteração {iter}, Custo Inicial: {ini_cost}, Custo Final: {cost}, tempo = {time.time() - start_time}")
            
            if cost < best_cost:
                best_cost = cost
                best_keys = keys
        
        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)
        print(f"Melhor Custo: {best_cost}, Melhor Custo Inicial: {best_ini_cost}, tempo = {time.time() - start_time}")  

        return best_keys, best_cost
    
    def VNS(self):
        pass
    
    def ILS(self):
        pass
    

        
    def BRKGA(self):
        pass
    
    



agora = datetime.datetime.now()
nome_arquivo = agora.strftime("resultados_%Y-%m-%d_%H-%M-%S.txt")


with open(nome_arquivo, "w") as f: #APENAS PARA TESTE
    for ins in instances_prob:
        env = VSBPP(ins)
        solver = Solvers(env)
        
        f.write(f"Instancia: {env.instance_name}\n\n")
        f.flush()

        resultados_ms = []
        resultados_sa = []
        for i in range(10):
            out = solver.MultiStart(10000, 3000, 150)
            resultados_ms.append(out[1])
            f.write(f"Resultado MS {i+1}: {out[1]} {out[0]}\n")
            f.flush()

            out = solver.SimulatedAnnealing(500, 10000, 0.995, 150)
            resultados_sa.append(out[1])
            f.write(f"Resultado SA {i+1}: {out[1]} {out[0]}\n")
            f.flush()

        media_ms = sum(resultados_ms) / len(resultados_ms)
        f.write(f"Média dos resultados MS: {media_ms}\n\n")
        f.flush()

        media_sa = sum(resultados_sa) / len(resultados_sa)
        f.write(f"Média dos resultados SA: {media_sa}\n\n")
        f.flush()
