import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from ttkthemes import ThemedStyle
import shutil
import os
import winreg
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import sqlite3

# Define private and public keys
private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend)
public_key = private_key.public_key()

# Define private and public keys
private_key1 = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend)
public_key1 = private_key1.public_key()


private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )

public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

private_key1_pem = private_key1.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )

public_key1_pem = public_key1.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

key = 'PvP7oSQbrKD8HNRYvWpPTJPmqgEMZfIeO5BuS1DqDUE='

f = Fernet(key)

class ConexionDB:
    def __init__(self, path):
        self.base_datos = path
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

class ConexionCodigo:
    def __init__(self, path):
        self.base_datos = path
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

def get_passwords(path):
    connect = ConexionDB(path)

    sql = "SELECT password FROM datos_cifrados"

    connect.cursor.execute(sql)

    passwords = connect.cursor.fetchall()
    connect.cerrar()

    return passwords

def get_id(path):
    connect = ConexionDB(path)

    sql = "SELECT id_user FROM datos_cifrados"

    connect.cursor.execute(sql)

    id_user = connect.cursor.fetchall()
    connect.cerrar()

    return id_user

def get_code(path):
    connect = ConexionCodigo(path)

    sql = "SELECT FROM codigo"

    connect.cursor.execute(sql)

    code = connect.cursor.fetchall()
    connect.cerrar()

    return code

def decode_passwords(path):
    passwords = get_password(path)

    uncrypted = []

    for password in passwords:

        decrypyed_password = f.decrypt(password)

        uncrypted.append(decrypyted_password)

    return uncrypted

def encode_passwords(password, path):
    # Obtener el valor de la variable de entorno
    public_db_key = os.environ.get("Public_db_key")

    p = Fernet(public_db_key)

    passwords = decode_passwords(path)

    encryted = []

    for password in passwords:
        encrypted_password = p.encrypt(password)

        encryted.append(encrypted_password)

    return encryted

def delete_old_passwords(path, id_user):
    connect = ConexionDB(path)

    sql = "UPDATE FROM datos_cifrados(password) WHERE id_user = ?"

    connect.cursor.execute(sql, id_user)
    connect.cerrar()

class InstalacionApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.geometry("600x400")
        self.ventana.title("Asistente de Instalación")

        self.style = ThemedStyle(self.ventana)
        self.style.set_theme("equilux")
        self.style.theme_use('equilux')
        self.ventana.resizable(0, 0)

        self.ubicacion_seleccionada = 'C:/Program Files'
        self.ubicacion_database = 'C:/Program Files/Administrador de contraseñas'
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        
        self.introduccion()

    def seleccionar_ubicacion(self):
        self.ubicacion_seleccionada = filedialog.askdirectory()
        self.ubicacion_entry.delete(0, 100)
        self.ubicacion_entry.insert(0, self.ubicacion_seleccionada)
        self.ubicacion_database = self.ubicacion_seleccionada + '/Administrador de contraseñas/database'

    def seleccionar_ubicacion_db(self):
        self.ubicacion_database = filedialog.askdirectory()
        self.actualizar_entry.delete(0, 100)
        self.actualizar_entry.insert(0, self.ubicacion_database)

    def instalar(self):
        if self.ubicacion_seleccionada:
            self.instalar_progreso.grid(
                row=0, column=0, padx=(0, 20), pady=(0, 0))

            self.progreso_label.insert(
                index="0.0", text="Instalando...")
            self.progreso_label.configure(state="disabled")
            self.regresar_1_button.destroy()



            # Crear las carpetas necesarias en la ubicación seleccionada
            self.crear_carpetas()
            
            # Copiar los archivos a las carpetas correspondientes
            self.copiar_archivos()
            self.variable_entorno()
            self.crear_archivos()

            self.exito()
        else:
            tk.messagebox.showwarning(
                "Advertencia", "Debes seleccionar una ubicación de instalación.")

    def crear_carpetas(self):
        # Crear las carpetas necesarias en la ubicación seleccionada

        ruta_principal = os.path.join(
            self.ubicacion_seleccionada, "Administrador de contraseñas")
        os.makedirs(ruta_principal, exist_ok=True)

        ruta_graficos = os.path.join(ruta_principal, "image")
        os.makedirs(ruta_graficos, exist_ok=True)

        ruta_basedatos = os.path.join(ruta_principal, "database")
        os.makedirs(ruta_basedatos, exist_ok=True)

        ruta_respaldo = os.path.join(ruta_principal, "backup")
        os.makedirs(ruta_respaldo, exist_ok=True)

    def copiar_archivos(self):
        try:

            if self.ubicacion_database != self.ubicacion_seleccionada + '/Administrador de contraseñas/database':
                
                archivo_basedatos = self.ubicacion_database
                ubicacion_db = self.ubicacion_seleccionada + '/Administrador de contraseñas/database' 
            
                for file in os.listdir(self.ubicacion_database):
                    shutil.copy2(os.path.join(self.ubicacion_database, file), ubicacion_db)

            else:
                db_codigo = open(self.ubicacion_seleccionada + '/Administrador de contraseñas/database/codigo_acceso.db', 'w')
                db_codigo.close()

                db_usuarios = open(self.ubicacion_seleccionada + '/Administrador de contraseñas/database/datos_usuarios.db', 'w')
                db_usuarios.close()
        except SameFileError:
            print("Los archivos ya existen")

    def crear_archivos(self):
        respaldo_claves = open(self.ubicacion_seleccionada + '/Administrador de contraseñas/backup/.env', 'w')
        respaldo_claves.write("Public_db_key=\n")
        respaldo_claves.write(f"{public_key_pem.decode()}\n")
        respaldo_claves.write("Private_db_key=\n")
        respaldo_claves.write(f"{private_key_pem.decode()}\n")
        respaldo_claves.write("Public_table_key=\n")
        respaldo_claves.write(f"{public_key1_pem.decode()}\n")
        respaldo_claves.write("Private_table_key=\n")
        respaldo_claves.write(f"{private_key1_pem.decode()}\n")
        respaldo_claves.close()

    def introduccion(self):
        self.introduccion_frame = ctk.CTkFrame(
            self.ventana, width=600, height=600, fg_color="#242424")
        self.introduccion_frame.grid()
        self.introduccion_label = ctk.CTkTextbox(
            self.introduccion_frame, fg_color="#242424", width=400, activate_scrollbars=False)
        self.introduccion_label.grid(
            row=0, column=0, padx=(180, 0), pady=(0, 150))

        self.introduccion_label.insert(
            index="0.0", text="Bienvenido al asistente de instalacion del gestor de contraseñas\nlos pasos a continuacion te guiaran en el proceso de instalado,\nsi ya tienes alguna version instalada se actualizará.\nPresiona continuar para comenzar la instalación.")
        self.introduccion_label.configure(state="disabled")

        self.introduccion_button = ctk.CTkButton(
            self.introduccion_frame, text="Continuar", fg_color="#242424", hover_color="#2b2b2b", command=self.ubicacion, width=100)
        self.introduccion_button.grid(
            row=1, column=0, padx=(450, 0), pady=(10, 0))

    def ubicacion(self):
        self.introduccion_frame.destroy()

        self.count = self.count + 1 

        if self.count >= 2:
            self.actualizar_frame.destroy()
        
            
        self.ubicacion_frame = ctk.CTkFrame(
            self.ventana, width=600, height=600, fg_color="#242424")
        self.ubicacion_frame.grid()

        self.ubicacion_label = ctk.CTkTextbox(
            self.ubicacion_frame, fg_color="#242424", width=600, activate_scrollbars=False)
        self.ubicacion_label.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 0))

        self.ubicacion_label.insert(
            index="0.0", text="La ubicacion predeterminada es en archivos del programa, si decides cambiar la ubicacion recuerda\nque podria afectar el funcionamiento de algunas caracteristicas de la aplicacion.")
        self.ubicacion_label.configure(state="disabled")

        self.ubicacion_entry = ctk.CTkEntry(
            self.ubicacion_frame,  fg_color="#242424", border_color="#2b2b2b", border_width=1, width=400)
        self.ubicacion_entry.grid(
            row=0, column=0, padx=(0, 170), pady=(0, 50))

        self.ubicacion_entry.insert(0, self.ubicacion_seleccionada)

        self.ubicacion_button = ctk.CTkButton(
            self.ubicacion_frame, text="Seleccionar ubicacion", fg_color="#242424", hover_color="#2b2b2b", command=self.seleccionar_ubicacion, width=100)
        self.ubicacion_button.grid(
            row=0, column=0, padx=(410, 0), pady=(0, 50))

        self.ubicacion_cont_button = ctk.CTkButton(
            self.ubicacion_frame, text="Continuar", fg_color="#242424", hover_color="#2b2b2b", command=self.actualizar, width=100)
        self.ubicacion_cont_button.grid(
            row=1, column=0, padx=(420, 0), pady=(150, 0))

    def actualizar(self):
        self.ubicacion_frame.destroy()
        self.count = self.count + 1 


        if self.count1 >= 2:
            self.count1 = self.count1

        else:

            if self.count >= 2:
                self.count1 = 1
            
        if self.count1 >= 2:
            self.encriptacion_frame.destroy()

        self.actualizar_frame = ctk.CTkFrame(
            self.ventana, width=600, height=600, fg_color="#242424")
        self.actualizar_frame.grid()

        self.actualizar_label = ctk.CTkTextbox(
            self.actualizar_frame, fg_color="#242424", width=600, activate_scrollbars=False)
        self.actualizar_label.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 0))

        self.actualizar_label.insert(
            index="0.0", text="Si es tu primera vez instalando la aplicacion presiona continuar.\nSi ya habias descargado antes la aplicacion se conservaran las contraseñas que has guardado.\nSi antes instalaste la aplicacion en la ubicacion predeterminada presiona continuar.\nSi instalaste la aplicacion en otra ubicacion seleccionala a continuacion.")
        self.actualizar_label.configure(state="disabled")

        self.actualizar_entry = ctk.CTkEntry(
            self.actualizar_frame,  fg_color="#242424", border_color="#2b2b2b", border_width=1, width=400)
        self.actualizar_entry.grid(
            row=0, column=0, padx=(0, 170), pady=(0, 0))

        self.actualizar_entry.insert(
            0, self.ubicacion_database)

        self.continuar_button = ctk.CTkButton(
            self.actualizar_frame, text="Seleccionar ubicacion", fg_color="#242424", hover_color="#2b2b2b", command=self.seleccionar_ubicacion_db, width=100)
        self.continuar_button.grid(
            row=0, column=0, padx=(410, 0), pady=(0, 0))

        self.continuar_button_cont_button = ctk.CTkButton(
            self.actualizar_frame, text="Continuar", fg_color="#242424", hover_color="#2b2b2b", command=self.encriptacion, width=100)
        self.continuar_button_cont_button.grid(
            row=1, column=0, padx=(420, 0), pady=(150, 0))

        self.regresar_button = ctk.CTkButton(
            self.actualizar_frame, text="Regresar", fg_color="#242424", hover_color="#2b2b2b", command=self.ubicacion, width=100)
        self.regresar_button.grid(
            row=1, column=0, padx=(0, 450), pady=(150, 0))

    def radiobutton_event(self):
        print("radiobutton toggled, current value:", self.radio_var.get())

    def encriptacion(self):
        self.actualizar_frame.destroy()
        self.count1 = self.count1 + 1
        

        if self.count2 >= 2:
            self.count2 = self.count2

        else:

            if self.count1 >= 2:
                self.count2 = 1

        if self.count2 >= 2:
            self.instalar_frame.destroy()


        self.encriptacion_frame = ctk.CTkFrame(
            self.ventana, width=600, height=600, fg_color="#242424")
        self.encriptacion_frame.grid()

        self.radio_var = tk.IntVar(value=0)

        self.encriptacion_label = ctk.CTkTextbox(
            self.encriptacion_frame, fg_color="#242424", width=600, activate_scrollbars=False)
        self.encriptacion_label.grid(
            row=0, column=0, padx=(10, 0), pady=(0, 60))

        self.encriptacion_label.insert(
            index="0.0", text="La nueva version del administrador de contraseñas ofrece un nuevo y mas seguro metodo de cifrado,\nlo que mantiene tus contraseñas mas seguras.\nEs recomendable actualizar a este nuevo metodo de cifrado, pero si lo deseas puedes seguir usando \nel metodo antigüo.")
        self.encriptacion_label.configure(state="disabled")

        self.new_encryption = ctk.CTkRadioButton(self.encriptacion_frame,command=self.radiobutton_event ,border_width_unchecked=2 ,radiobutton_width=8,variable= self.radio_var,value=1 ,radiobutton_height=8 ,  width=100, height=4,text="Nuevo metodo de cifrado (recomendado)")
        self.new_encryption.grid(row=0, column=0, padx=(0, 250), pady=(0, 0))

        self.new_encryption_desc = ctk.CTkTextbox(self.encriptacion_frame, fg_color="#242424", width=400, height=50 ,activate_scrollbars=False)
        self.new_encryption_desc.grid(row=0, column=0, padx=(0, 100), pady=(80, 0))

        self.new_encryption_desc.insert(index="0.0", text="El nuevo metodo usa cifrado asimetrico para incrementar la\nseguridad a la hora de guardar y acceder a tus contraseñas.")
        self.new_encryption_desc.configure(state="disabled")


        self.old_encryption = ctk.CTkRadioButton(self.encriptacion_frame,command=self.radiobutton_event ,border_width_unchecked=2 ,radiobutton_width=8,variable= self.radio_var,value=2 ,radiobutton_height=8 ,  width=100, height=4,text="Antigüo metodo de cifrado")
        self.old_encryption.grid(row=0, column=0, padx=(0, 330), pady=(150, 0))

        self.old_encryption_desc = ctk.CTkTextbox(self.encriptacion_frame, fg_color="#242424", width=400, height=50 ,activate_scrollbars=False)
        self.old_encryption_desc.grid(row=0, column=0, padx=(0, 100), pady=(230, 0))

        self.old_encryption_desc.insert(index="0.0", text="El viejo metodo usa cifrado simetrico lo que limita la \nseguridad a la hora de guardar y acceder a tus contraseñas.")
        self.old_encryption_desc.configure(state="disabled")




        self.continuar_encriptacion_button = ctk.CTkButton(
            self.encriptacion_frame, text="Continuar", fg_color="#242424", hover_color="#2b2b2b", command=self.instalacion, width=100)
        self.continuar_encriptacion_button.grid(
            row=1, column=0, padx=(420, 0), pady=(80, 0))

        self.regresar_encriptacion_button = ctk.CTkButton(
            self.encriptacion_frame, text="Regresar", fg_color="#242424", hover_color="#2b2b2b", command=self.actualizar, width=100)
        self.regresar_encriptacion_button.grid(
            row=1, column=0, padx=(0, 450), pady=(80, 0))

    def instalacion(self):
        self.encriptacion_frame.destroy()

        self.count2 = self.count2 + 1


        self.instalar_frame = ctk.CTkFrame(
            self.ventana, width=600, height=600, fg_color="#242424")
        self.instalar_frame.grid()

        self.instalar_label = ctk.CTkTextbox(
            self.instalar_frame, fg_color="#242424", width=600, activate_scrollbars=False)
        self.instalar_label.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 0))

        self.instalar_label.insert(
            index="0.0", text="Presiona instalar para comenzar con la instalacion.")
        self.instalar_label.configure(state="disabled")

        self.instalar_progreso = ctk.CTkProgressBar(
            self.instalar_frame,  fg_color="#242424", border_color="#2b2b2b", progress_color="Green", border_width=1, width=500)

        self.progreso_label = ctk.CTkTextbox(
            self.instalar_frame, fg_color="#242424", width=100, height=5, activate_scrollbars=False)
        self.progreso_label.grid(
            row=0, column=0, padx=(0, 430), pady=(0, 40))

        # Botón de instalación
        self.boton_instalar = ctk.CTkButton(
            self.instalar_frame, text="Instalar", fg_color="#242424", hover_color="#2b2b2b", width=100, command=self.instalar)
        self.boton_instalar.grid(row=1, column=0, padx=(420, 0), pady=(150, 0))

        self.regresar_1_button = ctk.CTkButton(
            self.instalar_frame, text="Regresar", fg_color="#242424", hover_color="#2b2b2b", width=100, command= self.encriptacion)
        self.regresar_1_button.grid(
            row=1, column=0, padx=(0, 450), pady=(150, 0))

    def exito(self):
        self.instalar_frame.destroy()

        self.exito_frame = ctk.CTkFrame(self.ventana, width=600, height=600, fg_color="#242424")
        self.exito_frame.grid()

        self.exito_label = ctk.CTkTextbox(
            self.exito_frame, fg_color="#242424", width=600, activate_scrollbars=False)
        self.exito_label.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 0))

        self.exito_label.insert(
            index="0.0", text="Instalacion completada con exito.")
        self.exito_label.configure(state="disabled")

        self.close_button = ctk.CTkButton(
            self.exito_frame, text="Terminar", fg_color="#242424", hover_color="#2b2b2b", width=100, command= self.ventana.destroy)
        self.close_button.grid(
            row=1, column=0, padx=(420, 0), pady=(150, 0))

    def variable_entorno(self):

        # Ruta al Registro del sistema
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
        ENVIRONMENT_PATH = r"Environment"

        # Nombre y valor de la variable de entorno
        public_db_key = "Public_db_key"
        public_db_key_value = f"{public_key_pem.decode()}"

        # Nombre y valor de la variable de entorno
        private_db_key = "Private_db_key"
        private_db_key_value = f"{private_key_pem.decode()}"

        # Nombre y valor de la variable de entorno
        public_table_key = "Public_table_key"
        public_table_key_value = f"{public_key1_pem.decode()}"

        # Nombre y valor de la variable de entorno
        private_table_key = "Private_table_key"
        private_table_key_value = f"{private_key1_pem.decode()}"

        # Abrir la clave del Registro del sistema correspondiente a las variables de entorno
        clave_reg = winreg.OpenKey(
            HKEY_CURRENT_USER, ENVIRONMENT_PATH, 0, winreg.KEY_ALL_ACCESS)

        # Establecer el valor de la variable de entorno
        winreg.SetValueEx(clave_reg, public_db_key, 0,
                          winreg.REG_EXPAND_SZ, public_db_key_value)

        winreg.SetValueEx(clave_reg, private_db_key, 0,
                          winreg.REG_EXPAND_SZ, private_db_key_value)

        winreg.SetValueEx(clave_reg, public_table_key, 0,
                          winreg.REG_EXPAND_SZ, public_table_key_value)

        winreg.SetValueEx(clave_reg, private_table_key, 0,
                          winreg.REG_EXPAND_SZ, private_table_key_value)

        # Actualizar el entorno del proceso actual
        os.environ[public_db_key] = public_db_key_value
        os.environ[private_db_key] = private_db_key_value
        os.environ[public_table_key] = public_table_key_value
        os.environ[private_table_key] = private_table_key_value

        # Cerrar la clave del Registro del sistema
        winreg.CloseKey(clave_reg)


# Crear la ventana principal
ventana = ctk.CTk()

# Crear la instancia de la aplicación
app = InstalacionApp(ventana)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
