from indexador import Indexador
from searchTree import RecuperacaoInformacao 



def main():
    caminho_corpus = "bbc-fulltext/bbc"   # ajuste para o seu diretório real
    arquivo_indice = "indice.txt"

    # Cria ou carrega o índice
    indexador = Indexador(caminho_corpus, arquivo_indice)

    # Inicializa o módulo de recuperação
    busca = RecuperacaoInformacao(indexador)

    print("\nÍndice pronto para consultas booleanas!")

    while True:
        consulta = input("Consulta: ").strip()
        if consulta.lower() == "sair":
            print("\nSalvando índice e encerrando...")
            indexador.salvar_indice()
            print("Índice salvo. Até mais!")
            break

        if not consulta:
            continue

        try:
            busca.mostrar_resultados(consulta)
        except Exception as e:
            print(f"\nErro ao processar consulta: {e}\n")


if __name__ == "__main__":
    main()


