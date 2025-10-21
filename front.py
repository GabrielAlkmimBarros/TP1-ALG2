from flask import Flask, render_template, request
import os
import re
import math # Importe a biblioteca math
from indexador import Indexador
from searchTree import RecuperacaoInformacao

app = Flask(__name__)

caminho_corpus = "bbc-fulltext/bbc"
arquivo_indice = "indice.txt"

indexador = Indexador(caminho_corpus, arquivo_indice)
busca = RecuperacaoInformacao(indexador)

#função para gerar os snippets na exibição dos resultados
def gerar_snippet(caminho_arquivo: str, termos_consulta: list) -> str:
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

        #considera o texto excluindo o titulo (primeira linha)
        corpo_texto = '\n'.join(conteudo.split('\n')[1:]).strip()
        corpo_texto_lower = corpo_texto.lower()

        #encontra a primeira ocorrência do termo da consulta no corpo do texto
        melhor_posicao= -1
        termo_original= ""
        for termo in termos_consulta:
            match = re.search(r'\b' + re.escape(termo.lower()) + r'\b', corpo_texto_lower) #\b para garantir que é uma palavra inteira
            if match:
                melhor_posicao = match.start()
                termo_original = corpo_texto[melhor_posicao:match.end()]
                break

        if melhor_posicao != -1:
            TAMANHO_TRECHO_SNIPPET = 80
            tamanho_termo = len(termo_original)

            inicio_snippet = max(0, melhor_posicao - TAMANHO_TRECHO_SNIPPET)
            fim_snippet = min(len(corpo_texto), melhor_posicao + tamanho_termo + TAMANHO_TRECHO_SNIPPET)

            snippet = corpo_texto[inicio_snippet:fim_snippet]

            termo_destacado = f"<b>{termo_original}</b>"

            snippet_final = re.sub(re.escape(termo_original), termo_destacado, snippet, 1)

            #adiciona '...' se o texto foi truncado
            if inicio_snippet > 0:
                snippet_final = "..." + snippet_final
            if fim_snippet < len(corpo_texto):
                snippet_final = snippet_final + "..."
            
            return snippet_final.strip()
        
        else:
        # a palavra não for encontrada no corpo
            return corpo_texto[:160].strip() + "..."
            

                


    

@app.route("/")
def homepage():
    return render_template("index.html")

# Aceita GET (para paginação) e POST (para busca nova)
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    
    if request.method == "POST":
        # Se é uma nova busca (do formulário), vá para a página 1
        termo_buscado = request.form["query"]
        page = 1
    else: # request.method == "GET"
        # Se é um clique na paginação, pegue os parâmetros da URL
        termo_buscado = request.args.get("query", "")
        page = request.args.get("page", 1, type=int)


    termos_consulta = [t.lower() for t in re.findall(r'\(|\)|AND|OR|[A-Za-zÀ-ÿ0-9_-]+', termo_buscado) if t.lower() not in ("and", "or", "(", ")")]
    termos_consulta = list(set(termos_consulta)) # Remove duplicatas

    resultados_ranqueados = busca.processar_consulta(termo_buscado)

    RESULTADOS_POR_PAGINA = 10
    total_resultados = len(resultados_ranqueados)
    
    # Garante que a página não seja menor que 1
    if page < 1:
        page = 1
        
    # Calcula total de páginas (ex: 105 resultados / 10 por pág = 10.5, arredonda para 11)
    total_paginas = math.ceil(total_resultados / RESULTADOS_POR_PAGINA)

    # Calcula o índice de início e fim para fatiar a lista
    inicio_slice = (page - 1) * RESULTADOS_POR_PAGINA
    fim_slice = inicio_slice + RESULTADOS_POR_PAGINA

    #pega os resultados da página atual
    resultados_para_pagina = resultados_ranqueados[inicio_slice:fim_slice]


    lista_resultados = []

    # itera sobre os 10 da página atual
    for doc_id, score in resultados_para_pagina:
        # Pega o caminho do arquivo (ex: "bbc-fulltext/bbc/tech/001.txt")
        caminho_arquivo = indexador.mapa_docs.get(doc_id)
        if not caminho_arquivo:
            continue

        #lê o conteúdo do arquivo
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            titulo = f.readline().strip()

            if not titulo:
                titulo = "Sem Título"

        # Formata o "título" para ser o caminho relativo (ex: "tech/001.txt")
        titulo_bonito = titulo

        snippet_final = gerar_snippet(caminho_arquivo, termos_consulta)

        # Cria o dicionário que o seu HTML 'resultado.html' espera
        resultado_formatado = {
            'titulo': titulo_bonito,
            'link': '#', # Link placeholder
            'snippet': snippet_final,
            'score': f"{score:.3f}"
        }
        
        lista_resultados.append(resultado_formatado)

    # renderiza a página de resultados com os dados reais
    return render_template('resultado.html',
                           query=termo_buscado,
                           resultados=lista_resultados, # A lista agora está paginada
                           total_encontrado=total_resultados, # O número total de resultados
                           page=page, # A página atual
                           total_paginas=total_paginas # O número total de páginas
                           )


if __name__ == "__main__":
    app.run(debug=True)