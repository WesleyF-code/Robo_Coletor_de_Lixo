import tkinter as tk
import time
import numpy as np
from ambiente import Ambiente
from agentes import AgenteColetor

TAMANHO_CELULA = 30
TAMANHO_MATRIZ = 20

class SimuladorVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de IA - Robô Lixeiro (Modo Sequencial)")
        
        self.sequencia_arquiteturas = ["reativo_simples", "baseado_modelos", "bdi", "utilidade"]
        self.indice_atual = 0
        
        self.resultados_finais = []
        
        self.canvas = tk.Canvas(root, width=TAMANHO_MATRIZ*TAMANHO_CELULA, height=TAMANHO_MATRIZ*TAMANHO_CELULA, bg="#f0f0f0")
        self.canvas.pack()
        
        self.status_var = tk.StringVar()
        self.label_status = tk.Label(root, textvariable=self.status_var, font=("Courier", 11, "bold"), bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=10, pady=10)
        self.label_status.pack(fill=tk.X)
        
        self.inicializar_agente_atual()

    def inicializar_agente_atual(self):
        self.arquitetura_atual = self.sequencia_arquiteturas[self.indice_atual]
        self.ambiente = Ambiente(seed=42)
        self.agente = AgenteColetor()
        
        self.passos = 0
        self.pontuacao = 0
        self.lixos_coletados = 0
        self.tempo_inicial = time.time()

        # Como o robô vai andar por várias células repetidas vezes, o set garante que a mesma
        # coordenada (linha, coluna) não seja adicionada duas vezes na memória, poupando processamento.
        self.caminho_percorrido = set()
        
        self.atualizar_simulacao()

    def desenhar_mundo(self):
        self.canvas.delete("all")
        
        for r in range(TAMANHO_MATRIZ):
            for c in range(TAMANHO_MATRIZ):
                x1, y1 = c * TAMANHO_CELULA, r * TAMANHO_CELULA
                x2, y2 = x1 + TAMANHO_CELULA, y1 + TAMANHO_CELULA
                

               # Se a célula atual (r, c) foi visitada pelo robô, pintamos de azul claro
                if (r, c) in self.caminho_percorrido:
                    cor_fundo = "#1C6826"  # Azul bem claro para o rastro
                else:
                    cor_fundo = "#000000"  # Cor cinza padrão original do fundo
                    

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor_fundo, outline="#0D2424")

                #self.canvas.create_rectangle(x1, y1, x2, y2, outline="#dcdcdc")
                
                conteudo = self.ambiente.matriz[r][c]
                if (r, c) == self.ambiente.lixeira:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2637cf", outline="#dcdcdc")
                elif conteudo == 1:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="#a3a39e")
                elif conteudo == 5:
                    #self.canvas.creat_oval(x1+5, y1+5, x2-5, y2-5, fill="#f0ff1e")
                    self.canvas.create_text(x1 + TAMANHO_CELULA/2, y1 + TAMANHO_CELULA/2, text="5", fill="#fffb1e", font=("Arial", 14, "bold"))

        r_ag, c_ag = self.agente.pos
        ax1, ay1 = c_ag * TAMANHO_CELULA, r_ag * TAMANHO_CELULA
        ax2, ay2 = ax1 + TAMANHO_CELULA, ay1 + TAMANHO_CELULA
        self.canvas.create_rectangle(ax1, ay1, ax2, ay2, fill="#ff4500", outline="#ffffff")
        
        if self.agente.carga == "Orgânico":
            self.canvas.create_oval(ax1+10, ay1+10, ax2-10, ay2-10, fill="#8b4513")
        elif self.agente.carga == "Reciclável":
            self.canvas.create_oval(ax1+10, ay1+10, ax2-10, ay2-10, fill="#1e90ff")

        tempo_decorrido_ms = (time.time() - self.tempo_inicial) * 1000
        
        self.status_var.set(
            f"AGENTE: {self.arquitetura_atual.upper():<16} | "
            f"PASSOS: {self.passos:>4} | "
            f"PONTOS: {self.pontuacao:>2} | "
            f"TEMPO: {tempo_decorrido_ms:>7.2f} ms"
        )

    def imprimir_tabela_terminal(self):
        print("\n" + "="*84)
        print(f"{'RESULTADOS EXPERIMENTOS E COMPARATIVO DE DESEMPENHO':^84}")
        print("="*84)
        print(f"| {'Arquitetura do Agente':<20} | {'Lixos':<6} | {'Pontuação Total':<15} | {'Nº de Passos':<12} | {'Tempo de Execução':<18} |")
        print("-"*84)
        for res in self.resultados_finais:
            print(f"| {res['nome'].upper():<20} | {res['lixos']:>2}/15  | {res['pontos']:>15} | {res['passos']:>12} | {res['tempo']:>14.2f} ms |")
        print("="*84 + "\n")

    def atualizar_simulacao(self):
        #Toda vez que a função rodar (ou seja, a cada passo que o robô der), o simulador vai pegar a coordenada (linha, coluna) onde
        #o agente está naquele exato momento (self.agente.pos) e vai colocá-la dentro da nossa lista de locais visitados.
        self.caminho_percorrido.add(self.agente.pos)

        lixos_restantes = np.any((self.ambiente.matriz == 1) | (self.ambiente.matriz == 5))

        # Critério de parada do agente atual: mapa limpo e robô sem carga OU limite de segurança de passos atingido
        if (not lixos_restantes and self.agente.carga is None) or self.passos >= 3000:
            self.desenhar_mundo()
            self.root.update()
            time.sleep(1.5)
            
            tempo_final_ms = (time.time() - self.tempo_inicial) * 1000
            
            self.resultados_finais.append({
                "nome": self.arquitetura_atual,
                "lixos": self.lixos_coletados,
                "pontos": self.pontuacao,
                "passos": self.passos,
                "tempo": tempo_final_ms
            })
            
            self.indice_atual += 1
            if self.indice_atual < len(self.sequencia_arquiteturas):
                self.inicializar_agente_atual()
            else:
                self.status_var.set("FIM DE TODOS OS EXPERIMENTOS! Relatório gerado no terminal.")
                self.imprimir_tabela_terminal()
            return

        if self.arquitetura_atual == "reativo_simples":
            acao = self.agente.agir_reativo_simples(self.ambiente)
        elif self.arquitetura_atual == "baseado_modelos":
            acao = self.agente.agir_baseado_em_modelos(self.ambiente)
        elif self.arquitetura_atual == "bdi":
            todos_lixos = {(r, c): self.ambiente.matriz[r][c] for r in range(20) for c in range(20) if self.ambiente.matriz[r][c] in [1,5]}
            acao = self.agente.agir_bdi(self.ambiente, todos_lixos)
        elif self.arquitetura_atual == "utilidade":
            todos_lixos = {(r, c): self.ambiente.matriz[r][c] for r in range(20) for c in range(20) if self.ambiente.matriz[r][c] in [1,5]}
            acao = self.agente.agir_utilidade(self.ambiente, todos_lixos)

        if acao == "Soltar Lixo":
            if self.agente.carga == "Orgânico":
                self.pontuacao += 1
                self.lixos_coletados += 1
            elif self.agente.carga == "Reciclável":
                self.pontuacao += 5
                self.lixos_coletados += 1
            self.agente.carga = None
            
        self.passos += 1
        self.desenhar_mundo()
        
        # Altere o valor de 40 para 10 se quiser que a animação rode muito mais rápido na tela
        self.root.after(10, self.atualizar_simulacao)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorVisual(root)
    root.mainloop()
