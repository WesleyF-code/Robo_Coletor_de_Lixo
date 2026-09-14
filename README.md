# 🤖 Robô Coletor de Lixo — Simulação de Agentes de IA

Projeto desenvolvido para a Atividade Prática 1 da disciplina de Inteligência Artificial (Prof. Me. Nerval de Jesus Santos Junior)[cite: 1]. O objetivo é especificar, implementar e comparar quatro arquiteturas de agentes inteligentes na tarefa de varredura, coleta e destinação de resíduos em uma matriz $20\times20$[cite: 1].

---

## 📋 Especificação PEAS

| Componente | Descrição Técnica |
| :--- | :--- |
| **P (Performance)** | Maximizar a pontuação coletando lixo Orgânico (+1) e Reciclável (+5)[cite: 1]; minimizar o número de passos e tempo[cite: 1]. |
| **E (Environment)** | Matriz $20\times20$ estática, discreta, determinística e parcialmente observável (visão dos 8 vizinhos)[cite: 1]. |
| **A (Actuators)** | Movimentação em 8 direções (`N`, `S`, `L`, `O`, `NE`, `NO`, `SE`, `SO`), `Pegar Lixo`, `Soltar Lixo` e `NoOp`[cite: 1, 3]. |
| **S (Sensors)** | Posição $(x, y)$, detector de lixo atual e nos 8 vizinhos, e coordenadas da lixeira em $(20, 20)$[cite: 1]. |

---

## 🧠 Arquiteturas Implementadas

* **Reativo Simples**: Baseado puramente em regras de condição-ação instantâneas e padrão de navegação determinístico ("cortador de grama") quando não há lixo visível[cite: 1, 3].
* **Baseado em Modelos**: Mantém histórico do estado interno via matriz de visitados $V_{20\times20}$ para priorizar células menos exploradas e evitar *loops* redundantes[cite: 1, 3].
* **Baseado em Objetivos (BDI)**: Estrutura mental dividida em Crenças, Desejos e Intenções, priorizando deliberadamente a busca por lixos recicláveis (+5) antes dos orgânicos (+1)[cite: 1, 3].
* **Baseado em Utilidade**: Calcula quantitativamente o trade-off entre o valor do lixo e a distância relativa (Manhattan) entre o agente, o item e a lixeira $X$[cite: 1, 3]:
  $$U = \text{Valor} - (\lambda \cdot D_{\text{Manhattan}}(\text{Agente}, \text{Lixo})) - D_{\text{Manhattan}}(\text{Lixo}, \text{Lixeira})$$[cite: 1, 3]

---

## 📁 Estrutura dos Arquivos

* `ambiente.py`: Define o grid $20\times20$, posição da lixeira (índice `19, 19`), geração aleatória reproduzível via `seed=42` dos 10 lixos orgânicos e 5 recicláveis, e sensor de vizinhança[cite: 5].
* `agentes.py`: Contém a classe `AgenteColetor` com o motor de tomada de decisão para cada uma das 4 arquiteturas de IA[cite: 3].
* `loop_principal.py`: Script de execução em terminal para benchmark quantitativo das arquiteturas em lote.
* `visual_principal.py`: Interface gráfica interativa construída em Tkinter para simulação em tempo real e visualização das rotas do agente.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.8+
* Biblioteca `numpy`

```bash
pip install numpy
