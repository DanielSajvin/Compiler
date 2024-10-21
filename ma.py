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
                'falso': 'Palabra reservada'}
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

identifier = {'a': 'Identificador',
              'b': 'Identificador',
              'c': 'Identificador',
              'd': 'Identificador',
              'e': 'Identificador',
              'f': 'Identificador',
              'g': 'Identificador',
              'h': 'Identificador',
              'i': 'Identificador',
              'j': 'Identificador',
              'k': 'Identificador',
              'l': 'Identificador',
              'm': 'Identificador',
              'n': 'Identificador',
              'ñ': 'Identificador',
              'o': 'Identificador',
              'p': 'Identificador',
              'q': 'Identificador',
              'r': 'Identificador',
              's': 'Identificador',
              't': 'Identificador',
              'u': 'Identificador',
              'v': 'Identificador',
              'w': 'Identificador',
              'x': 'Identificador',
              'y': 'Identificador',
              'z': 'Identificador'}
identifier_key = identifier.keys()

a = file.read()

# Contadores
count = 0  # Contador para ver el numero de linea que toca


program = a.split("\n")

for line in program:
    count = count + 1
    print("Linea#", count, "\n", line)
    tokens = line.split(' ')
    print("Los tokens son: ", tokens)
    print("Linea#", count, "propiedades \n")

    countReserverdWord = 0  # Contador para el numero de palabras reservadas que hay
    countOperator = 0  # Contador para operadores
    countSign = 0  # Contador para signos
    countIdentifier = 0  # Contador para identificadores
    countNumber = 0  # Contador para Numeros

    for token in tokens:

        if token in reservedWord_key:
            countReserverdWord = countReserverdWord + 1
            print("[", token, "]", "es: ", reservedWord[token])
            print("Cantidad que se repite: ", countReserverdWord)

        elif token in operator_key:
            countOperator = countOperator + 1
            print("[", token, "]", "es:", operator[token])
            print("Cantidad que se repite: ", countOperator)

        elif token in sign_key:
            countSign = countSign + 1
            print("[", token, "]", "es:", sign[token])
            print("Cantidad que se repite: ", countSign)

        elif token in identifier_key:
            countIdentifier = countIdentifier + 1
            print("[", token, "]", "es", identifier[token])
            print("Cantidad que se repite: ", countIdentifier)

        elif re.match("^[0-9]+$", token):
            # Si el token es un número entero, incrementa el contador y muestra la información correspondiente
            countNumber = countNumber + 1
            print("[", token, "]", "El token es un número entero")
            print("Cantidad que se repite: ", countNumber)

        elif re.match("^[0-9]+[a-zA-ZñÑ]+$", token):
            # Si el token es una palabra, muestra la información correspondiente
            print("[", token, "]", "es una palabra")

        # else:
        #    print("[", token, "]", "ERROR") # Se borra
        #    break

    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _")
