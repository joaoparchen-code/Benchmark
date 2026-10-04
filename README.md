# Benchmark de Operações de Memória: Windows vs Linux

Este repositório contém os scripts e as instruções necessárias para reproduzir o experimento comparativo de desempenho em operações de memória (alocação, escrita, leitura e liberação) entre os sistemas operacionais Windows e Linux.

## Pré-requisitos

Para garantir a validade científica e a reprodutibilidade do experimento, os testes devem ser executados em ambientes controlados com configurações idênticas.

**Hardware Físico Sugerido:**
* Processador: Intel i5-9300H 2.4GHz (ou equivalente)
* Memória RAM: Mínimo de 16 GB (para permitir VMs com 8GB)
* Armazenamento SSD

**Ambiente de Virtualização:**
* **Software:** VirtualBox (versão 7.2.16r ou compatível)
* **VM 1 (Linux):** Ubuntu Server 25.04
* **VM 2 (Windows):** Windows Server 2022
* **Configuração das VMs:** 4 vCPUs e 8192 MB de RAM para cada.

**Dependências de Software (em ambas as VMs):**
* Python 3.14.x (Arquitetura x64)
* Bibliotecas Python para análise (necessárias apenas na máquina que fará a geração dos gráficos):
  ```bash
  pip install pandas matplotlib seaborn
  ```

## Passo a Passo para Execução

### Etapa 1: Coleta de Dados no Linux (Ubuntu Server)
1. Inicie a máquina virtual do Linux (certifique-se de que a VM do Windows esteja **desligada**).
2. Feche todas as aplicações em segundo plano desnecessárias no sistema hospedeiro e na VM.
3. Abra o arquivo `microbenchmark.py` e altere a última linha do código para salvar o arquivo com o nome correto:
   ```python
   executar_microbenchmark("resultados_linux.csv")
   ```
4. Execute o script no terminal:
   ```bash
   python microbenchmark.py
   ```
5. Aguarde a conclusão dos testes (blocos de 100MB a 1000MB, 100 repetições cada). O arquivo `resultados_linux.csv` será gerado.
6. Transfira este arquivo CSV para a máquina onde a análise será feita e desligue a VM do Linux.

### Etapa 2: Coleta de Dados no Windows (Windows Server)
1. Inicie a máquina virtual do Windows (certifique-se de que a VM do Linux esteja **desligada**).
2. Repita o processo de fechamento de aplicações em segundo plano.
3. Abra o arquivo `microbenchmark.py` e altere a última linha para:
   ```python
   executar_microbenchmark("resultados_windows.csv")
   ```
4. Execute o script via Prompt de Comando ou PowerShell:
   ```cmd
   python microbenchmark.py
   ```
5. Após a conclusão, o arquivo `resultados_windows.csv` será gerado.
6. Transfira este arquivo para a mesma pasta onde o CSV do Linux foi salvo. Desligue a VM do Windows.

### Etapa 3: Análise de Dados e Geração de Gráficos
1. Na máquina hospedeira (ou em qualquer máquina com as bibliotecas Pandas, Matplotlib e Seaborn instaladas), certifique-se de que os três arquivos estão no mesmo diretório:
   * `programa.py`
   * `resultados_linux.csv`
   * `resultados_windows.csv`
2. Execute o script de análise:
   ```bash
   python programa.py
   ```
3. O script irá:
   * Validar os dados (buscar por valores nulos ou negativos).
   * Exibir no console a tabela com as médias de tempo por operação e tamanho de bloco.
   * Gerar e salvar um painel com 4 gráficos no arquivo `comparativo_desempenho_SO.png`.

## Estrutura dos Arquivos
* `microbenchmark.py`: Script de coleta de dados utilizando a biblioteca `time` e operações de baixo nível (`bytearray`, `gc.collect()`).
* `programa.py`: Script de junção, validação, cálculo de estatísticas e plotagem gráfica dos resultados.
