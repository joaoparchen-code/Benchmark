import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_resultados(csv_windows, csv_linux):
    # 1. Carregamento dos arquivos
    try:
        df_win = pd.read_csv(csv_windows)
        df_win['sistema'] = 'Windows'
        
        df_lin = pd.read_csv(csv_linux)
        df_lin['sistema'] = 'Linux'
    except FileNotFoundError as e:
        print(f"Erro: Certifique-se de que os arquivos CSV existem. {e}")
        return

    # 2. Junção e manipulação dos dados
    df_completo = pd.concat([df_win, df_lin], ignore_index=True)
    colunas_tempo = ['alloc_ms', 'write_ms', 'read_ms', 'free_ms']

    # Regras de validação básicas do protocolo: verificar valores negativos e nulos
    if (df_completo[colunas_tempo] < 0).any().any() or df_completo.isnull().values.any():
        print("Aviso: Existem valores nulos ou tempos negativos. Validação falhou!")

    # 3. Criação de Tabelas (Agrupamento)
    # Agrupando por Sistema e Tamanho do Bloco e calculando a média
    df_media = df_completo.groupby(['sistema', 'bloco_MB'])[colunas_tempo].mean().reset_index()
    
    print("\n--- Média de Tempo das Operações por Sistema Operacional (ms) ---")
    print(df_media)

    # 4. Geração de Gráficos Comparativos
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparação de Desempenho: Windows vs Linux\n(Tempos em Milissegundos)', fontsize=16)

    operacoes = [
        ('alloc_ms', 'Alocação de Memória', axes[0, 0]),
        ('write_ms', 'Escrita em Memória', axes[0, 1]),
        ('read_ms', 'Leitura de Memória', axes[1, 0]),
        ('free_ms', 'Liberação de Memória', axes[1, 1])
    ]

    for coluna, titulo, ax in operacoes:
        sns.lineplot(
            data=df_completo, 
            x='bloco_MB', 
            y=coluna, 
            hue='sistema', 
            marker='o', 
            errorbar=None, # Define se deseja exibir o intervalo de confiança
            ax=ax
        )
        ax.set_title(titulo)
        ax.set_xlabel('Tamanho do Bloco (MB)')
        ax.set_ylabel('Tempo (ms)')

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig('comparativo_desempenho_SO.png', dpi=300)
    print("\nGráfico comparativo salvo como 'comparativo_desempenho_SO.png'")
    plt.show()

if __name__ == "__main__":
    # Substitua pelos nomes exatos dos arquivos CSV gerados na primeira etapa
    analisar_resultados('resultados_windows.csv', 'resultados_linux.csv')
