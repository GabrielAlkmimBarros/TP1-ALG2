import os
import re
from trie import TrieCompacta


class Indexador:


    def __init__(self, caminho_corpus: str, arquivo_indice: str = "indice.txt"):
        self.caminho_corpus = caminho_corpus
        self.trie = TrieCompacta()
        self.doc_id = 0
        self.mapa_docs = {}  # {id: caminho_arquivo}
        self.arquivo_indice = arquivo_indice

        # Se já existir índice salvo, carrega; caso contrário, constrói e salva
        if os.path.exists(arquivo_indice):
            print(f"Carregando índice existente de '{arquivo_indice}'...\n")
            self.carregar_indice(arquivo_indice)
        else:
            print("Nenhum índice encontrado. Construindo novo índice...\n")
            self.construir_indice()
            self.salvar_indice(arquivo_indice)


    def construir_indice(self):
        """
        Percorre todas as pastas e arquivos do corpus, indexando termos na Trie.
        """
        for categoria in os.listdir(self.caminho_corpus):
            caminho_categoria = os.path.join(self.caminho_corpus, categoria)
            if not os.path.isdir(caminho_categoria):
                continue

            for arquivo in sorted(os.listdir(caminho_categoria), key=lambda x: int(x.split('.')[0])):
                caminho_arquivo = os.path.join(caminho_categoria, arquivo)

                if not arquivo.endswith(".txt"):
                    continue

                self.doc_id += 1
                self.mapa_docs[self.doc_id] = caminho_arquivo

                print(f"Indexando {caminho_arquivo} (ID={self.doc_id})...")
                self._processar_documento(caminho_arquivo, self.doc_id)

        print("\nIndexação concluída com sucesso!")


    def _processar_documento(self, caminho_arquivo, doc_id):
        """
        Lê o conteúdo do arquivo, normaliza o texto e insere termos na Trie.
        """
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            texto = f.read()

        # Normaliza: letras minúsculas, remove pontuação, divide em palavras
        palavras = re.findall(r"\b[a-zA-Záéíóúãõç]+\b", texto.lower())

        for termo in palavras:
            self.trie.insert(termo, doc_id)


    def buscar(self, termo: str):
        """
        Retorna o conjunto de IDs de documentos em que o termo aparece.
        """
        termo = termo.lower()
        return self.trie.search(termo)


    def mostrar_docs(self, ids):
        """
        Mostra os caminhos dos documentos a partir de seus IDs.
        """
        return [self.mapa_docs[i] for i in ids if i in self.mapa_docs]


    def salvar_indice(self, caminho_arquivo: str = None):
        """
        Salva o índice (mapa de documentos + postings da Trie) em arquivo texto.
        Formato:
            # MAPA_DOCS
            id|caminho
            ...
            # TRIE
            termo|doc_id:freq,doc_id:freq,...
        """
        if caminho_arquivo is None:
            caminho_arquivo = self.arquivo_indice

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            # MAPA DE DOCUMENTOS
            f.write("# MAPA_DOCS\n")
            for doc_id, caminho in self.mapa_docs.items():
                f.write(f"{doc_id}|{caminho}\n")

            # TRIE COM POSTINGS
            f.write("\n# TRIE\n")
            palavras = self.trie.get_all_words_with_postings()
            for termo, postings in palavras.items():
                pares = [f"{doc}:{freq}" for doc, freq in postings.items()]
                f.write(f"{termo}|{','.join(pares)}\n")

        print(f"\nÍndice salvo em '{caminho_arquivo}' com sucesso.")


    def carregar_indice(self, caminho_arquivo: str = None):
        """
        Carrega um índice salvo em disco e reconstrói a Trie e o mapa de documentos.
        """
        if caminho_arquivo is None:
            caminho_arquivo = self.arquivo_indice

        if not os.path.exists(caminho_arquivo):
            print("Arquivo de índice não encontrado. Será criado um novo.")
            return

        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            secao = None
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                # Detecta seções
                if linha.startswith("#"):
                    if "MAPA_DOCS" in linha:
                        secao = "MAPA_DOCS"
                    elif "TRIE" in linha:
                        secao = "TRIE"
                    continue

                # Mapa de documentos
                if secao == "MAPA_DOCS":
                    doc_id, caminho = linha.split("|", 1)
                    self.mapa_docs[int(doc_id)] = caminho

                # Trie + postings
                elif secao == "TRIE":
                    termo, dados = linha.split("|", 1)
                    pares = dados.split(",")
                    for par in pares:
                        doc, freq = par.split(":")
                        doc, freq = int(doc), int(freq)
                        for _ in range(freq):
                            self.trie.insert(termo, doc)


        if self.mapa_docs:
            self.doc_id = max(self.mapa_docs.keys())

        print(f"Índice carregado de '{caminho_arquivo}' com sucesso.\n")
