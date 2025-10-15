from indexador import Indexador

if __name__ == "__main__":
    corpus_path = "bbc-fulltext/bbc"
    indexador = Indexador(corpus_path)

    # 1. Construir índice
    indexador.construir_indice()

    # 2. Buscar um termo
    termo = input("\nDigite um termo para buscar: ")
    docs = indexador.buscar(termo)

    if not docs:
        print("Nenhum documento encontrado.")
    else:
        print(f"Termo '{termo}' encontrado nos documentos:")
        for doc in indexador.mostrar_docs(docs):
            print(" -", doc)