import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FormUsuarios(tk.Tk):
    def __init__(self, parent):
        self.tipo_action = "Guardar"
        self.tipo_user = ""
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(self.frame, text="Registro de usuarios", font=('Times', 16)).place(x=70, y=30)

        labelcedula = tk.Label(self.frame, text="Cedula", font=('Times', 14))
        labelcedula.place(x=70, y=100)
        self.ccedula = tk.Entry(self.frame, width=40)
        self.ccedula.place(x=220, y=100)

        labelnombre = tk.Label(self.frame, text="Nombre", font=('Times', 14))
        labelnombre.place(x=70, y=130)
        self.cnombre = tk.Entry(self.frame, width=40)
        self.cnombre.place(x=220, y=130)

        labelusuario = tk.Label(self.frame, text="Username", font=('Times', 14))
        labelusuario.place(x=70, y=160)
        self.cusuario = tk.Entry(self.frame, width=40)
        self.cusuario.place(x=220, y=160)

        labelcontrasena = tk.Label(self.frame, text="Contraseña", font=('Times', 14))
        labelcontrasena.place(x=500, y=100)
        self.ccontrasena = tk.Entry(self.frame, width=40, show="*")
        self.ccontrasena.place(x=600, y=100)

        labelcorreo = tk.Label(self.frame, text="Correo", font=('Times', 14))
        labelcorreo.place(x=500, y=130)
        self.ccorreo = tk.Entry(self.frame, width=40)
        self.ccorreo.place(x=600, y=130)

        labeltipo = tk.Label(self.frame, text="Rol", font=('Times', 14))
        labeltipo.place(x=500, y=160)
        self.ctipo = ttk.Combobox(self.frame, width=40)
        self.ctipo.place(x=600, y=160)
        self.ctipo["values"] = ("Administrador", "Vendedor")

        btn_guardar = tk.Button(self.frame, text="Guardar", font=('Times', 14), command=self.guardar_usuario)
        btn_guardar.place(x=70, y=190)

        btn_actualizar = tk.Button(self.frame, text="Actualizar", font=('Times', 14), command=self.actualizar_usuario)
        btn_actualizar.place(x=170, y=580)

        self.listar_usuarios()

    def listar_usuarios(self):
        tk.Label(self.frame, text="LISTADO DE USUARIOS", font=('Times', 16)).place(x=70, y=230)
        
        self.tablausuarios = ttk.Treeview(self.frame, columns=("Nombre", "Username", "Email", "Rol"))
        self.tablausuarios.heading("#0", text="Cedula")
        self.tablausuarios.heading("Nombre", text="Nombre")
        self.tablausuarios.heading("Username", text="Username")
        self.tablausuarios.heading("Email", text="Email")
        self.tablausuarios.heading("Rol", text="Rol")

        self.tablausuarios.bind("<ButtonRelease-1>", self.cargar_datos_usuario)

        try:
            with open(r"E:\LoginAppPart2 (5)\LoginAppPart2\db_users.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for usuarios in data["users"]:
                    self.tablausuarios.insert("", "end", text=f'{usuarios["id"]}', values=(f'{usuarios["name"]}', f'{usuarios["username"]}', f'{usuarios["email"]}', f'{usuarios["role"]}'))
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON")

        self.tablausuarios.place(x=70, y=280)

        btnEliminar = tk.Button(self.frame, text="Eliminar", font=('Times', 14), command=self.eliminar_usuarios)
        btnEliminar.place(x=70, y=550)

    def cargar_datos_usuario(self, event):
        selected_item = self.tablausuarios.selection()
        if not selected_item:
            return
        cedula = self.tablausuarios.item(selected_item)["text"]

        try:
            with open(r"E:\LoginAppPart2 (5)\LoginAppPart2\db_users.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for usuario in data["users"]:
                    if usuario["id"] == cedula:
                        self.ccedula.delete(0, tk.END)
                        self.ccedula.insert(0, usuario["id"])
                        self.cnombre.delete(0, tk.END)
                        self.cnombre.insert(0, usuario["name"])
                        self.cusuario.delete(0, tk.END)
                        self.cusuario.insert(0, usuario["username"])
                        self.ccontrasena.delete(0, tk.END)
                        self.ccontrasena.insert(0, usuario["password"])
                        self.ccorreo.delete(0, tk.END)
                        self.ccorreo.insert(0, usuario["email"])
                        self.ctipo.set(usuario["role"])
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON")

    def guardar_usuario(self):
        cedula = self.ccedula.get()
        nombre = self.cnombre.get()
        usuario = self.cusuario.get()
        contrasena = self.ccontrasena.get()
        correo = self.ccorreo.get()
        rol = self.ctipo.get()

        if not (cedula and nombre and usuario and contrasena and correo and rol):
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        try:
            with open(r"E:\LoginAppPart2 (5)\LoginAppPart2\db_users.json", "r+", encoding="utf-8") as file:
                data = json.load(file)
                nuevo_usuario = {
                    "id": cedula,
                    "name": nombre,
                    "username": usuario,
                    "password": contrasena,
                    "email": correo,
                    "role": rol
                }
                data["users"].append(nuevo_usuario)
                file.seek(0)
                json.dump(data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            self.listar_usuarios()
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON")

    def actualizar_usuario(self):
        cedula = self.ccedula.get()
        nombre = self.cnombre.get()
        usuario = self.cusuario.get()
        contrasena = self.ccontrasena.get()
        correo = self.ccorreo.get()
        rol = self.ctipo.get()

        if not (cedula and nombre and usuario and contrasena and correo and rol):
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        selected_item = self.tablausuarios.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un usuario para actualizar")
            return

        try:
            with open(r"E:\LoginAppPart2 (5)\LoginAppPart2\db_users.json", "r+", encoding="utf-8") as file:
                data = json.load(file)

                for usuario_data in data["users"]:
                    if usuario_data["id"] == cedula:
                        usuario_data["name"] = nombre
                        usuario_data["username"] = usuario
                        usuario_data["password"] = contrasena
                        usuario_data["email"] = correo
                        usuario_data["role"] = rol
                        break

                file.seek(0)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.truncate()

            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            self.listar_usuarios()
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON")

    def eliminar_usuarios(self):
        selected_item = self.tablausuarios.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar")
            return

        cedula = self.tablausuarios.item(selected_item)["text"]

        try:
            with open(r"E:\LoginAppPart2 (5)\LoginAppPart2\db_users.json", "r+", encoding="utf-8") as file:
                data = json.load(file)
                data["users"] = [usuario for usuario in data["users"] if usuario["id"] != cedula]
                file.seek(0)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.truncate()

            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            self.listar_usuarios()
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON")

if __name__ == "__main__":
    app = FormUsuarios(None)
    app.mainloop()
