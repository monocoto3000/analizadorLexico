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
    delimitadores_stack = []
    identificadores_definidos = set() 

    if tokens[0][1] != "Begin":
        errores.append("Error: El código debe iniciar con 'Begin'")
    if tokens[-1][1] != "End":
        errores.append("Error: El código debe terminar con 'End'")

    i = 0
    while i < len(tokens):
        tipo, lexema, pos = tokens[i]

        if tipo == "OPERADOR" or tipo == "OPERADOR_LOGICO":
            if i == len(tokens) - 1 or tokens[i+1][0] not in ["IDENTIFICADOR", "NUMERO_FLOAT", "NUMERO_ENTERO", "CADENA", "DELIMITADOR"]:
                errores.append(f"Error en posición {pos}: Operador '{lexema}' sin valor después del operador")
        
        if tipo == "OPERADOR_LOGICO":
            if i == 0 or tokens[i-1][0] not in ["IDENTIFICADOR", "NUMERO_FLOAT", "NUMERO_ENTERO"]:
                errores.append(f"Error en posición {pos}: Operador '{lexema}' sin valor antes del operador lógico")
            if i == len(tokens) - 1 or tokens[i+1][0] not in ["IDENTIFICADOR", "NUMERO_FLOAT", "NUMERO_ENTERO", "CADENA", "DELIMITADOR"]:
                errores.append(f"Error en posición {pos}: Operador '{lexema}' sin valor después del operador lógico")

        if tipo == "IDENTIFICADOR":
            if i > 0:
                token_anterior = tokens[i-1]
                if token_anterior[1] in ["var", "fun", "float", "int", "number"]:
                    identificadores_definidos.add(lexema)
                elif token_anterior[1] not in ["call"] and lexema not in identificadores_definidos:
                    if not (i > 1 and tokens[i-2][1] in ["var", "float", "int", "number", "fun", "call"]):
                        errores.append(f"Error en posición {pos}: Identificador '{lexema}' indefinido")

        if lexema == "fun":
            if i + 2 >= len(tokens) or tokens[i+1][0] != "IDENTIFICADOR" or tokens[i+2][1] != "{":
                errores.append(f"Error en posición {pos}: Estructura incorrecta de función")

        if tipo == "IDENTIFICADOR" and i + 1 < len(tokens):
            siguiente_token = tokens[i+1]
            if siguiente_token[1] == "=":
                if i + 2 >= len(tokens) or tokens[i+2][0] not in ["NUMERO_FLOAT", "NUMERO_ENTERO", "IDENTIFICADOR", "CADENA"]:
                    errores.append(f"Error en posición {pos}: Asignación incorrecta para '{lexema}'")

        if lexema == "if":
            if i + 2 >= len(tokens) or tokens[i+1][1] != "(":
                errores.append(f"Error en posición {pos}: Estructura de condicional incorrecta")

        if lexema == "return":
            if i + 1 >= len(tokens) or tokens[i+1][0] not in ["IDENTIFICADOR", "NUMERO_FLOAT", "NUMERO_ENTERO"]:
                errores.append(f"Error en posición {pos}: Return vacío")
        
        if lexema == "in":
            if i + 1 >= len(tokens) or tokens[i+1][0] not in ["IDENTIFICADOR"]:
                errores.append(f"Error en posición {pos}: Ningun identificador asociado para entrada")

        if lexema == "out":
            if i + 1 >= len(tokens) or tokens[i+1][1] != "(":
                errores.append(f"Error en posición {pos}: Error en impresion de entrada o salida")

        if lexema in ["var", "number", "float", "int"]:  
            if i + 2 >= len(tokens):
                errores.append(f"Error en posición {pos}: Error de declaración de variable")
            else:
                if tokens[i+2][1] != "=":
                    errores.append(f"Error en posición {pos}: Error en declaración de variable")
                else:
                    identificadores_definidos.add(tokens[i+1][1])

        if tipo == "DELIMITADOR":
            if lexema in "{(":
                delimitadores_stack.append(lexema)
            elif lexema in "})":
                if not delimitadores_stack:
                    errores.append(f"Error en posición {pos}: Delimitador de cierre '{lexema}' sin apertura correspondiente")
                else:
                    ultimo_delimitador = delimitadores_stack.pop()
                    if (ultimo_delimitador == "{" and lexema != "}") or \
                       (ultimo_delimitador == "(" and lexema != ")"):
                        errores.append(f"Error en posición {pos}: Delimitador no coincidente")

        i += 1

    if delimitadores_stack:
        errores.append(f"Error: Faltan delimitadores de cierre")

    return errores

codigo_fuente = """
Begin
fun app {
    var x = 6
    var y = 5
    var string = "Hola mundo"
    number y = 5.5
    if (x > y) {
        var sum = x + y
        return sum
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
