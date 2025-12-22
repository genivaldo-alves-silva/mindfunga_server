import time
import datetime
import sys
import psutil # Módulo para verificar o uso de RAM (opcional, mas recomendado)
import os

# --- Configurações ---
# Objetivo: Alocar aproximadamente 4 GB de RAM.
# Um inteiro (int) em Python consome aproximadamente 28 bytes (em sistemas 64-bit).
# 4 GB = 4 * 1024 * 1024 * 1024 bytes = 4,294,967,296 bytes.
# Número de inteiros necessários: 4,294,967,296 / 28 ≈ 153,391,689
# Vamos arredondar para um valor ligeiramente maior para garantir a alocação.

NUM_ELEMENTOS = 320_000_000  # Total de elementos na lista (aproximadamente 4.5 GB)
DURACAO_HOLD_SEGUNDOS = 100 # O job manterá a RAM alocada por 5 minutos (300 segundos)

def job_de_alto_consumo():
    """
    Simula um job que aloca uma grande quantidade de RAM e a segura.
    """
    
    # 1. Verificação Inicial
    process = psutil.Process(os.getpid())
    mem_inicial = process.memory_info().rss / (1024 * 1024) # RAM em MB
    
    print(f"🚀 Job de Teste de RAM Iniciado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏳ Tempo de Alocação: {DURACAO_HOLD_SEGUNDOS} segundos (5 minutos)")
    print(f"📦 Tentando alocar {NUM_ELEMENTOS:,} elementos...")
    print(f"📊 Uso inicial de RAM: {mem_inicial:.2f} MB")
    
    # 2. Alocação de Memória
    print("\n--- INICIANDO ALOCAÇÃO DE RAM ---")
    
    try:
        # Cria uma lista onde cada elemento é um inteiro
        # O list comprehension forçará a alocação imediata de toda a memória.
        grande_lista = [i for i in range(NUM_ELEMENTOS)]
        
        # O Python só libera a memória quando a lista é destruída ou sai de escopo.
        
        mem_alocada = process.memory_info().rss / (1024 * 1024)
        mem_alocada_gb = mem_alocada / 1024
        
        print(f"🎉 Alocação Concluída com Sucesso!")
        print(f"📊 Uso total de RAM após alocação: {mem_alocada:.2f} MB ({mem_alocada_gb:.2f} GB)")
        print("-----------------------------------")
        
        # 3. Segurar a Memória (Mantendo o Job Ativo)
        print(f"\n✋ Segurando a RAM por {DURACAO_HOLD_SEGUNDOS} segundos...")
        tempo_decorrido = 0
        
        # Loop para manter o job ativo por 5 minutos, mas com baixo consumo de CPU
        while tempo_decorrido < DURACAO_HOLD_SEGUNDOS:
            tempo_de_dormir = min(30, DURACAO_HOLD_SEGUNDOS - tempo_decorrido) # Log a cada 30s
            time.sleep(tempo_de_dormir) 
            tempo_decorrido += tempo_de_dormir
            
            porcentagem = (tempo_decorrido / DURACAO_HOLD_SEGUNDOS) * 100
            print(f"⏱️ Progresso: {tempo_decorrido}s de {DURACAO_HOLD_SEGUNDOS}s ({porcentagem:.0f}%) | RAM: {process.memory_info().rss / (1024 * 1024):.2f} MB")

    except MemoryError:
        print("\n❌ ERRO: O sistema não conseguiu alocar a memória solicitada. O job será encerrado.")
        # Se ocorrer um MemoryError, a lista pode não ter sido totalmente criada.
        
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")
        
    finally:
        # A lista só será liberada quando a função terminar.
        print(f"\n✅ Job de Teste Concluído em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        mem_final = process.memory_info().rss / (1024 * 1024)
        print(f"📊 Uso de RAM no encerramento do script: {mem_final:.2f} MB")

if __name__ == "__main__":
    try:
        if 'psutil' not in sys.modules:
             print("⚠️ O módulo 'psutil' não está importado. Por favor, instale-o para monitorar o uso de RAM.")
             print("Execute: pip install psutil")
             sys.exit(1)
             
        job_de_alto_consumo()
        
    except ImportError:
        print("⚠️ O módulo 'psutil' é necessário para este script de alto consumo de RAM. Por favor, instale-o (pip install psutil).")
        sys.exit(1)
