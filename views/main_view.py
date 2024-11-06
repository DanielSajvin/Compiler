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

        self.btn_asm.clicked.connect(self.save_asm_file)


        self.btn_generate_exe.clicked.connect(self.generate_exe)  # Nuevo botón para generar .exe y .obj


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

            # Convertir código intermedio a código máquina y mostrarlo en 'txt_maquina'
            machine_code = compiled.convert_to_assembly(intermediate_code)
            self.txt_maquina.setText(machine_code)

        except Exception as e:
            print(f"Error: {e}")  # Mostrar el error en la consola para diagnosticar

    def save_asm_file(self):
        # Obtener el código que ya está en txt_maquina
        asm_code = self.txt_maquina.toPlainText()

        if asm_code.strip() == "":
            # Si no hay nada en el cuadro de texto de código máquina, mostrar un mensaje de error
            self.show_error_message("No hay código máquina generado para guardar.")
            return

        # Abrir el cuadro de diálogo para guardar el archivo
        file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo ASM', '', 'ASM Files (*.asm);;All Files (*)')

        if file_name:  # Si el usuario seleccionó un nombre de archivo
            try:
                # Escribir el contenido del código en el archivo seleccionado
                with open(file_name, 'w') as asm_file:
                    asm_file.write(asm_code)
                self.show_success_message(f"Archivo guardado exitosamente en {file_name}")
            except Exception as e:
                # Mostrar un mensaje de error si hay algún problema al escribir el archivo
                self.show_error_message(f"Error al guardar el archivo: {str(e)}")

    def generate_exe(self):
        asm_file_path = QFileDialog.getOpenFileName(self, 'Select ASM File', '', 'Assembly Files (*.asm)')[0]
        if asm_file_path:
            obj_file = asm_file_path.replace('.asm', '.obj')
            exe_file = asm_file_path.replace('.asm', '.exe')

            try:
                # Compilar el archivo .asm a .obj
                subprocess.run(['ml', '/c', '/Fo' + obj_file, asm_file_path], check=True)  # ml es MASM en Windows

                # Enlazar el archivo .obj a .exe
                subprocess.run(['link', '/OUT:' + exe_file, obj_file], check=True)

                QMessageBox.information(self, "EXE Generated", f"Archivo .exe generado en {exe_file}")

            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Error al generar .exe: {e}")
            except FileNotFoundError:
                QMessageBox.critical(self, "Error",
                                     "MASM o LINK no encontrados. Asegúrate de que están instalados y en el PATH.")


