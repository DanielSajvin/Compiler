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
        self.label_count = 0  # Contador para generar etiquetas únicas

        # Errores
        self.lexical_errors = []
        self.syntax_errors = []
        self.semantic_errors = []

        # Diccionario de palabras reservadas
        self.reservedWord = {
            'entero': 'Palabra reservada',
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
            'print': 'Palabra reservada',
        }
        self.reservedWord_key = self.reservedWord.keys()

        self.declared_variables = {}
        self.declared_variables_keys = self.declared_variables.keys()

        self.function_declared_variables = {}
        self.function_declared_variables_keys = self.function_declared_variables.keys()

    # Función para generar etiquetas únicas
    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

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
            pattern = r'\b(?!entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso|print|[0-9])\w+(?!\w*;)(' \
                      r'?=(?:[^"]|"[^"]*")*$)\b'
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

                        return message
                    except:
                        self.semantic_errors.append(f"Error semántico en {declaration}: valor no válido")
                        return f"{declaration}\nEl valor de la variable no está en el formato correcto"
                else:
                    self.semantic_errors.append(f"Error semántico en {declaration}: tipo no válido")
                    return f"{declaration}\nEl tipo de variable no es correcto"
            else:
                is_modification = check_variable_modification(declaration)
                if not (is_modification[1]):
                    self.syntax_errors.append(f"Error sintáctico en {declaration}")
                    return f"{declaration}\nLa declaración de la variable no es correcta"

                else:
                    return is_modification[0]

        def check_variable_modification(modification):
            pattern = r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([+\-]?=)\s*([^;\n\r]+)\s*;"

            match = re.match(pattern, modification)

            if not (match):
                return f"{modification} está mal declarado", False

            else:
                var_name = match.group(1)

                if var_name not in self.declared_variables_keys \
                        and var_name not in self.function_declared_variables_keys:
                    self.semantic_errors.append(f"Error semántico: {var_name} no está declarado")
                    return f"{var_name} no existe", False

                return f"Modificación de variable\nNombre de variable: {var_name}\n", True

        def check_condition_statement(statement):
            pattern = r"\(\s*(.[^()]+)\s*(==|!=|>=|<=|>|<|is|is not)\s*(.[^()]+)\)"

            match = re.match(pattern, statement)

            if not (match):
                self.syntax_errors.append(f"Error sintáctico en {statement}")
                return f"{statement} mal declarado"

            return f"{statement} bien declarado"

        def check_if_statement(statement):
            pattern = r"\s*((si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((" \
                      r"sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*(" \
                      r"(sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{" \
                      r"}]+\}))?\s*((sino si)\s*(\(.[^()]+\))\s*(\{.[^{}]+\}))?\s*((sino)\s*(\{.[^{}]+\}))?"

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
                self.syntax_errors.append(f"Error sintáctico en {statement}")
                return "La condición está mal declarada."

        def is_token_sign(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.match(pattern, token)

            if match:
                return True
            return False

        def check_doWhile_statement(statement):
            pattern = r"(hacer)\s*(\{[\s\S]*?\})\s*(mientras)\s*(\(.[^()]+\))\s*;"

            match = re.match(pattern, statement)
            if match:
                message = f"Palabra reservada: hacer, mientras\nCondición: {match.group(4)}\nAcciones: {match.group(2)}"
            else:
                self.syntax_errors.append(f"Error sintáctico en {statement}")
                message = "La condición -hacer/mientras- está mal declarada"

            return message

        def check_while_statement(statement):
            pattern = r"(mientras)\s*(\([^;]+\))\s*(\{[\s\S]*?\})"

            match = re.match(pattern)
            if match:
                message = f"Palabra reservada: mientras\nCondiciones: {check_condition_statement(match.group(2))}\nAcciones: {match.group(3)}"
            else:
                self.syntax_errors.append(f"Error sintáctico en {statement}")
                message = "La condición -mientras- está mal declarada"
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
                        self.semantic_errors.append(f"Error semántico en {statement}: valor no válido")
                        message = 'Atributo mal declarado'
            else:
                self.syntax_errors.append(f"Error sintáctico en {statement}")
                message = f"{statement} mal declarado"

            return message

        def check_function_statement(statement):
            pattern = r"\s*(func)\s*([a-zA-Z0-9_]+)\s*\(([^()]*)\)\s*([^{}]+)\s*(end func\([^()]+\);)"

            match = re.match(pattern)
            if match:
                message = f"Palabra reservada: func: {check_condition_statement(match.group(1))}\nNombre de la función: {match.group(2)}\n"
                atributes = match.group(3)
                if atributes is not None:
                    self.function_declared_variables.clear()

                    atribute_list = atributes.split(',')

                    message += 'Atributos: '

                    for a in atribute_list:
                        message += check_atribute_statement(a)

                    message += f"\nAcciones: {match.group(4)}"
            else:
                self.syntax_errors.append(f"Error sintáctico en {statement}")
                message = "La función está mal declarada"
            return message

        file = open(self.file)
        content = file.read()
        program = content.split("\n")
        message = ""  # Mensaje final

        for i, line in enumerate(program):
            tokens = line.split()
            for token in tokens:
                if token in self.reservedWord_key:
                    self.countReserverdWordPrint += 1
                elif check_operator_in_token(token):
                    self.countOperatorPrint += check_operator_in_token(token)
                elif check_sign_in_token(token):
                    self.countSignPrint += check_sign_in_token(token)
                elif check_identifier_in_token(token):
                    self.countIdentifierPrint += check_identifier_in_token(token)
                elif re.match("^[0-9]+$", token):  # Números enteros
                    continue
                else:
                    # Si el token no coincide con ningún conjunto conocido, es un error léxico
                    self.lexical_errors.append(f"Error léxico en token: '{token}' en la línea {i + 1}")
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
        # Reiniciar el código intermedio
        self.intermediate_code = []

        # Inicializar etiquetas para el flujo de control
        label_true = None
        label_false = None
        label_end = None

        # Dividir el programa en líneas
        program_lines = program.split("\n")

        inside_if_block = False
        inside_else_block = False

        for line in program_lines:
            line = line.strip()

            # Detectar declaración de variables
            if "entero" in line or "decimal" in line:  # Detecta declaración de variables
                var_declaration = re.match(r"(entero|decimal)\s+(\w+)\s*=\s*(.+);", line)
                if var_declaration:
                    var_type = var_declaration.group(1)  # 'entero' o 'decimal'
                    var_name = var_declaration.group(2)  # Nombre de la variable
                    var_value = var_declaration.group(3)  # Valor asignado a la variable

                    # Generar código intermedio para la declaración de variables
                    self.intermediate_code.append(f"{var_name} = {var_value}")
                else:
                    self.intermediate_code.append(f"ERROR: Declaración inválida en: {line}")

            # Detectar la estructura del 'si'
            elif "si" in line:  # Detecta la estructura del 'si'
                condition_match = re.search(r"\((.*?)\)", line)
                if condition_match:
                    condition = condition_match.group(1)
                    label_true = self.new_label()
                    label_false = self.new_label()
                    label_end = self.new_label()

                    # Generar código intermedio para la condición 'si'
                    self.intermediate_code.append(f"IF {condition} GOTO {label_true}")
                    self.intermediate_code.append(f"GOTO {label_false}")
                    self.intermediate_code.append(f"{label_true}:")  # Etiqueta verdadera
                    inside_if_block = True

            elif "sino" in line:  # Detecta la estructura del 'sino'
                if label_false is not None:
                    # Antes de entrar al bloque 'sino', debemos saltar al final del bloque 'si'
                    self.intermediate_code.append(f"GOTO {label_end}")
                    self.intermediate_code.append(f"{label_false}:")  # Etiqueta falsa del 'si'
                    inside_if_block = False
                    inside_else_block = True

            elif "{" in line or "}" in line:
                # Ignorar las llaves
                continue

            elif "print" in line:  # Instrucción de impresión dentro del bloque 'si' o 'sino'
                content = line.split('print')[1].strip().replace(";", "").replace("(", "").replace(")", "")
                if inside_if_block:
                    self.intermediate_code.append(f"CALL print({content})")  # Dentro del bloque 'si'
                    inside_if_block = False  # Aquí aseguramos que se termine el bloque 'si'
                    self.intermediate_code.append(f"GOTO {label_end}")  # Saltar al final después del 'si'
                elif inside_else_block:
                    self.intermediate_code.append(f"CALL print({content})")  # Dentro del bloque 'sino'
                    inside_else_block = False  # Termina el bloque 'sino'

        if label_end:
            # Marcar el final del condicional
            self.intermediate_code.append(f"{label_end}:")

        return "\n".join(self.intermediate_code)
