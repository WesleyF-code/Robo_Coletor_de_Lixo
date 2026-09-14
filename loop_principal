import time
import numpy as np
from ambiente import Ambiente
from robo_lixeiro.descartado.agentes03funcionou import AgenteColetor

def rodar_experimento(tipo_agente):
    ambiente = Ambiente(seed=42) # Garante a mesma distribuição de lixos para todos
    agente = AgenteColetor()
    
    passos = 0
    pontuacao = 0
    lixos_coletados = 0
    tempo_inicial = time.time()
    
    # Executa por no máximo 15000 passos para evitar loops infinitos no reativo simples
    while passos < 15000:
        # 1. PEGA A AÇÃO COM BASE NA ARQUITETURA
        if tipo_agente == "reativo_simples":
            acao = agente.agir_reativo_simples(ambiente)
        elif tipo_agente == "baseado_modelos":
            acao = agente.agir_baseado_em_modelos(ambiente)
        elif tipo_agente == "bdi":
            todos_lixos = {(r, c): ambiente.matriz[r][c] for r in range(20) for c in range(20) if ambiente.matriz[r][c] in [1,5]}
            acao = agente.agir_bdi(ambiente, todos_lixos)
        elif tipo_agente == "utilidade":
            todos_lixos = {(r, c): ambiente.matriz[r][c] for r in range(20) for c in range(20) if ambiente.matriz[r][c] in [1,5]}
            acao = agente.agir_utilidade(ambiente, todos_lixos)
        
        # 2. CONTABILIZAÇÃO DE ENTRADA NA LIXEIRA
        if acao == "Soltar Lixo":
            if agente.carga == "Orgânico":
                pontuacao += 1
                lixos_coletados += 1
            elif agente.carga == "Reciclável":
                pontuacao += 5
                lixos_coletados += 1
            agente.carga = None 
            
        passos += 1
        
        # 3. CRITÉRIO DE PARADA: Mapa limpo e agente sem carga
        lixos_restantes = np.any((ambiente.matriz == 1) | (ambiente.matriz == 5))
        if not lixos_restantes and agente.carga is None:
            break
        
    tempo_final = time.time()
    tempo_ms = (tempo_final - tempo_inicial) * 1000
    
    # Formatação exata para bater com as colunas da tabela do relatório
    print(f"| {tipo_agente.upper():<18} | {lixos_coletados:>2}/15 | {pontuacao:>15} | {passos:>12} | {tempo_ms:>21.2f} ms |")
    return lixos_coletados, pontuacao, passos, tempo_ms

if __name__ == "__main__":
    print("\n" + "="*80)
    print(f"{'RESULTADOS EXPERIMENTOS E COMPARATIVO DE DESEMPENHO':^80}")
    print("="*80)
    print(f"| {'Arquitetura do Agente':<18} | {'Lixos':<5} | {'Pontuação Total':<15} | {'Nº de Passos':<12} | {'Tempo de Execução':<24} |")
    print("-"*80)
    
    # Roda consecutivamente as 4 arquiteturas da ficha prática
    rodar_experimento("reativo_simples")
    rodar_experimento("baseado_modelos")
    rodar_experimento("bdi")
    rodar_experimento("utilidade")
    print("="*80 + "\n")
