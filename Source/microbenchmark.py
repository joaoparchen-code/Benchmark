import time
import csv
import gc

def executar_microbenchmark(nome_arquivo="resultados_microbenchmark.csv"):
    # Requisitos fixos: blocos de 100 a 1000 MB, incremento de 100 MB, 100 repetições
    tamanhos_mb = range(100, 1001, 100)
    repeticoes = 100
    
    # Cabeçalho exigido pelo protocolo
    cabecalho = ['bloco_MB', 'teste', 'alloc_ms', 'write_ms', 'read_ms', 'free_ms']

    with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(cabecalho)

        for bloco in tamanhos_mb:
            tamanho_bytes = bloco * 1024 * 1024
            print(f"Testando bloco de {bloco} MB...")
            
            for teste in range(1, repeticoes + 1):
                # 1. Alocação
                inicio_alloc = time.perf_counter()
                bloco_memoria = bytearray(tamanho_bytes)
                fim_alloc = time.perf_counter()

                # 2. Escrita
                inicio_escrita = time.perf_counter()
                # Escrita em pedaços para evitar picos que mascarem o benchmark de SO
                tamanho_chunk = 1024 * 1024
                for i in range(0, tamanho_bytes, tamanho_chunk):
                     bloco_memoria[i:i+tamanho_chunk] = b'\xAA' * tamanho_chunk
                fim_escrita = time.perf_counter()

                # 3. Leitura
                inicio_leitura = time.perf_counter()
                # Acessando fatias para forçar a leitura real pela CPU
                _ = bloco_memoria[::1024]
                fim_leitura = time.perf_counter()

                # 4. Liberação
                inicio_liberacao = time.perf_counter()
                del bloco_memoria
                gc.collect() # Força o Garbage Collector para garantir a liberação
                fim_liberacao = time.perf_counter()

                # Conversão para milissegundos
                alloc_ms = (fim_alloc - inicio_alloc) * 1000
                write_ms = (fim_escrita - inicio_escrita) * 1000
                read_ms = (fim_leitura - inicio_leitura) * 1000
                free_ms = (fim_liberacao - inicio_liberacao) * 1000

                # Gravando registro no CSV
                writer.writerow([bloco, teste, alloc_ms, write_ms, read_ms, free_ms])

    print(f"Execução concluída! Arquivo salvo como: {nome_arquivo}")

if __name__ == "__main__":
    # Altere o nome do arquivo dependendo do SO testado
    # Ex: "resultados_windows.csv" ou "resultados_linux.csv"
    executar_microbenchmark("resultados_microbenchmark.csv")
