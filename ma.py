import re # Librería para expresiones regulares
# Declaramos file para abrir el archivo y leerlo despues
file = open("TestFiles/read.txt")

# Declaramos un diccionario "reservedWord" para saber todos los tkns
reservedWord = {'entero': 'Palabra reservada',
                'decimal': 'Palabra reservada',
                'booleano': 'Palabra reservada',
                'cadena': 'Palabra reservada',
                'si': 'Palabra reservada',
                'sino': 'Palabra reservada',
                'mientras': 'Palabra reservada',
                'hacer': 'Palabra reservada',
                'verdadero': 'Palabra reservada',
                'falso': 'Palabra reservada',
                'print': 'Palabra reservada'  # Asegurarnos de incluir "imprimir" aquí
}
reservedWord_key = reservedWord.keys()

# Declaramos un diccionario "operator" para saber todos los tkns
operator = {'+': 'Operador',
            '-': 'Operador',
            '*': 'Operador',
            '/': 'Operador',
            '%': 'Operador',
            '=': 'Operador',
            '==': 'Operador',
            '<': 'Operador',
            '>': 'Operador',
            '>=': 'Operador',
            '<=': 'Operador'}
operator_key = operator.keys()

# Declaramos un diccionario "sign" para saber todos los tkns
sign = {'(': 'Signo',
        ')': 'Signo',
        '{': 'Signo',
        '}': 'Signo',
        '"': 'Signo',
        ';': 'Signo'}
sign_key = sign.keys()


identifier = {chr(i): 'Identificador' for i in range(97, 123)}  # Genera identificadores de 'a' a 'z'
identifier_key = identifier.keys()

a = file.read()

# Contadores
count = 0  # Contador para ver el numero de linea que toca
lexical_errors = []  # Lista para almacenar los errores léxicos

program = a.split("\n")

for line in program:
    count += 1
    print("Linea#", count, "\n", line)
    tokens = line.split(' ')
    print("Los tokens son: ", tokens)

    for token in tokens:
        if token in reservedWord_key:
            print("[", token, "]", "es: ", reservedWord[token])

        elif token in operator_key:
            print("[", token, "]", "es:", operator[token])

        elif token in sign_key:
            print("[", token, "]", "es:", sign[token])

        elif token in identifier_key:
            print("[", token, "]", "es", identifier[token])

        elif re.match("^[0-9]+$", token):
            print("[", token, "]", "El token es un número entero")

        elif re.match("^[0-9]+[a-zA-ZñÑ]+$", token):
            print("[", token, "]", "es una palabra")

        else:
            lexical_errors.append(f"Error léxico en token: {token} en la línea {count}")
            print(f"Error léxico en token: {token} en la línea {count}")

    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
