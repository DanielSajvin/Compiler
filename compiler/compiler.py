# Libreria para expresiones regulares
import re


class Compiler:
    def __init__(self, file):
        # Declaramos el archivo
        self.file = file

        self.countReserverdWordPrint = 0
        self.countIdentifierPrint = 0
        self.countOperatorPrint = 0
        self.countSignPrint = 0
        self.intermediate_code = []  # Para almacenar el código intermedio

        # Declaramos un diccionario "reservedWord" para saber todos los tkns
        self.reservedWord = {'entero': 'Palabra reservada',
                             'decimal': 'Palabra reservada',
                             'booleano': 'Palabra reservada',
                             'cadena': 'Palabra reservada',
                             'si': 'Palabra reservada',
                             'sino': 'Palabra reservada',
                             'sino si': 'Palabra reservada',
                             'mientras': 'Palabra reservada',
                             'hacer': 'Palabra reservada',
                             'para': 'Palabra reservada',
                             'func': 'Palabra reservada',
                             'print': 'Palabra reservada',}
        self.reservedWord_key = self.reservedWord.keys()

        self.declared_variables = {}
        self.declared_variables_keys = self.declared_variables.keys()

        self.function_declared_variables = {}
        self.function_declared_variables_keys = self.function_declared_variables.keys()

    # Analisis del archivo completo y sus cadenas
    def parse(self):
        # FUNCIONES CONTADORES
        def check_sign_in_token(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.findall(pattern, token)

            if match:
                return len(match)

        def check_operator_in_token(token):
            pattern = r"[\+\-\*\/\%\=\==\<\>\>=\<=]"
            match = re.findall(pattern, token)

            if match:
                return len(match)

        def check_identifier_in_token(token):
            pattern = r'\b(?!entero|decimal|booleano|print|cadena|si|sino|mientras|hacer|verdadero|falso|[0-9])\w+(?!\w*;)(' \
                      r'?=(?:[^"]|"[^"]*")*$)\b'
            # \b(?!entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso)[^\W\d]+\b(?=(?:(?:[^"]*"){
            # 2})*[^"]*$) casi funciona \b(?!entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso
            # |"|[0-9])\w+\b casi funciona x2 pero reconoce tambien los valores que se le da a la variable
            match = re.findall(pattern, token)

            if match:
                return len(match)

        def check_reserverdWord_in_token(token):
            pattern = r"\b(entero|decimal|booleano|cadena|si|sino|sino si|mientras|hacer|verdadero|falso|print)\b"
            match = re.findall(pattern, token)

            if match:
                return len(match)

        # VERIF SINTAX
        def check_variable_declaration(declaration):
            pattern = r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^;]+)\s*;"

            match = re.match(pattern, declaration)

            if match:
                type = match.group(1)

                if type in self.reservedWord_key:
                    try:
                        name = match.group(2)
                        value = match.group(3)

                        self.declared_variables[name] = value

                        message = f"Tipo de variable: {type}\nNombre de variable: {name}\nValor de la variable: {value}"

                        eval(value)
                        # check_declaration_value(declaration)

                        return message
                    except:
                        return f"{declaration}\nEl valor de la variable no esta en el formato correcto"
                else:
                    return f"{declaration}\nEl tipo de variable no es correcto"
            else:
                is_modification = check_variable_modification(declaration)
                if not (is_modification[1]):
                    return f"{declaration}\nLa declaracion de la variable no es correcta"

                else:
                    return is_modification[0]

        def check_variable_modification(modification):
            pattern = r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([+\-]?=)\s*([^;\n\r]+)\s*;"

            match = re.match(pattern, modification)

            if not (match):
                return f"{modification} esta mal declarado"

            else:
                var_name = match.group(1)

                if var_name not in self.declared_variables_keys \
                        and var_name not in self.function_declared_variables_keys:
                    return f"{var_name} no existe", False

                else:
                    # value = match.group(3)
                    # prev_value = self.declared_variables[var_name]
                    # mod_value = match.group(3)
                    #
                    # operation = match.group(2)
                    # if operation == "=":
                    #     new_value = mod_value
                    #
                    # elif operation == "+=":
                    #     if isinstance(prev_value, numbers.Number):
                    #         print('int')
                    #         new_value = prev_value + mod_value
                    #
                    #     elif isinstance(prev_value, float):
                    #         print('float')
                    #         new_value = float(prev_value) + float(mod_value)
                    #
                    #     elif isinstance(prev_value, str):
                    #         print('string')
                    #         prev_value = prev_value.replace('"', '')
                    #         mod_value = mod_value.replace('"', '')
                    #
                    #         new_value = prev_value + mod_value
                    #
                    # elif operation == "-=":
                    #     new_value = prev_value - mod_value
                    #
                    # self.declared_variables[var_name] = new_value

                    return f"Modificacion de variable\nNombre de variable: {var_name}\n", True

        def check_condition_statement(statement):
            pattern = r"\(\s*(.[^()]+)\s*(==|!=|>=|<=|>|<|is|is not)\s*(.[^()]+)\)"

            match = re.match(pattern, statement)

            if not (match):
                return f"{statement} mal declarado"

            else:
                return f"{statement} bien declarado"

        def check_if_statement(statement):
            pattern = r"\s*(si)\s*(\(.*?\))\s*(\{.*?\})\s*((sino)\s*(\{.*?\}))?"

            match = re.match(pattern, statement)
            if match:
                # Palabras reservadas utilizadas (si, sino)
                used_reserved = [match.group(1)]
                conditions = [match.group(2)]  # Condición (dentro del "si")
                actions = [match.group(3)]  # Acciones para el bloque verdadero

                if match.group(5):  # Sino existe
                    used_reserved.append(match.group(5))  # Añadimos 'sino'
                    actions.append(match.group(6))  # Acción para el bloque "sino"

                message = f"Palabras reservadas: {', '.join(used_reserved)}\nCondiciones: "

                for c in conditions:
                    message += f"{check_condition_statement(c)}, "  # Verificar cada condición

                message += f"\nAcciones: {', '.join(actions)}"

                return message
            else:
                return "La condición está mal declarada."
            
            """
            pattern = r"\s*((si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((" \
                      r"sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*(" \
                      r"(sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{" \
                      r"}]+\}))?\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((sino)\s*(\{.[^{}]+\}))?"

            
            grupo 0: EXPRESION COMPLETA
            grupo 1: si (CONDICION) {ACCION SI VERDADERO}
            grupo 2: si
            grupo 3: (CONDICION)
            grupo 4: {ACCION SI VERDADERO}
            grupo 5: sino si (CONDICION) {ACCION SI VERDADERO}
            grupo 6: sino si
            grupo 7: (CONDICION)
            grupo 8: {ACCION SI VERDADERO}
            grupo 29: sino {ACCION}
            grupo 30: sino
            grupo 31: {ACCION}

            ESTA SUJETO A BUGS EN CASO DE VARIOS "sino si" DEBIDO A LA FORMA EN LA QUE OPERA
            LA EXPRESION REGULAR AL MOMENTO DE EVALUAR
            
            (SE INTENTO SOLUCIONAR INSERTANDO VARIOS SINO SI EN LA EXPRESION REGULAR, MAS NO ES UNA SOLUCION
            ABSOLUTA)
            

            match = re.match(pattern, statement)
            if match:
                used_reserved = [match.group(2)]
                conditions = [match.group(3)]
                actions = [match.group(4)]

                for number in range(0, 31):
                    group = match.group(number)
                    if group is not None:
                        if number == 6 or number == 30:
                            used_reserved.append(group)

                        elif number == 7 or number == 11 or number == 15 or number == 19 or number == 23 or number == 27:
                            conditions.append(group)

                        elif number == 8 or number == 12 or number == 16 or number == 20 or number == 24 or number == 28 or number == 31:
                            actions.append(group)

                message = f"Palabras reservadas: {', '.join(used_reserved)}\nCondiciones: "

                for c in conditions:
                    message += f"{check_condition_statement(c)}, "

                message += f"\nAcciones: {', '.join(actions)}"

                return message
            else:
                return "La condicion esta mal declarada."
        """

        def is_token_sign(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.match(pattern, token)

            if match:
                return True
            else:
                return False

        def check_doWhile_statement(statement):
            pattern = r"(hacer)\s*(\{[\s\S]*?\})\s*(mientras)\s*(\(.[^()]+\))\s*;"

            match = re.match(pattern, statement)
            if match:
                message = f"Palabra reservada: hacer, mientras\nCondicion: {match.group(4)}\nAcciones: {match.group(2)}"

            else:
                message =  "La condicion -hacer/mientras- esta mal declarada"

            return message

        def check_while_statement(statement):
            pattern = r"(mientras)\s*(\([^;]+\))\s*(\{[\s\S]*?\})"


            match = re.match(pattern, statement)
            if match:
                message = f"Palabra reservada: mientras\nCondiciones: {check_condition_statement(match.group(2))}\nAcciones: {match.group(3)}"

            else:
                message = "La condicion -mientras- esta mal declarada"
            return message

        def check_atribute_statement(statement):
            pattern = r"\s*([a-zA-Z0-9_]*)\s+([a-zA-Z0-9_]*)\s*=?\s*(.*)"
            message = ''

            match = re.match(pattern, statement)
            if match:
                name = match.group(2)
                value = match.group(3)

                if value == '':
                    self.function_declared_variables[name] = value
                    message = f"'{statement}' bien declarado\t"

                else:
                    try:
                        eval(value)
                        self.function_declared_variables[name] = value
                        message = f"{statement} bien declarado"

                    except:
                        message = 'ATRIBUTO MAL DECLARADO'

            else:
                message = f"{statement} mal declarado"

            return message


        def check_function_statement(statement):
            pattern = r"\s*(func)\s*([a-zA-Z0-9_]+)\s*\(([^()]*)\)\s*([^{}]+)\s*(end func\([^()]+\);)"

            match = re.match(pattern, statement)
            if match:
                message = f"Palabra reservada: func: {check_condition_statement(match.group(1))}\nNombre de la funcion: {match.group(2)}\n"
                atributes = match.group(3)
                if atributes is not None:
                    self.function_declared_variables.clear()

                    atribute_list = atributes.split(',')

                    message += 'Atributes: '

                    for a in atribute_list:
                        message += check_atribute_statement(a)

                    message += f"\nAcciones: {match.group(4)}"
            else:
                message = "La funcion esta mal declarada"
            return message

        file = open(self.file)

        # Extraer el contenido del archivo
        content = file.read()

        program = content.split("\n")

        # Declaracion de variables
        message = ""  # Mensaje final

        for i, token in enumerate(program):
            if token != '':
                if check_operator_in_token(token):
                    self.countOperatorPrint += check_operator_in_token(token)

                if check_reserverdWord_in_token(token):
                    self.countReserverdWordPrint += check_reserverdWord_in_token(token)

                if check_sign_in_token(token):
                    self.countSignPrint += check_sign_in_token(token)

                if check_identifier_in_token(token):
                    self.countIdentifierPrint += check_identifier_in_token(token)

                if 'si' in token and 'sino' not in token:
                    token = ''

                    for new_token in program[i:]:
                        token += f"{new_token}"

                        if '}' in new_token and 'sino' not in new_token:
                            break

                    message += f"{check_if_statement(token)}\n\n\n"

                elif '#' in token[0]:
                    message += f"Comentario: {token.replace('#', '')}\n\n\n"

                elif is_token_sign(token):
                    message += ''

                elif 'hacer' in token:
                    token = ''

                    for new_token in program[i:]:
                        token += f"{new_token}"
                        print(token)

                        if '}' in new_token and 'mientras' in new_token:
                            break

                    message += f"{check_doWhile_statement(token)}\n\n\n"

                elif 'mientras' in token and '}' not in token:
                    token = ''

                    for new_token in program[i:]:
                        token += f"{new_token}"

                        if '}' in new_token and 'mientras' not in new_token:
                            break

                    message += f"{check_while_statement(token)}\n\n\n"

                elif 'func' in token and 'end' not in token:
                    token = ''

                    function_name = program[i:][0].split()[1]
                    for new_token in program[i:]:
                        token += f"{new_token}"

                        if 'end function' in new_token and function_name in new_token:
                            break
                    message += f"{check_function_statement(token)}\n\n\n"

                else:
                    message += f"{check_variable_declaration(token)}\n\n\n"

        file.close()
        return message

    # Metodo para obtener el codigo intermedio
    def generate_intermediate_code(self, program):
        temp_count = 0
        label_count = 0

        def new_temp():
            nonlocal temp_count
            temp_name = f"T{temp_count}"
            temp_count += 1
            return temp_name

        def new_label():
            nonlocal label_count
            label_name = f"L{label_count}"
            label_count += 1
            return label_name

        intermediate_code = []
        current_label_true = None
        current_label_false = None
        current_end_label = None
        in_if_block = False  # Bandera para saber si estamos dentro de un bloque 'si'
        in_do_while_block = False  # Bandera para saber si estamos dentro de un bloque 'hacer mientras'

        # Función para validar condiciones simples (si, mientras, hacer mientras)
        def validate_condition(condition):
            # Verifica que la condición esté bien formada (por ejemplo, no vacía y contenga un operador lógico)
            pattern = r'^[a-zA-Z0-9_]+\s*(>|<|==|>=|<=|!=)\s*[a-zA-Z0-9_]+$'
            return re.match(pattern, condition)

        for line in program:
            line = line.strip()  # Limpiar la línea de espacios

            # Procesar condicionales "si"
            if "si" in line:
                condition_match = re.search(r"\((.*?)\)", line)
                if condition_match:
                    condition_text = condition_match.group(1).strip()

                    # Validar condición del 'si'
                    if not validate_condition(condition_text):
                        intermediate_code.append(f"ERROR: Condición mal declarada en: {line}")
                        continue

                    # Crear etiquetas para el flujo de control
                    current_label_true = new_label()
                    current_label_false = new_label()
                    current_end_label = new_label()
                    in_if_block = True  # Activar bandera para indicar que estamos dentro de un 'si'

                    # Generar código intermedio para la condición 'si'
                    intermediate_code.append(f"IF {condition_text} GOTO {current_label_true}")
                    intermediate_code.append(f"GOTO {current_label_false}")
                    intermediate_code.append(f"{current_label_true}:")  # Etiqueta para el bloque 'si'
                else:
                    intermediate_code.append(f"ERROR: Condición mal declarada en: {line}")

            # Procesar "sino"
            elif "sino" in line:
                if in_if_block:  # Asegurarse de que exista un 'si' previo
                    intermediate_code.append(f"GOTO {current_end_label}")
                    intermediate_code.append(f"{current_label_false}:")  # Etiqueta para el bloque 'sino'
                    in_if_block = False  # Desactivar la bandera para indicar que se terminó el bloque 'si'
                else:
                    intermediate_code.append("ERROR: 'sino' sin 'si' precedente.")

            # Procesar ciclos "mientras"
            elif "mientras" in line and not "hacer" in line:
                condition_match = re.search(r"\((.*?)\)", line)
                if condition_match:
                    condition_text = condition_match.group(1).strip()

                    # Validar condición del 'mientras'
                    if not validate_condition(condition_text):
                        intermediate_code.append(f"ERROR: Condición mal declarada en: {line}")
                        continue

                    start_label = new_label()
                    end_label = new_label()

                    # Generar código intermedio para el ciclo 'mientras'
                    intermediate_code.append(f"{start_label}:")
                    intermediate_code.append(f"IF {condition_text} GOTO {start_label}")
                    intermediate_code.append(f"GOTO {end_label}")
                    current_end_label = end_label
                else:
                    intermediate_code.append(f"ERROR: Condición mal declarada en: {line}")

            # Procesar ciclos "hacer mientras"
            elif "hacer" in line:
                start_label = new_label()
                intermediate_code.append(f"{start_label}:")  # Etiqueta para el inicio del ciclo 'hacer'
                in_do_while_block = True  # Activar la bandera

            # Procesar condición "mientras" del ciclo "hacer mientras"
            elif "mientras" in line and "hacer" in line:
                if in_do_while_block:
                    condition_match = re.search(r"\((.*?)\)", line)
                    if condition_match:
                        condition_text = condition_match.group(1).strip()

                        # Validar condición del 'hacer mientras'
                        if not validate_condition(condition_text):
                            intermediate_code.append(f"ERROR: Condición mal declarada en: {line}")
                            continue

                        intermediate_code.append(f"IF {condition_text} GOTO {start_label}")
                        in_do_while_block = False  # Desactivar la bandera
                    else:
                        intermediate_code.append(f"ERROR: Condición mal declarada en: {line}")
                else:
                    intermediate_code.append(f"ERROR: 'hacer mientras' sin bloque 'hacer' precedente.")

            # Manejo de cierre de bloques con "}"
            elif "}" in line:
                if current_end_label:
                    intermediate_code.append(f"{current_end_label}:")
                    current_end_label = None

            # Procesar operaciones dentro de los bloques si/sino o mientras
            elif "=" in line:
                parts = line.split("=")
                left = parts[0].strip()
                right = parts[1].strip().replace(";", "")

                if any(op in right for op in ["+", "-", "*", "/"]):
                    operands = re.split(r'(\+|\-|\*|\/)', right)
                    if len(operands) == 3:
                        temp_var = new_temp()
                        intermediate_code.append(f"{temp_var} = {operands[0].strip()} {operands[1]} {operands[2].strip()}")
                        intermediate_code.append(f"{left} = {temp_var}")
                    else:
                        intermediate_code.append(f"ERROR: Expresión inválida en: {line}")
                else:
                    intermediate_code.append(f"{left} = {right}")

        return "\n".join(intermediate_code)

