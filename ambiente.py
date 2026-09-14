import numpy as np
import random

class Ambiente:
    def __init__(self, seed=42):
        self.tamanho = 20
        self.lixeira = (19, 19) # Posição (20,20) em índice 0-indexed (0 a 19)
        self.seed = seed
        self.reset()

    def reset(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        # 0: Vazio, 1: Orgânico (+1), 5: Reciclável (+5)
        self.matriz = np.zeros((self.tamanho, self.tamanho), dtype=int)
        
        # Posicionar 10 lixos orgânicos e 5 recicláveis aleatoriamente
        posicoes_possiveis = [(r, c) for r in range(self.tamanho) for c in range(self.tamanho) 
                              if (r, c) != (0, 0) and (r, c) != self.lixeira]
        random.shuffle(posicoes_possiveis)
        
        for _ in range(10):
            r, c = posicoes_possiveis.pop()
            self.matriz[r][c] = 1 # Orgânico
            
        for _ in range(5):
            r, c = posicoes_possiveis.pop()
            self.matriz[r][c] = 5 # Reciclável

    def obter_vizinhos(self, pos):
        # Retorna o que está nas 8 células vizinhas imediatas
        r, c = pos
        vizinhos = {}
        dr = [-1, -1, -1, 0, 0, 1, 1, 1]
        dc = [-1, 0, 1, -1, 1, -1, 0, 1]
        direcoes = ['NO', 'N', 'NE', 'O', 'L', 'SO', 'S', 'SE']
        
        for i in range(8):
            nr, nc = r + dr[i], c + dc[i]
            if 0 <= nr < self.tamanho and 0 <= nc < self.tamanho:
                vizinhos[direcoes[i]] = (self.matriz[nr][nc], (nr, nc))
        return vizinhos

