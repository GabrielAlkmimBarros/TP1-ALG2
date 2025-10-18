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

            for arquivo in sorted(os.listdir(caminho_categoria), key=lambda x: int(x.split('.')[0])):
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
    
    def salvar_indice(self):
        """
        Salva o mapa_docs e a Trie em arquivos de texto.
        """
        # 1. Salvar o mapa_docs (Formato: ID,caminho_do_arquivo)
        with open(self.map_file, "w", encoding="utf-8") as f_map:
            for doc_id, caminho in self.mapa_docs.items():
                f_map.write(f"{doc_id},{caminho}\n")
        
        # 2. Salvar a Trie (Formato: palavra:doc1,freq1;doc2,freq2;...)
        with open(self.trie_file, "w", encoding="utf-8") as f_trie:
            # Pega todas as palavras e suas postings da Trie
            palavras_postings = self.trie.get_all_words_with_postings()
            
            for palavra, postings in palavras_postings.items():
                # Formata a lista de postagem: "doc1,freq1;doc2,freq2"
                postings_formatadas = []
                for doc_id, freq in postings.items():
                    postings_formatadas.append(f"{doc_id},{freq}")
                
                linha = f"{palavra}:{';'.join(postings_formatadas)}\n"
                f_trie.write(linha)

    # ---------------------------------------------------------------
    # --- NOVA FUNÇÃO: CARREGAR ÍNDICE ---
    # ---------------------------------------------------------------
    def carregar_indice(self):
        """
        Carrega o índice (mapa_docs e Trie) a partir dos arquivos.
        """
        # 1. Carregar o mapa_docs
        with open(self.map_file, "r", encoding="utf-8") as f_map:
            for linha in f_map:
                doc_id, caminho = linha.strip().split(',', 1)
                self.mapa_docs[int(doc_id)] = caminho
        
        # 2. Carregar a Trie
        with open(self.trie_file, "r", encoding="utf-8") as f_trie:
            for linha in f_trie:
                palavra, postings_str = linha.strip().split(':', 1)
                
                postings_list = postings_str.split(';')
                for posting in postings_list:
                    doc_id, freq = posting.split(',')
                    
                    # Re-insere a palavra na Trie.
                    # Como o insert apenas incrementa a frequência,
                    # precisamos chamá-lo 'freq' vezes.
                    for _ in range(int(freq)):
                        self.trie.insert(palavra, int(doc_id))