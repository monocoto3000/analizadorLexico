import re

TOKENS = [
    ("PALABRA_RESERVADA", r"\b(fun|Begin|End|float|int|number|in|out|if|else|return|var|call)\b"),
    ("NUMERO_FLOAT", r"\b\d+\.\d+\b"),
    ("NUMERO_ENTERO", r"\b\d+\b"),
    ("OPERADOR_LOGICO", r"(==|!=|<|>)"),
    ("OPERADOR", r"[+\-*/=]"),
    ("DELIMITADOR", r"[(){}]"),
    ("LITERAL_CADENA", r'".*?"'),
    ("COMENTARIO", r"\#.*"),
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("ESPACIO", r"[ \t\n]+")
]

def analizador_lexico(codigo_fuente):
    tokens = []
    pos = 0
    while pos < len(codigo_fuente):
        match = None
        for token_tipo, patron in TOKENS:
            regex = re.compile(patron)
            match = regex.match(codigo_fuente, pos)
            if match:
                lexema = match.group(0)
                if token_tipo != "ESPACIO":  
                    tokens.append((token_tipo, lexema, pos))
                pos = match.end()
                break
        if not match:
            raise ValueError(f"Error léxico: carácter inesperado en posición {pos} ('{codigo_fuente[pos]}')")
    return tokens

def verificar_tokens(tokens):
    errores = []
    delimitadores = 0

    for i in range(len(tokens)):
        tipo, lexema, pos = tokens[i]

        # Después de 'fun' o 'var' debe haber un 'IDENTIFICADOR'
        if tipo == "PALABRA_RESERVADA" and lexema in ["fun", "var"]:
            if i + 1 >= len(tokens) or tokens[i + 1][0] != "IDENTIFICADOR":
                errores.append(f"Error en posición {pos}: Se esperaba un IDENTIFICADOR después de '{lexema}'")

        # Después de un 'OPERADOR' debe haber un 'NUMERO_FLOAT' o 'NUMERO_ENTERO' o 'IDENTIFICADOR'
        if tipo == "OPERADOR":
            if i + 1 >= len(tokens) or tokens[i + 1][0] not in ["NUMERO_FLOAT", "NUMERO_ENTERO", "IDENTIFICADOR"]:
                errores.append(f"Error en posición {pos}: Se esperaba un número o identificador después del operador '{lexema}'")

        # Contador de Delimitadores 
        if tipo == "DELIMITADOR":
            delimitadores += 1

    # La cantidad de delimitadores debe ser par
    if delimitadores % 2 != 0:
        errores.append("Error: La cantidad de delimitadores no es par (faltan cierres o aperturas)")

    return errores

codigo_fuente = """
fun ejemplillo {
    var x = 10
    if (x > 5) {
        x = x + 1 
    }
    # Comentario
}
"""

try:
    tokens = analizador_lexico(codigo_fuente)
    errores = verificar_tokens(tokens)

    print("Tokens generados:")
    for token in tokens:
        print(token)

    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(error)
    else:
        print("\nNo se encontraron errores")

except ValueError as e:
    print(e)