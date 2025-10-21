import re
import math
from collections import defaultdict

# Implementação de uma AVL tree para processar a consulta

class NoConsulta:
    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor          # termo ou operador ('AND', 'OR')
        self.esquerda = esquerda    # filho esquerdo (NoConsulta)
        self.direita = direita      # filho direito (NoConsulta)



class RecuperacaoInformacao:


    def __init__(self, indexador):
        self.indexador = indexador
        self.trie = indexador.trie

    
    def processar_consulta(self, consulta: str):

        tokens = re.findall(r'\(|\)|AND|OR|[A-Za-zÀ-ÿ0-9_-]+', consulta)
        tokens = [t.strip() for t in tokens if t.strip()]

        arvore = self._construir_arvore(tokens)
        resultado = self._avaliar_arvore(arvore)

        ranking = self.ranquear_documentos(consulta)
        ranking_filtrado = [r for r in ranking if r[0] in resultado]

        return ranking_filtrado




    
    def _construir_arvore(self, tokens):

        def precedencia(op):
            return 2 if op == "AND" else 1 if op == "OR" else 0

        valores = []     # nós
        operadores = []  # strings

        def aplicar_operador():
            
            if not operadores:
                raise ValueError("Erro, faltou operador")
            op = operadores.pop()
            if len(valores) < 2 :
                return
            
            direita = valores.pop()
            esquerda = valores.pop()
            valores.append(NoConsulta(op, esquerda, direita))

        if tokens[0] in ("AND", "OR") or tokens[-1] in ("AND", "OR"):
            print("Pesquisa inválida")
            return None
        
        for token in tokens:
            if token == '(':
                operadores.append(token)

            elif token == ')':
                while operadores and operadores[-1] != '(':
                    aplicar_operador()
                operadores.pop()  # remove '('

            elif token in ("AND", "OR"):
                while (operadores and precedencia(operadores[-1]) >= precedencia(token)):
                    aplicar_operador()
                operadores.append(token)

            else:
                # termo
                if valores and (not operadores or operadores[-1] not in ("AND", "OR", "(")):
                    operadores.append("OR")
                valores.append(NoConsulta(token.lower()))

        while operadores:
            aplicar_operador()

        return valores[-1] if valores else None

    
    def _avaliar_arvore(self, no):

        if no is None:
            return set()

        # Nó folha -> termo
        if no.valor not in ("AND", "OR"):
            return self.trie.search(no.valor)

        # Nó interno -> operador lógico
        esquerda = self._avaliar_arvore(no.esquerda)
        direita = self._avaliar_arvore(no.direita)

        if no.valor == "AND":
            return esquerda & direita
        else:  # "OR"
            return esquerda | direita

    def contar_nos(self, no):

        if no is None:
            return 0
        return 1 + self.contar_nos(no.esquerda) + self.contar_nos(no.direita)



    def mostrar_resultados(self, consulta: str):
        resultados = self.processar_consulta(consulta)
        if not resultados:
            print("\nNenhum documento encontrado.")
            return

        print(f"\nConsulta: {consulta}")
        print(f"Documentos encontrados ({len(resultados)}):\n")

        for doc_id, score in resultados:
            caminho = self.indexador.mapa_docs.get(doc_id, "Documento não encontrado")
            print(f" - {caminho}  (relevância = {score:.3f})")


    def ranquear_documentos(self, consulta: str):

        termos = re.findall(r"[A-Za-zÀ-ÿ0-9_-]+", consulta.lower())
        if not termos:
            return []


        scores_por_doc = defaultdict(list)

        for termo in termos:
            node = self._buscar_no_trie(termo)
            if not node or not node.is_end:
                continue

            postings = node.postings  # {doc_id: freq}

            freqs = list(postings.values())
            media = sum(freqs) / len(freqs)
            variancia = sum((f - media)**2 for f in freqs) / len(freqs)
            desvio = math.sqrt(variancia) if variancia > 0 else 1  # evita divisão por zero

            # z-score 
            for doc_id, f in postings.items():
                z = (f - media) / desvio
                scores_por_doc[doc_id].append(z)

        # Média dos z-scores 
        relevancia = {}
        for doc_id, zs in scores_por_doc.items():
            relevancia[doc_id] = sum(zs) / len(termos)

        # Ordena em ordem decrescente de relevância
        docs_ordenados = sorted(relevancia.items(), key=lambda x: x[1], reverse=True)

        return docs_ordenados


    def _buscar_no_trie(self, termo: str):
        """
        Navega na trie para retornar o nó final correspondente ao termo.
        """
        node = self.trie.root
        current = termo
        while current:
            found = False
            for edge, child in node.children.items():
                if current.startswith(edge):
                    current = current[len(edge):]
                    node = child
                    found = True
                    break
            if not found:
                return None
        return node
