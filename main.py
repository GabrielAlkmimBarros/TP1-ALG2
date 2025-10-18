import os  # <-- PASSO 1: Adicione esta importação
from indexador import Indexador
from searchTree import RecuperacaoInformacao 

if __name__ == "__main__":
    corpus_path = "bbc-fulltext/bbc"
    

    indexador = Indexador(corpus_path)
    #print("\nConstruindo índice...") <-- Não precisamos mais disso
    indexador.construir_indice() # <-- Isso agora vai carregar ou construir

    # Cria o módulo de busca 
    busca = RecuperacaoInformacao(indexador)

    # Loop interativo
    while True:
        consulta = input("\nDigite sua consulta (ou 'sair'): ")
        if consulta.lower() == "sair":
            break

        # Avalia a consulta usando a árvore 
        docs = busca.processar_consulta(consulta)

        if not docs:
            print("Nenhum documento encontrado.")
        else:
            # Converte IDs em caminhos de arquivo
            caminhos = [indexador.mapa_docs[i] for i in docs]
            
            # --- PASSO 2: A LINHA CORRIGIDA ---
            # Usa os.path.basename(x) para pegar '135.txt' de forma segura
            caminhos = sorted(caminhos, key=lambda x: int(os.path.basename(x).split('.')[0]))

            print(f"\nConsulta: {consulta}")
            print(f"Documentos encontrados ({len(caminhos)}):")
            for caminho in caminhos:
                print(" -", caminho)