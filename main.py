import os  # <-- PASSO 1: Adicione esta importação
from indexador import Indexador
from searchTree import RecuperacaoInformacao 



def main():
    caminho_corpus = "bbc-fulltext/bbc"   
    arquivo_indice = "indice.txt"



    indexador = Indexador(caminho_corpus, arquivo_indice)

 
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
