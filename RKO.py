import os
import numpy as np
import time
import random
import copy
from vsbpp import VSBPP 
import math
import datetime
import bisect
from multiprocessing import Manager, Process, cpu_count



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


best_prob = [
    1350, 1310, 1140, 1190, 1090, 1260, 1250, 1250, 1350, 1370,
    1940, 2210, 2700, 2520, 2590, 2320, 2490, 2720, 2140, 2630,
    4870, 5430, 5140, 5170, 4960, 5160, 4770, 4840, 5100, 4640,
    10910, 10290, 10150, 10100, 9910, 10620, 9920, 9900, 9890, 10200,
    25000, 25720, 24340, 25790, 24440, 24870, 25010, 25100, 24920, 25560
]

best_slim = [
    12700, 12140, 13620, 12550, 10630, 11130, 13020, 12180, 11090, 12800,
    25430, 26300, 27770, 24300, 25820, 23820, 28590, 25900, 24890, 25760,
    61770, 62090, 66770, 63970, 62150, 61130, 63340, 63250, 61170, 62000,
    126610, 123250, 123070, 123070, 127710, 125580, 128260, 130410, 125680, 129400,
    254330, 257370, 251880, 248520, 245110, 250930, 258700, 256950, 258480, 255750
]

best_conc = [
    8890, 7832, 8516, 8591, 8474, 7538, 7876, 8116, 8392, 9127,
    17307, 16391, 16637, 15864, 17699, 15457, 16203, 15353, 15860, 15292,
    39307, 40767, 39963, 38945, 39785, 43096, 41307, 39756, 40166, 41046,
    81458, 78523, 81544, 80265, 81076, 81333, 81200, 80899, 78381, 84535,
    160446, 162193, 161879, 161128, 164625, 159107, 162445, 159878, 161694, 153403
]

best_conv = [
    19364, 19000, 18272, 19016, 16612, 18632, 18682, 19517, 17950, 17127,
    35423, 36362, 33390, 34327, 38055, 35009, 38175, 36003, 32700, 36998,
    94768, 97983, 95832, 91068, 87676, 83124, 90407, 87059, 87398, 90541,
    176950, 180993, 182758, 180859, 179158, 188838, 178185, 177461, 181005, 176902,
    356244, 369839, 364550, 356984, 365557, 365142, 360824, 371799, 355723, 357058
]

# Supondo que as listas instances_* e best_* já estejam definidas:

dicionario_best = {
    **dict(zip(instances_prob, best_prob)),
    **dict(zip(instances_slin, best_slim)),
    **dict(zip(instances_conc, best_conc)),
    **dict(zip(instances_conv, best_conv)),
}


class RKO():
    def __init__(self, env):
        self.env = env
        self.__MAX_KEYS = self.env.tam_solution
        
    
    def random_keys(self):
        return np.random.random(self.__MAX_KEYS)
    def inserir_em_elite(self, elite, fitness_elite, key, fitness, tam_elite, modo='maiores'):
        if modo == 'maiores':
            # Lista em ordem decrescente (maior no começo, menor no fim)
            comparar = lambda novo, atual: novo > atual
        elif modo == 'menores':
            # Lista em ordem crescente (menor no começo, maior no fim)
            comparar = lambda novo, atual: novo < atual
        else:
            raise ValueError("modo deve ser 'maiores' ou 'menores'")

        i = 0
        for value in fitness_elite:
            if comparar(fitness, value):
                break
            i += 1

        # Se ainda tem espaço, só insere na posição correta
        if len(elite) < tam_elite:
            elite.insert(i, key)
            fitness_elite.insert(i, fitness)
        else:
            # Se o novo fitness é melhor que o último (pior da elite), substitui
            if comparar(fitness, fitness_elite[-1]):
                elite.pop(-1)
                fitness_elite.pop(-1)
                elite.insert(i, key)
                fitness_elite.insert(i, fitness)

        if modo == 'maiores':
            elite.sort(key=lambda x: fitness_elite[elite.index(x)], reverse=True)
            fitness_elite.sort(reverse=True)
        else:
            elite.sort(key=lambda x: fitness_elite[elite.index(x)])
            fitness_elite.sort()
        return elite, fitness_elite


    def vizinhos(self, keys, min = 0.1, max = 0.25):
   
        new_keys = keys.copy()
        N = len(new_keys)

        # número de posições a perturbar
        min_p = int(min * N)
        max_p = int(max * N)
        n_perturb = random.randint(min_p, max_p)

        for _ in range(n_perturb):
            i = random.randrange(N)
            new_keys[i] = random.random()

        return new_keys
    def pertubacao(self, keys): #Realiza perturbações nas chaves, gerando vizinhos, soluções proximas/parecidas, para a solução atual.
        new_keys = copy.deepcopy(keys)
        prob = random.random()
        if prob < 0.5:
            alteracoes = math.ceil(self.__MAX_KEYS * 0.1) # altera 10% das chaves
            for _ in range(int(alteracoes)):
                idx1, idx2 = random.sample(range(self.__MAX_KEYS), 2)  # Escolhe dois índices distintos aleatórios
                new_keys[idx1], new_keys[idx2] = new_keys[idx2], new_keys[idx1]  # Realiza o swap


        elif prob < 0.7:
            alteracoes = math.ceil(self.__MAX_KEYS * 0.25) # altera 25% das chaves
            for _ in range(int(alteracoes)):
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
    
    def MultiStart(self,max_iter,x, tempo, tag,  pool,lock,best): # Multi Start, gera várias soluções aleatórias e aplica a busca local em cada uma delas, retornando a melhor solução encontrada
        best_keys = None
        best_cost = float('inf')
        best_ini_cost = float('inf')
        start_time = time.time()
        iter = 0
        random_keys = self.random_keys()
        ini_solution = self.env.decoder(random_keys)
        ini_cost = self.env.cost(ini_solution)
        with lock:
            entry = (ini_cost, random_keys)
            
            bisect.insort(pool, entry)       
            if len(pool) > 10:
                pool.pop() 

        while time.time() - start_time < tempo:
            
            
            iter += 1
            k = 0
            while True:
                k+=1
                # print(pool)
                with lock:
                    if len(pool) > 0:
                        # print("POOL")
                        break
            random_keys = random.sample(list(pool), 1)[0][1]
            ini_solution = self.env.decoder(random_keys)
            ini_cost = self.env.cost(ini_solution)
            if ini_cost < best_ini_cost:
                best_ini_cost = ini_cost
            
            keys = self.LocSearch(random_keys,x)

            solution = self.env.decoder(keys)
            cost = self.env.cost(solution)
            with lock:
                entry = (cost, keys)
                
                bisect.insort(pool, entry)       
                if len(pool) > 20:
                    pool.pop()

            # with lock:
            #     if cost < best[0]:
            #         best[0] = cost
            #         best[1] = keys
            #         print(f"\n MS {tag} NOVO MELHOR: {cost} BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}%") 
            
            print(f"\rtempo = {round(time.time() - start_time,2)}", end="")
            
            if cost < best_cost:
                best_cost = cost
                best_keys = keys
                
                print(f"\n MS {tag} NOVO MELHOR: {cost} BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}%") 
                if best_cost == self.env.dict_best[self.env.instance_name]:
                        # print(f" \n{tag} MELHOR: {fitness} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((fitness - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% -  Tempo: {round(time.time() - start_time,2)}s")

                        
                        solution = self.env.decoder(best_keys)
                        cost = self.env.cost(solution, True)  
                        
                            
                            
                        return self.env.bins_usados, best_keys, best_cost
        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)
        # print(f"Melhor Custo: {best_cost}, Melhor Custo Inicial: {best_ini_cost}, tempo = {round(time.time() - start_time,2)}")  

        return self.env.bins_usados,best_keys, best_cost
        

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
        
            
            
        return self.env.bins_usados, best_keys, best_cost
        
        
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
    
    def VNS(self,limit_time,x, tag,  pool,lock,best):
        k = [[0.01, 0.2], [0.2, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 0.99]]
        idx_k = 0
        start_time = time.time()
        bests_S = []
        if self.env.greedy:
            sol = self.env.ssp3()
            s = sol[1]
            bests_S.append(s)
            
            best_cost = sol[0]
            best_keys = s
            
            sol = self.env.greedy_solution_capacity(0)
            s = sol[1]
            bests_S.append(s)

        
            if best_cost > sol[0]:
                best_cost = sol[0]
                best_keys = s
            
            sol = self.env.greedy_solution_cost(0)
            s = sol[1]
            bests_S.append(s)
            
            if best_cost > sol[0]:
                best_cost = sol[0]
                best_keys = s
        else:
            keys = self.random_keys()
            best_keys = keys
            best_cost = self.env.cost(self.env.decoder(keys))
            bests_S.append(keys)
        
        
        
 
        
        print(f"VNS {tag} Melhor Custo: {best_cost} - tempo = {time.time() - start_time}")
        if self.env.dict_best is not None:
            if best_cost == self.env.dict_best[self.env.instance_name]:
                        print(f"VNS {tag} MELHOR: {best_cost} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((best_cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% tempo = {time.time() - start_time}")                        
                        print(f"VNS {tag} ENCERRADO")
                        solution = self.env.decoder(best_keys)
                        cost = self.env.cost(solution, True)  
                            
                                
                                
                        return self.env.bins_usados, best_keys, best_cost    
        
        while time.time() - start_time < limit_time:
            print(f"\rtempo = {round(time.time() - start_time,2)} ", end="")

            if idx_k >= len(k) + 1:
                idx_k = 0
                
            if random.random() < 0.1:
                    s1 = random.sample(list(pool), 1)[0][1]
            
            else:

                if idx_k == len(k):
                    s1 = self.pertubacao(bests_S[random.randint(0, len(bests_S)-1)])
                    # print("Pertubação")
                else:  
                    s1 = self.vizinhos(bests_S[random.randint(0, len(bests_S)-1)], k[idx_k][0], k[idx_k][1])
                    
            # print(s1)
            s2 = self.LocSearch(s1,x)
            
            sol2 = self.env.decoder(s2)
            cost = self.env.cost(sol2)
            # print(tag, cost,best_cost)
            
            if cost <= best_cost:
                best_cost = cost
                best_keys = s2
                
                bests_S.append(s2)
                # print(f"VNS {tag} Melhor Custo: {best_cost} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((best_cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% tempo = {time.time() - start_time}")
                with lock:
                    entry = (best_cost, list(best_keys))
                       
                    bisect.insort(pool, entry)  
                    
                    if len(pool) > 20:
                        pool.pop()
                        
                    if best_cost < best[0]:
                        best[0] = best_cost
                        best[1] = list(best_keys)
                        print(f"VNS {tag} NOVO MELHOR: {best_cost} - tempo = {time.time() - start_time}")
                        
                
                if self.env.dict_best is not None:
                    if best_cost == self.env.dict_best[self.env.instance_name]:
                        print(f"VNS {tag} MELHOR: {best_cost} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((best_cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% tempo = {time.time() - start_time}")                        
                        print(f"VNS {tag} ENCERRADO")
                        solution = self.env.decoder(best_keys)
                        cost = self.env.cost(solution, True)  
                            
                                
                                
                        return self.env.bins_usados, best_keys, best_cost        
            else:
                idx_k += 1

        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)  
        
            
        print(f"VNS {tag} ENCERRADO")
        return self.env.bins_usados, best_keys, best_cost
            
    
    def ILS(self,limit_time,x, tag,  pool,lock,best):

        start_time = time.time()
        bests_S = []
        if self.env.greedy:
            sol = self.env.ssp3()
            s = sol[1]
            bests_S.append(s)
            
            best_cost = sol[0]
            best_keys = s
            
            sol = self.env.greedy_solution_capacity(0)
            s = sol[1]
            bests_S.append(s)

        
            if best_cost > sol[0]:
                best_cost = sol[0]
                best_keys = s
            
            sol = self.env.greedy_solution_cost(0)
            s = sol[1]
            bests_S.append(s)
            
            if best_cost > sol[0]:
                best_cost = sol[0]
                best_keys = s
        else:
            keys = self.random_keys()
            best_keys = keys
            best_cost = self.env.cost(self.env.decoder(keys))
            bests_S.append(keys)
        
        
        
 
        
        
        print(f"ILS {tag} Melhor Custo: {best_cost} - tempo = {time.time() - start_time}")
        if self.env.dict_best is not None:
            if best_cost == self.env.dict_best[self.env.instance_name]:
                        print(f"VNS {tag} MELHOR: {best_cost} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((best_cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% tempo = {time.time() - start_time}")                        
                        print(f"VNS {tag} ENCERRADO")
                        solution = self.env.decoder(best_keys)
                        cost = self.env.cost(solution, True)  
                            
                                
                                
                        return self.env.bins_usados, best_keys, best_cost    
        while time.time() - start_time < limit_time:
            print(f"\rtempo = {round(time.time() - start_time,2)} ", end="")


                
            if random.random() < 0.1:
                    s1 = random.sample(list(pool), 1)[0][1]
            
            else:
                if random.random() < 0.2:
                    s1 = self.pertubacao(bests_S[random.randint(0, len(bests_S)-1)])
                
                else:
                    min = random.random()          
                    max = random.uniform(min, 1.0) 
                    s1 = self.vizinhos(bests_S[random.randint(0, len(bests_S)-1)], min, max)
                    
            s2 = self.LocSearch(s1,x)
            
            sol2 = self.env.decoder(s2)
            cost = self.env.cost(sol2)
            
            
            if cost <= best_cost:
                best_cost = cost
                best_keys = s2
                
                bests_S.append(s2)
                # print(f"ILS {tag} Melhor Custo: {best_cost} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((best_cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% tempo = {time.time() - start_time}")
                with lock:
                    entry = (best_cost, list(best_keys))
                       
                    bisect.insort(pool, entry)  
                    
                    if len(pool) > 20:
                        pool.pop()
                    if best_cost < best[0]:
                        best[0] = best_cost
                        best[1] = list(best_keys)
                        print(f"ILS {tag} NOVO MELHOR: {best_cost} - tempo = {time.time() - start_time}")

                if self.env.dict_best is not None:
                    if best_cost == self.env.dict_best[self.env.instance_name]:
                        print(f"ILS {tag} MELHOR: {best_cost} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((best_cost - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% tempo = {time.time() - start_time}")
                        print(f"ILS {tag} ENCERRADO")
                            
                        solution = self.env.decoder(best_keys)
                        cost = self.env.cost(solution, True)  
                            
                                
                                
                        return self.env.bins_usados, best_keys, best_cost

        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)  
        
            
        print(f"ILS {tag} ENCERRADO")
        return self.env.bins_usados, best_keys, best_cost
    

        
    def BRKGA(self, pop_size, elite_pop, chance_elite, limit_time,tag,pool,lock,best):
        generation = 0
        tam_elite = int(pop_size * elite_pop)
        metade = False
        
        
        if self.env.greedy:
            population = [self.random_keys() for _ in range(pop_size - 3)]
            cost,keys = self.env.ssp3()
            population.append(keys)
            cost,keys = self.env.greedy_solution_capacity(0)
            population.append(keys)
            cost,keys = self.env.greedy_solution_cost(0)
            population.append(keys)
        else:
            population = [self.random_keys() for _ in range(pop_size)]
        best_keys = None
        best_fitness = float('inf')
        
        start_time = time.time()
        
        pop = 0
        qnt = 0
        while time.time() - start_time < limit_time:
            if metade == False:
                metade = True
                if time.time() - start_time > limit_time/2:
                    population = [self.random_keys() for _ in range(pop_size)]
                    # with lock:
                    #     pool = []
            pop += 1
            generation += 1
            
            elite = []
            elite_sol = []
            fitness_elite = []
            
            fitness_values = []

                  
            
            
            for key in population:
                
                qnt += 1
                
                sol = self.env.decoder(key)
                fitness = self.env.cost(sol)
                
                fitness_values.append(fitness)
                

                
                if  not sol in elite_sol:
                    elite.append(key)
                    elite_sol.append(sol)
                    fitness_elite.append(fitness)
                
                
                


                
                if fitness < best_fitness:
                    pop = 0
                    best_keys = key
                    best_fitness = fitness
                    with lock:
                        entry = (best_fitness, list(best_keys))
                        # print(entry)
                        bisect.insort(pool, entry)  
                        # print(pool.type)     
                        if len(pool) > 20:
                            pool.pop()
                        if best_fitness < best[0]:
                            best[0] = best_fitness
                            best[1] = list(best_keys)
                            print(f"BRKGA {tag} NOVO MELHOR: {best_fitness} -  Tempo: {round(time.time() - start_time,2)}s")
          
                        
                    # print(f"BRKGA {tag} Melhor Custo: {fitness} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((fitness - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% -  Tempo: {round(time.time() - start_time,2)}s")
          
                    if self.env.dict_best is not None:
                        if fitness == self.env.dict_best[self.env.instance_name]:
                            print(f" \n{tag} MELHOR: {fitness} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((fitness - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}% -  Tempo: {round(time.time() - start_time,2)}s")
                            print(f"BRKGA {tag} ENCERRADO")
                            
                            solution = self.env.decoder(best_keys)
                            cost = self.env.cost(solution, True)  
                            
                                
                                
                            return self.env.bins_usados, best_keys, best_fitness
        
            ordenado = sorted(zip(elite, fitness_elite), key=lambda x: x[1]) 
            elite, fitness_elite = zip(*ordenado)  

            elite = list(elite)
            fitness_elite = list(fitness_elite)
    
            elite = elite[:tam_elite]
            fitness_elite = fitness_elite[:tam_elite]
            
            
            # print(fitness_elite)

            best_local_fitness = fitness_elite[0]
            best_local_keys = elite[0]


            # with lock:
            #     if fitness_elite[0] < best[0]:
            #         best[0] = fitness_elite[0]
            #         best[1] = elite[0]
            #         print(f" \nBRKGA {tag} NOVO MELHOR: {fitness} - BEST:{self.env.dict_best[self.env.instance_name]} - GAP: {round((fitness - self.env.dict_best[self.env.instance_name]) / self.env.dict_best[self.env.instance_name] * 100, 2)}%")


                        
                        
                # print(pool)
                    
            new_population = [elite[0]]
  

            while len(new_population) < pop_size:
                
                if random.random() < 1:
                    parent1 = random.sample(population, 1)[0]
                else:
                    parent1 = random.sample(list(pool), 1)[0][1]
                    
                if random.random() < 1:
                    parent2 = random.sample(elite, 1)[0]
                else:
                    parent2 = random.sample(list(pool), 1)[0][1]
                    
                
               
                child1 = np.zeros(self.__MAX_KEYS)
                child2 = np.zeros(self.__MAX_KEYS)
                if random.random() < 0.95:
                    for i in range(len(child1)):
                        if random.random() < chance_elite:
                            child1[i] = parent2[i]
                            child2[i] = parent1[i]
                            
                        else:
                            child1[i] = parent1[i]
                            child2[i] = parent2[i]
                else:
                    child1 = parent1
                    child2 = parent2
                
                
                for idx in range(len(child1)):
                    if random.random() < 0.05:
                        
                        child1[idx] = random.random()
                    if random.random() < 0.05:
                        child2[idx] = random.random()                
                new_population.append(child1)
                new_population.append(child2)
            
   
                
     
            population = new_population
            population.pop(0)
            key_pool = random.sample(list(pool), 1)[0][1]
            population.append(key_pool)
            print(f"\rtempo = {round(time.time() - start_time,2)} ", end="")

            # print(f"\r{tag} Geração {generation + 1}: Melhor fitness = {best_fitness}  -  Tempo: {round(time.time() - start_time,2)}s")
            
            
        solution = self.env.decoder(best_keys)
        cost = self.env.cost(solution, True)  
        
            
        # print(qnt)
        print(f"BRKGA {tag} ENCERRADO")    
        return self.env.bins_usados, best_keys, best_fitness

    def solve(self, pop_size, elite_pop, chance_elite, limit_time, n_workers=None,brkga=1, ms=1, sa=1, vns=1, ils=1):
        """Roda múltiplas instâncias de BRKGA em paralelo e compartilha apenas best_solution."""
        if n_workers is None:
            n_workers = cpu_count()



        manager = Manager()
        shared = manager.Namespace()
        shared.best_keys = None
        shared.best_fitness = float('inf')
        shared.best_pair = manager.list([float('inf'), None])
        shared.best_pool = manager.list() 
        lock = manager.Lock()
        processes = []
        tag = 0
        for _ in range(brkga):
            p = Process(
                target=_brkga_worker,
                args=(self.env, pop_size, elite_pop, chance_elite, limit_time, shared, lock,tag)
            )
            tag += 1
            processes.append(p)
            p.start()
        for _ in range(ms):
            p = Process(
                target=_MS_worker,
                args=(self.env,10000,100,limit_time, shared, lock,tag)
            )
            tag += 1
            processes.append(p)
            p.start()
        for _ in range(sa):
            p = Process(
                target=_SA_worker,
                args=( limit_time, shared, lock,tag)
            )
            tag += 1
            processes.append(p)
            p.start()
        for _ in range(vns):
            p = Process(
                target=_VNS_worker,
                args=(self.env, limit_time,pop_size, shared, lock,tag)
            )
            tag += 1
            processes.append(p)
            p.start()
        for _ in range(ils):
            p = Process(
                target=_ILS_worker,
                args=(self.env, limit_time,pop_size, shared, lock,tag)
            )
            tag += 1
            processes.append(p)
            p.start()

        for p in processes:
            p.join()


        solution = self.env.decoder(shared.best_keys)
        
        cost = self.env.cost(solution, True)
        return self.env.bins_usados, shared.best_fitness
        
def _brkga_worker(env, pop_size, elite_pop, chance_elite, limit_time, shared, lock,tag):
    runner = RKO(env)
    _, local_keys, local_best = runner.BRKGA(pop_size, elite_pop, chance_elite, limit_time,tag,shared.best_pool,lock,shared.best_pair)
    
    with lock:
        if local_best < shared.best_fitness:
            shared.best_fitness = local_best
            shared.best_keys = local_keys

def _MS_worker(env, max_itr, x, limit_time, shared, lock,tag):
    runner = RKO(env)
    _, local_keys, local_best = runner.MultiStart( max_itr,x,limit_time,tag,shared.best_pool,lock,shared.best_pair)
    
    with lock:
        if local_best < shared.best_fitness:
            shared.best_fitness = local_best
            shared.best_keys = local_keys
def _GRASP_worker(env, max_itr, x, limit_time, shared, lock,tag):
    runner = RKO(env)
    _, local_keys, local_best = runner.MultiStart( max_itr,x,limit_time,tag,shared.best_pool,lock,shared.best_pair)
    
    with lock:
        if local_best < shared.best_fitness:
            shared.best_fitness = local_best
            shared.best_keys = local_keys
            
def _VNS_worker(env, limit_time, x, shared, lock,tag):
    runner = RKO(env)
    _, local_keys, local_best = runner.VNS(limit_time,x,tag,shared.best_pool,lock,shared.best_pair)
    
    with lock:
        if local_best < shared.best_fitness:
            shared.best_fitness = local_best
            shared.best_keys = local_keys
def _ILS_worker(env, limit_time, x, shared, lock,tag):
    runner = RKO(env)
    _, local_keys, local_best = runner.ILS(limit_time,x,tag,shared.best_pool,lock,shared.best_pair)
    
    with lock:
        if local_best < shared.best_fitness:
            shared.best_fitness = local_best
            shared.best_keys = local_keys

def _SA_worker(env, pop_size, elite_pop, chance_elite, limit_time, shared, lock,tag):
    runner = RKO(env)
    _, local_keys, local_best = runner.SimulatedAnnealing( limit_time,tag,shared.best_pool,lock)
    
    with lock:
        if local_best < shared.best_fitness:
            shared.best_fitness = local_best
            shared.best_keys = local_keys
      
# instances_conc = reversed(instances_conc)  
if __name__ == "__main__":
    agora = datetime.datetime.now()
    nome_arquivo = agora.strftime("resultados_%Y-%m-%d_%H-%M-%S.txt")


    import csv
    from datetime import datetime
    # instances_prob,
    instancias = [ instances_slin[6:],    instances_conv, instances_conc ]
    # instancias = reversed(instancias)
    # set1 = 0
    # set2 = 0
    # set3 = 0
    # set4 = 0
    # for instance in instancias:
    #     with open(f"resultados_greedy_{instance[0]}.csv", "w", newline='') as f_csv:
    #         for ins in instance:
    #             env = VSBPP(ins, dicionario_best)
    #             cost,keys = env.ssp3()
    #             sol = env.decoder(keys)
    #             new_cost = env.cost(sol)
    #             # print(cost,new_cost)
    #             if new_cost == cost:
    #                 if ins in instances_prob:
    #                     set1 += 1
    #                 elif ins in instances_slin:
    #                     set2 += 1
    #                 elif ins in instances_conc:
    #                     set3 += 1
    #                 elif ins in instances_conv:
    #                     set4 += 1
    #                 # print("Deu bom")
    #             f_csv.write(f'{ins}, {int(round(cost,0))}, {dicionario_best[ins]}, {round((cost - dicionario_best[ins]) / dicionario_best[ins] * 100, 2)} \n')
    #             f_csv.flush()
                
    # print(f"Set 1: {set1} de {len(instances_prob)}")
    # print(f"Set 2: {set2} de {len(instances_slin)}")
    # print(f"Set 3: {set3} de {len(instances_conc)}")
    # print(f"Set 4: {set4} de {len(instances_conv)}")
    
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
                
    with open(nome_arquivo, "w") as f_txt, open("resultados.csv", "w", newline='') as f_csv:
        writer_csv = csv.writer(f_csv)
        writer_csv.writerow(["Instancia",  "BRKGA", "BEST", "GAP"])  # cabeçalho do CSV

        for instance in instancias:
            for ins in instance:
                print(f"\nInstancia: {ins} - Best: {dicionario_best[ins]}\n")
                env = VSBPP(ins, dicionario_best)
                best = dicionario_best[ins]
            
                
                agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f_txt.write(f"Instancia: {env.instance_name}, {agora}\n\n")
                f_txt.flush()

                resultados_ms = []
                resultados_brk = []
                resultados_sa = []
                for i in range(3):
                    solver = RKO(env)
                    out = solver.solve(
                        pop_size=int(500),
                        elite_pop=0.05 ,
                        chance_elite=0.7,
                        limit_time=150,       
                        n_workers=6,
                        brkga=brkga,
                        ms=ms,
                        sa=sa,
                        vns=vns,
                        ils=ils)
                    
                    resultados_brk.append(out[1])
                    f_txt.write(f"Resultado BRKGA {i+1}: {out[1]} {out[0]}\n")
                    f_txt.flush()
                    
                media_brk = sum(resultados_brk) / len(resultados_brk)
                best = dicionario_best[ins]
                gap = (media_brk - best) / best * 100
                f_txt.write(f"Media dos resultados MS: {media_brk}\n\n")
                f_txt.flush()
                
                f_csv.write(f'{ins}, {int(round(media_brk,0))}, {best}, {round(gap,2)} \n')
                f_csv.flush()

