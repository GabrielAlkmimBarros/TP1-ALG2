from indexador import Indexador
from searchTree import RecuperacaoInformacao 

if __name__ == "__main__":
    corpus_path = "bbc-fulltext/bbc"
    

    indexador = Indexador(corpus_path)
    print("\nConstruindo índice...")
    indexador.construir_indice()

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
            caminhos = sorted(caminhos, key=lambda x: int(x.split('/')[-1].split('.')[0]))

            print(f"\nConsulta: {consulta}")
            print(f"Documentos encontrados ({len(caminhos)}):")
            for caminho in caminhos:
                print(" -", caminho)
