# Importaciones de interfaz
from PyQt5 import uic  # Lanza error, pero es por el pycharm, no porque no funcione
from PyQt5.QtWidgets import QMainWindow, QFileDialog

# Importacion del paquete y clase Compile
from compiler import Compiler


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar archivo .ui
        uic.loadUi("views/designs/main_view.ui", self)

        # Mostrar interfaz
        self.show()

        # Al iniciar la interfaz

        # Interacciones con la interfaz
        self.openFile.clicked.connect(self.create)

    # Seleccionar el archivo a compilar
    def create(self) -> None:
        # Obtener la dirección del archivo
        file_name = QFileDialog.getOpenFileName(self, 'Select Program', 'D:/', 'File (*.txt)')[0]

        # Si se escoge un archivo, entonces...
        if file_name != '':
            # print(file_name)

            # Conseguir el nombre del archivo (de C:/dirección/de/archivo.txt a solamente archivo.txt)
            def get_name(string):
                def invertir_cadena(chain):
                    return chain[::-1]

                cadena_invertida = invertir_cadena(string)
                counter = 0
                letter = ''
                new_string = ''
                while letter != '/':
                    new_string += letter
                    letter = cadena_invertida[counter]
                    counter += 1

                name = invertir_cadena(new_string)
                return name

            # Cambiar el texto de lineText por el nombre del archivo (la barra al lado del botón "Abrir Archivo")
            self.fileName.setText(get_name(file_name))

            # Llamado del método "update_file_text_edit"
            self.update_fileContent_text_edit(file_name)

            # Llamado del metodo "compile"
            self.compile(file_name)

    # Cambiar textEdit "Texto" por el contenido del archivo
    def update_fileContent_text_edit(self, file):
        # Se abre el archivo en modo de lectura como f
        with open(file, 'r') as f:
            # Se leen los contenidos del archivo
            contents = f.read()

            # En el textEdit llamado "fileContent" se colocan los contenidos del archivo
            self.fileContent.setText(contents)

            f.close()

    # Cambiar el textEdit "Valores" por los valores encontrados en el archivo
    def update_fileValues_text_edit(self, values):
        self.fileValues.setText(values)

    # Cambiar el textEdit "Lista de Componentes" por los componentes del archivo
    def update_fileComponentes_text_edit(self, components):
        self.fileComponents.setText(components)

    # Compilar archivo
    def compile(self, file):
        try:
            compiled = Compiler(file)
            data = compiled.parse()
            data2 = f"Total de Operadores: {compiled.countOperatorPrint} \n " \
                    f"Total de Palabras Reservadas: {compiled.countReserverdWordPrint} \n " \
                    f"Total de Identificadores: {compiled.countIdentifierPrint} \n " \
                    f"Total de Signos: {compiled.countSignPrint} "
            self.update_fileComponentes_text_edit(data2)
            self.update_fileValues_text_edit(data)

            # Mostrar errores léxicos, sintácticos y semánticos
            errors = "\n".join(compiled.lexical_errors + compiled.syntax_errors + compiled.semantic_errors)
            self.txt_errores.setText(errors)  # Mostrar los errores en el QTextEdit 'txt_errores'

            # Generar código intermedio (por separado del análisis)
            with open(file, 'r') as f:
                file_content = f.read()  # Leer el contenido del archivo de nuevo para el código intermedio
                intermediate_code = compiled.generate_intermediate_code(file_content)  # Generar código intermedio

            # Finalmente, mostramos el código intermedio en el QTextEdit llamado label_inter
            self.label_inter.setText(intermediate_code)
        except Exception as e:
            print(f"Error: {e}")  # Mostrar el error en la consola para diagnosticar