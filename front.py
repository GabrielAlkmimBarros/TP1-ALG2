from flask import Flask, render_template, request
import os
import re
from indexador import Indexador
from searchTree import RecuperacaoInformacao

app = Flask(__name__)

caminho_corpus = "bbc-fulltext/bbc"
arquivo_indice = "indice.txt"

indexador = Indexador(caminho_corpus, arquivo_indice)
busca = RecuperacaoInformacao(indexador)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    termo_buscado = request.form["query"]

    resultados_ids = busca.processar_consulta(termo_buscado)

    lista_resultados = []

    ids_ordenados = sorted(resultados_ids)
    for doc_id in ids_ordenados:
        # Pega o caminho do arquivo (ex: "bbc-fulltext/bbc/tech/001.txt")
        caminho_arquivo = indexador.mapa_docs.get(doc_id)
        if not caminho_arquivo:
            continue

        # Formata o "título" para ser o caminho relativo (ex: "tech/001.txt")
        titulo_bonito = os.path.basename(os.path.dirname(caminho_arquivo)) + "/" + os.path.basename(caminho_arquivo)

        # 4. Cria o dicionário que o seu HTML 'resultado.html' espera
        resultado_formatado = {
            'titulo': titulo_bonito,
            'link': '#', # Link placeholder
            'snippet': f"Encontrado no documento ID: {doc_id}" # Um "snippet" simples por agora
        }
        lista_resultados.append(resultado_formatado)
        
    # 5. Renderiza a página de resultados com os dados reais
    return render_template('resultado.html', 
                           query=termo_buscado, 
                           resultados=lista_resultados,
                           total_encontrado=len(lista_resultados))

    ######################################################

    # AQUI VAI SER COLOCADO A CHAMADA DO PROGRAMA COM O PARAMETRO TERMO

    ######################################################


if __name__ == "__main__":
    app.run(debug=True)

