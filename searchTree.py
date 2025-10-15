import re

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
        """
        Constrói a árvore de consulta e avalia o resultado.
        """
        tokens = re.findall(r'\(|\)|AND|OR|[A-Za-zÀ-ÿ0-9_-]+', consulta)
        tokens = [t.strip() for t in tokens if t.strip()]

        arvore = self._construir_arvore(tokens)
        resultado = self._avaliar_arvore(arvore)
        return resultado

    
    def _construir_arvore(self, tokens):

        def precedencia(op):
            return 2 if op == "AND" else 1 if op == "OR" else 0

        valores = []     # nós
        operadores = []  # strings

        def aplicar_operador():
            
            if len(valores) < 2 or not operadores:
                return
            op = operadores.pop()
            direita = valores.pop()
            esquerda = valores.pop()
            valores.append(NoConsulta(op, esquerda, direita))

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

    
    def mostrar_resultados(self, consulta: str):

        resultados = self.processar_consulta(consulta)
        if not resultados:
            print("\nNenhum documento encontrado.")
            return

        print(f"\nConsulta: {consulta}")
        print(f"Documentos encontrados ({len(resultados)}):")
        for doc_id in sorted(resultados):
            print(f" - {self.indexador.mapa_docs[doc_id]}")
