# Implementação da estrutura de Trie compacta

class TrieNode:
    def __init__(self):
        self.children = {}      # {string_da_aresta: TrieNode}
        self.postings = []      # Estrutura: [(doc_id, frequencia), (doc_id, frequencia), ...]
        self.is_end = False     # Flag para indicar se o caminho até aqui forma um termo completo





class TrieCompacta:
    def __init__(self):
            self.root = TrieNode()

    def insert(self, word: str, doc_id: int):
        # Insere uma palavra associando-a a um documento.
        node = self.root
        current = word

        while True:
            for edge, child in node.children.items():
                # Encontra o maior prefixo comum entre current e edge
                prefix_len = self._common_prefix_length(current, edge)
                if prefix_len == 0:
                    continue

                # Caso 1: o prefixo é igual ao edge completo -> desce
                if prefix_len == len(edge):
                    current = current[prefix_len:]
                    node = child
                    break

                # Caso 2: o prefixo é parcial -> precisa dividir (split)
                else:
                    self._split_edge(node, edge, prefix_len)
                    # Após dividir, desce para o nó correspondente ao prefixo
                    node = node.children[edge[:prefix_len]]
                    current = current[prefix_len:]
                    break
            else:
                # Caso 3: não há prefixo comum -> adiciona nova aresta
                new_node = TrieNode()
                new_node.is_end = True
                new_node.docs.add(doc_id)
                node.children[current] = new_node
                return

            # Se já consumimos toda a palavra, marca fim de palavra
            if current == "":
                node.is_end = True
                node.docs.add(doc_id)
                return

    def search(self, word: str):
        """
        Busca uma palavra e retorna o conjunto de documentos associados.
        Retorna set() se a palavra não estiver no índice.
        """
        node = self.root
        current = word

        while current:
            found = False
            for edge, child in node.children.items():
                if current.startswith(edge):
                    current = current[len(edge):]
                    node = child
                    found = True
                    break
                elif edge.startswith(current):  # palavra termina no meio da aresta
                    return set()
            if not found:
                return set()  # não encontrou prefixo compatível

        # Se chegamos ao fim da palavra, verifica se é final de termo
        return node.docs if node.is_end else set()
    
    def _common_prefix_length(self, a: str, b: str) -> int:
        """
        Retorna o comprimento do maior prefixo comum entre a e b.
        Exemplo: a="carta", b="carro" -> retorna 3
        """
        min_len = min(len(a), len(b))
        for i in range(min_len):
            if a[i] != b[i]:
                return i
        return min_len
    


    def _split_edge(self, node, edge, prefix_len):
        """
        Divide uma aresta (edge) em duas, quando um novo termo
        compartilha apenas parte dela.

        """
        prefix = edge[:prefix_len]
        suffix = edge[prefix_len:]

        # Nó antigo que era o filho do edge original
        old_child = node.children.pop(edge)

        # Novo nó que representará o prefixo comum
        new_child = TrieNode()

        # O sufixo vira a nova aresta do novo nó
        new_child.children[suffix] = old_child

        # Substitui na árvore
        node.children[prefix] = new_child


    def print_trie(self, node=None, prefix=""):
        """
        Função auxiliar para depuração  
        """
        if node is None:
            node = self.root

        for edge, child in node.children.items():
            word = prefix + edge
            print(f"{word}  (end={child.is_end}, docs={child.docs})")
            self.print_trie(child, word)

        
    def get_all_words_with_postings(self) -> dict:
        """
        Retorna um dicionário de todos os termos na Trie com suas listas de postagem.
        Útil para calcular estatísticas globais.
        """
        words = {}
        self._get_all_words_recursive(self.root, "", words)
        return words




