import os
import re
from trie import TrieCompacta

class Indexador:
    """
    Responsável por percorrer o corpus, ler os textos e popular a Trie.
    """

    def __init__(self, caminho_corpus: str):
        self.caminho_corpus = caminho_corpus
        self.trie = TrieCompacta()
        self.doc_id = 0
        self.mapa_docs = {}  # {id: caminho_arquivo}

    # ---------------------------------------------------------------
    def construir_indice(self):
        """
        Percorre todas as pastas e arquivos de texto, inserindo termos na Trie.
        """
        for categoria in os.listdir(self.caminho_corpus):
            caminho_categoria = os.path.join(self.caminho_corpus, categoria)
            if not os.path.isdir(caminho_categoria):
                continue

            for arquivo in os.listdir(caminho_categoria):
                caminho_arquivo = os.path.join(caminho_categoria, arquivo)

                if not arquivo.endswith(".txt"):
                    continue

                self.doc_id += 1
                self.mapa_docs[self.doc_id] = caminho_arquivo

                print(f"Indexando {caminho_arquivo} (ID={self.doc_id})...")
                self._processar_documento(caminho_arquivo, self.doc_id)

        print("\n Indexação concluída!")

    # ---------------------------------------------------------------
    def _processar_documento(self, caminho_arquivo, doc_id):
        """
        Lê o texto e insere os termos na Trie.
        """
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            texto = f.read()

        # Normaliza o texto: minúsculas, remove pontuação, quebra em palavras
        palavras = re.findall(r"\b[a-zA-Záéíóúãõç]+\b", texto.lower())

        for termo in palavras:
            self.trie.insert(termo, doc_id)

    # ---------------------------------------------------------------
    def buscar(self, termo: str):
        """
        Retorna a lista de documentos em que o termo aparece.
        """
        termo = termo.lower()
        return self.trie.search(termo)

    # ---------------------------------------------------------------
    def mostrar_docs(self, ids):
        """
        Mostra os caminhos dos documentos a partir de seus IDs.
        """
        return [self.mapa_docs[i] for i in ids if i in self.mapa_docs]