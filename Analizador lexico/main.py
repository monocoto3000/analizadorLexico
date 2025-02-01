import re

TOKENS = [
    ("PALABRA_RESERVADA", r"\b(fun|Begin|End|float|int|number|in|out|if|else|return|var|call)\b"),
    ("NUMERO_FLOAT", r"\b\d+\.\d+\b"),
    ("NUMERO_ENTERO", r"\b\d+\b"),
    ("OPERADOR_LOGICO", r"(==|!=|<|>)"),
    ("OPERADOR", r"[+\-*/=]"),
    ("DELIMITADOR", r"[(){}]") ,
    ("CADENA", r'".*?"'),
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
    identificadores_declarados = set()

    if tokens[0][1] != "Begin":
        errores.append("Error: El código debe de iniciar con'Begin'")
    if tokens[-1][1] != "End":
        errores.append("Error: El código debe de terminar con 'End'")

    for i in range(1, len(tokens)):
        tipo, lexema, pos = tokens[i]

        if tipo == "PALABRA_RESERVADA":

            if lexema in ["float", "int", "number", "return", "var", "call", "fun"]:
                if i + 1 >= len(tokens) or tokens[i + 1][0] != "IDENTIFICADOR":
                    errores.append(f"Error en posición {pos}: Se esperaba un identificador después de '{lexema}'")
                else:
                    identificadores_declarados.add(tokens[i + 1][1])

            if lexema in ["fun", "var"]:
                if i + 1 >= len(tokens) or tokens[i + 1][0] != "IDENTIFICADOR":
                    errores.append(f"Error en posición {pos}: Se esperaba un identificador después de '{lexema}'")
            if lexema == "call":
                if i + 1 >= len(tokens) or tokens[i + 1][0] != "IDENTIFICADOR":
                    errores.append(f"Error en posición {pos}: Se esperaba un identificador después de 'call'")
            if lexema in ["in", "out"]:
                if i + 1 >= len(tokens) or tokens[i + 1][0] != "DELIMITADOR":
                    errores.append(f"Error en posición {pos}: Se esperaba un delimitador después de '{lexema}'")
            if lexema in ["if", "else"]:
                if i + 1 >= len(tokens) or tokens[i + 1][0] != "DELIMITADOR":
                    errores.append(f"Error en posición {pos}: Se esperaba un delimitador después de '{lexema}'")

        if tipo == "OPERADOR":
            if i + 1 >= len(tokens) or tokens[i + 1][0] not in ["NUMERO_FLOAT", "NUMERO_ENTERO", "IDENTIFICADOR", "CADENA"]:
                errores.append(f"Error en posición {pos}: Se esperaba un número, identificador o cadena después del operador '{lexema}'")

        if tipo == "IDENTIFICADOR":
            if lexema not in identificadores_declarados:
                tipo_anterior, _ , _ = tokens[i - 1] if i > 0 else (None, None, None)
                if tipo_anterior not in ["PALABRA_RESERVADA", "OPERADOR"]:
                    errores.append(f"Error en posición {pos}: '{lexema}' indefinido")

        if tipo == "DELIMITADOR":
            delimitadores += 1

    if delimitadores % 2 != 0:
        errores.append("Error: Faltan cierres o aperturas de delimitadores")

    return errores

codigo_fuente = """
Begin
fun app {
    var x = 10
    var string = "Hola mundo"
    if (x > 5) {
        x = x + 1 
        return x
    }
    out(x)
    # Comentario
}
call app
End
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
