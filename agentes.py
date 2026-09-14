import numpy as np
import random

# Função de distância calculada via Manhattan de forma rápida
def dist_manhattan_rapida(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class AgenteColetor:
    def __init__(self):
        self.pos = (0, 0) # Começa em (1,1) -> índice 0,0
        self.carga = None # None, 'Orgânico', ou 'Reciclável'
        self.visitados = np.zeros((20, 20), dtype=int) # Memória para o Agente Baseado em Modelos
        self.direcao_varredura = 'L' # Estado reativo simples para o movimento cortador de grama

    def mover_padrao(self, ambiente):
        r, c = self.pos
        
        # Se estiver carregando lixo, segue em linha reta direta para a lixeira (19,19)
        if self.carga is not None:
            dr = np.sign(19 - r)
            dc = np.sign(19 - c)
            direcoes_map = {
                (-1, 0): 'N', (1, 0): 'S', (0, 1): 'L', (0, -1): 'O',
                (-1, 1): 'NE', (-1, -1): 'NO', (1, 1): 'SE', (1, -1): 'SO'
            }
            self.pos = (r + dr, c + dc)
            return f"Mover({direcoes_map.get((dr, dc), 'NoOp')})"

        # Se estiver limpo, faz a varredura linear sistemática (Cortador de Grama)
        if self.direcao_varredura == 'L': # Indo para a direita (Leste)
            if c < 19:
                self.pos = (r, c + 1)
                return "Mover(L)"
            else: # Bateu na parede direita
                if r < 19:
                    self.pos = (r + 1, c)
                    self.direcao_varredura = 'O' # Muda sentido para a Esquerda
                    return "Mover(S)"
                else: # Fim do mapa, reseta para o topo
                    self.pos = (0, 0)
                    self.direcao_varredura = 'L'
                    return "Mover(Reset)"
                    
        elif self.direcao_varredura == 'O': # Indo para a esquerda (Oeste)
            if c > 0:
                self.pos = (r, c - 1)
                return "Mover(O)"
            else: # Bateu na parede esquerda
                if r < 19:
                    self.pos = (r + 1, c)
                    self.direcao_varredura = 'L' # Muda sentido para a Direita
                    return "Mover(S)"
                else: # Fim do mapa, reseta para o topo
                    self.pos = (0, 0)
                    self.direcao_varredura = 'L'
                    return "Mover(Reset)"
        return "NoOp"

    # 1. ARQUITETURA REATIVA SIMPLES
    def agir_reativo_simples(self, ambiente):
        r, c = self.pos
        item_atual = ambiente.matriz[r][c]
        
        # Regra 1: Se está sobre lixo e livre -> Pega
        if item_atual in [1, 5] and self.carga is None:
            self.carga = 'Orgânico' if item_atual == 1 else 'Reciclável'
            ambiente.matriz[r][c] = 0
            return "Pegar Lixo"
            
        # Regra 2: Se está carregando e chegou na lixeira -> Solta
        if self.carga is not None and self.pos == ambiente.lixeira:
            return "Soltar Lixo"
            
        # Regra 3: Se vê lixo nos 8 vizinhos e está livre -> Move até ele
        if self.carga is None:
            vizinhos = ambiente.obter_vizinhos(self.pos)
            for direcao, (conteudo, nova_pos) in vizinhos.items():
                if conteudo in [1,5]:
                    self.pos = nova_pos
                    return f"Mover({direcao})"
                    
        return self.mover_padrao(ambiente)

    # 2. ARQUITETURA BASEADA EM MODELOS
    def agir_baseado_em_modelos(self, ambiente):
        pos_atual = self.pos
        self.visitados[pos_atual[0], pos_atual[1]] += 1
        
        r, c = pos_atual
        item_atual = ambiente.matriz[r][c]
        
        if item_atual in [1, 5] and self.carga is None:
            self.carga = 'Orgânico' if item_atual == 1 else 'Reciclável'
            ambiente.matriz[r][c] = 0
            return "Pegar Lixo"
            
        if self.carga is not None and pos_atual == ambiente.lixeira:
            return "Soltar Lixo"
            
        vizinhos = ambiente.obter_vizinhos(pos_atual)
        if not vizinhos:
            return self.mover_padrao(ambiente)

        # Se estiver carregando lixo, prioriza o vizinho que te aproxima da lixeira
        if self.carga is not None:
            movimentos_lixeira = []
            for direcao, (conteudo, nova_pos) in vizinhos.items():
                d_lixeira = abs(nova_pos[0] - ambiente.lixeira[0]) + abs(nova_pos[1] - ambiente.lixeira[1])
                movimentos_lixeira.append((d_lixeira, direcao, nova_pos))
            movimentos_lixeira.sort(key=lambda x: x[0])
            _, direcao_escolhida, nova_pos_escolhida = movimentos_lixeira[0]
            self.pos = nova_pos_escolhida
            return f"Mover({direcao_escolhida})"

        if self.carga is None:
            for direcao, (conteudo, nova_pos) in vizinhos.items():
                if conteudo in [1,5]:
                    self.pos = nova_pos
                    return f"Mover({direcao})"
        
        # OTIMIZAÇÃO: Seleção do vizinho menos visitado
        melhor_opcao = min(
            vizinhos.items(), 
            key=lambda x: self.visitados[x[1][1][0], x[1][1][1]]
        )
        
        direcao_escolhida, (_, nova_pos_escolhida) = melhor_opcao
        self.pos = nova_pos_escolhida
        return f"Mover({direcao_escolhida})"

    # 3. ARQUITETURA BASEADA EM OBJETIVOS (BDI)
    def agir_bdi(self, ambiente, todos_lixos_conhecidos):
        if self.carga is not None:
            if self.pos == ambiente.lixeira:
                return "Soltar Lixo"
            return self.mover_direto_para(ambiente.lixeira)
        else:
            item_atual = ambiente.matriz[self.pos[0]][self.pos[1]]
            if item_atual in [1,5]:
                self.carga = 'Orgânico' if item_atual == 1 else 'Reciclável'
                ambiente.matriz[self.pos[0]][self.pos[1]] = 0
                return "Pegar Lixo"

            reciclaveis = [pos for pos, tipo in todos_lixos_conhecidos.items() if tipo == 5]
            organicos = [pos for pos, tipo in todos_lixos_conhecidos.items() if tipo == 1]
            
            alvos = reciclaveis if reciclaveis else organicos
            if not alvos:
                return self.mover_padrao(ambiente)
                
            alvo_mais_proximo = min(alvos, key=lambda p: dist_manhattan_rapida(self.pos, p))
            return self.mover_direto_para(alvo_mais_proximo)

    # 4. ARQUITETURA BASEADA EM UTILIDADE
    def agir_utilidade(self, ambiente, todos_lixos_conhecidos, Lambda_param=0.5):
        if self.carga is not None:
            if self.pos == ambiente.lixeira:
                return "Soltar Lixo"
            return self.mover_direto_para(ambiente.lixeira)
            
        item_atual = ambiente.matriz[self.pos[0]][self.pos[1]]
        if item_atual in [1,5]:
            self.carga = 'Orgânico' if item_atual == 1 else 'Reciclável'
            ambiente.matriz[self.pos[0]][self.pos[1]] = 0
            return "Pegar Lixo"

        if not todos_lixos_conhecidos:
            return self.mover_padrao(ambiente)
            
        melhor_lixo = None
        maior_utilidade = -float('inf')
        
        pos_atual = self.pos
        lixeira = ambiente.lixeira
        
        for (r_lixo, c_lixo), tipo_lixo in todos_lixos_conhecidos.items():
            valor = 5 if tipo_lixo == 5 else 1
            d_agente_lixo = abs(pos_atual[0] - r_lixo) + abs(pos_atual[1] - c_lixo)
            d_lixo_lixeira = abs(r_lixo - lixeira[0]) + abs(c_lixo - lixeira[1])
            
            u = valor - (Lambda_param * d_agente_lixo) - d_lixo_lixeira
            
            if u > maior_utilidade:
                maior_utilidade = u
                melhor_lixo = (r_lixo, c_lixo)
                
        if melhor_lixo:
            return self.mover_direto_para(melhor_lixo)
            
        return self.mover_padrao(ambiente)

    def mover_direto_para(self, destino):
        r, c = self.pos
        dr = np.sign(destino[0] - r)
        dc = np.sign(destino[1] - c)
        
        direcoes_map = {
            (-1, 0): 'N', (1, 0): 'S', (0, 1): 'L', (0, -1): 'O',
            (-1, 1): 'NE', (-1, -1): 'NO', (1, 1): 'SE', (1, -1): 'SO'
        }
        
        self.pos = (r + dr, c + dc)
        return f"Mover({direcoes_map.get((dr, dc), 'NoOp')})"
