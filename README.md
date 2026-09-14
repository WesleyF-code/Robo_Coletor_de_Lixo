# 🤖 Robô Coletor de Lixo — Simulação de Agentes de IA

Projeto desenvolvido para a Atividade Prática 1 da disciplina de Inteligência Artificial (Prof. Me. Nerval de Jesus Santos Junior). O objetivo é especificar, implementar e comparar quatro arquiteturas de agentes inteligentes na tarefa de varredura, coleta e destinação de resíduos em uma matriz $20\times20$.

---

## 📋 Especificação PEAS

| Componente | Descrição Técnica |
| :--- | :--- |
| **P (Performance)** | Maximizar a pontuação coletando lixo Orgânico (+1) e Reciclável (+5); minimizar o número de passos e tempo. |
| **E (Environment)** | Matriz $20\times20$ estática, discreta, determinística e parcialmente observável (visão dos 8 vizinhos). |
| **A (Actuators)** | Movimentação em 8 direções (`N`, `S`, `L`, `O`, `NE`, `NO`, `SE`, `SO`), `Pegar Lixo`, `Soltar Lixo` e `NoOp`. |
| **S (Sensors)** | Posição $(x, y)$, detector de lixo atual e nos 8 vizinhos, e coordenadas da lixeira em $(20, 20)$. |

---

## 🧠 Arquiteturas Implementadas

* **Reativo Simples**: Baseado puramente em regras de condição-ação instantâneas e padrão de navegação determinístico ("cortador de grama") quando não há lixo visível.
* **Baseado em Modelos**: Mantém histórico do estado interno via matriz de visitados $V_{20\times20}$ para priorizar células menos exploradas e evitar *loops* redundantes.
* **Baseado em Objetivos (BDI)**: Estrutura mental dividida em Crenças, Desejos e Intenções, priorizando deliberadamente a busca por lixos recicláveis (+5) antes dos orgânicos (+1).
* **Baseado em Utilidade**: Calcula quantitativamente o trade-off entre o valor do lixo e a distância relativa (Manhattan) entre o agente, o item e a lixeira $X$:
  $$U = \text{Valor} - (\lambda \cdot D_{\text{Manhattan}}(\text{Agente}, \text{Lixo})) - D_{\text{Manhattan}}(\text{Lixo}, \text{Lixeira})$$

---

## 📁 Estrutura dos Arquivos

* `ambiente.py`: Define o grid $20\times20$, posição da lixeira (índice `19, 19`), geração aleatória reproduzível via `seed=42` dos 10 lixos orgânicos e 5 recicláveis, e sensor de vizinhança.
* `agentes.py`: Contém a classe `AgenteColetor` com o motor de tomada de decisão para cada uma das 4 arquiteturas de IA.
* `loop_principal.py`: Script de execução em terminal para benchmark quantitativo das arquiteturas em lote.
* `visual_principal.py`: Interface gráfica interativa construída em Tkinter para simulação em tempo real e visualização das rotas do agente.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.8+
* Biblioteca `numpy`

```bash
pip install numpy

---

## 👥 Integrantes da Equipe

* **Claudio Roberto Andrade Araujo** - Matrícula: 2019039362
* **Hector Fernandes Oliveira** - Matrícula: 2022013869
* **Millena Gomes Andrade de Menezes Braga** - Matrícula: 2023041572
* **Nickolas Ferreira Maiolino** - Matrícula: 20260000716
* **Wesley Ferreira Costa** - Matrícula: 2023034442
