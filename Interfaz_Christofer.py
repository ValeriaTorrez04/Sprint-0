import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# ---------- Conexión a BD ----------
def conectar_bd():
    try:
        return mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10822167",
            password="9mPm8WpZUY",
            database="sql10822167",
            port=3306
        )
    except Exception as e:
        return None

# ---------- Funciones Lógicas ----------
def guardar():
    nombre = entry_nombre.get().strip()
    costo = entry_costo.get().strip()
    tiempo = entry_tiempo.get().strip()
    
    if not nombre or not costo or not tiempo:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return
    
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO recetas (nombre, costo, tiempo) VALUES (%s, %s, %s)",
                           (nombre, float(costo), float(tiempo)))
            conn.commit()
            messagebox.showinfo("Éxito", f"'{nombre}' registrada correctamente")
            limpiar()
            mostrar()
        except Exception as e:
            messagebox.showerror("Error", "No se pudo guardar (Posible nombre duplicado)")
        finally:
            conn.close()

def mostrar():
    for row in tabla.get_children():
        tabla.delete(row)
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, costo, tiempo FROM recetas")
        for fila in cursor.fetchall():
            tabla.insert("", "end", values=fila)
        conn.close()

def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_costo.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)

# ---------- Interfaz de Alto Impacto ----------
ventana = tk.Tk()
ventana.title("Sprint 0 - Christofer (Red Style)")
ventana.geometry("700x550")
ventana.configure(bg='#000000') # Fondo Negro Puro

# Encabezado Neutro
tk.Label(ventana, text="SISTEMA DE GESTIÓN DE RECETAS", font=("Impact", 20), 
         fg="#FF0000", bg='#000000').pack(pady=20)
# Contenedor de Formulario
frame_inputs = tk.Frame(ventana, bg='#000000')
frame_inputs.pack(pady=10)

# Estilos de etiquetas y entradas
estilo_label = {"bg": "#000000", "fg": "#FFFFFF", "font": ("Arial", 10, "bold")}
estilo_entry = {"bg": "#1A1A1A", "fg": "#FFFFFF", "insertbackground": "red", "relief": "flat"}

tk.Label(frame_inputs, text="NOMBRE DE LA RECETA", **estilo_label).grid(row=0, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(frame_inputs, width=35, **estilo_entry)
entry_nombre.grid(row=0, column=1, pady=5)

tk.Label(frame_inputs, text="COSTO ($)", **estilo_label).grid(row=1, column=0, padx=10, pady=5)
entry_costo = tk.Entry(frame_inputs, width=35, **estilo_entry)
entry_costo.grid(row=1, column=1, pady=5)

tk.Label(frame_inputs, text="TIEMPO (MIN)", **estilo_label).grid(row=2, column=0, padx=10, pady=5)
entry_tiempo = tk.Entry(frame_inputs, width=35, **estilo_entry)
entry_tiempo.grid(row=2, column=1, pady=5)

# Botones
btn_guardar = tk.Button(ventana, text="GUARDAR RECETA", command=guardar, 
                        bg="#FF0000", fg="#FFFFFF", font=("Arial", 10, "bold"), 
                        relief="flat", width=25, cursor="hand2")
btn_guardar.pack(pady=20)

# Estilo de la Tabla (Treeview)
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#1A1A1A", foreground="white", fieldbackground="#1A1A1A", borderwidth=0)
style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Arial", 10, "bold"))
style.map("Treeview", background=[('selected', '#FF0000')]) # Fila seleccionada en Rojo

tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Costo", "Tiempo"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="NOMBRE")
tabla.heading("Costo", text="COSTO")
tabla.heading("Tiempo", text="TIEMPO")
tabla.column("ID", width=50, anchor="center")
tabla.pack(fill="both", expand=True, padx=20, pady=10)

mostrar()
ventana.mainloop()