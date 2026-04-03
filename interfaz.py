import tkinter as tk
from tkinter import messagebox
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10822167",
        password="9mPm8WpZUY",
        database="sql10822167",
        port=3306
    )

def guardar_receta():
    nombre = entry_nombre.get()
    costo = entry_costo.get()
    tiempo = entry_tiempo.get()

    if not nombre or not costo or not tiempo:
        messagebox.showwarning("Aviso", "Completa todos los campos")
        return

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO recetas (nombre, costo, tiempo) VALUES (%s, %s, %s)",
                       (nombre, float(costo), float(tiempo)))
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Éxito", "Receta guardada correctamente")
        entry_nombre.delete(0, tk.END)
        entry_costo.delete(0, tk.END)
        entry_tiempo.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

# Ventana principal
ventana = tk.Tk()
ventana.title("Registro de Recetas")
ventana.geometry("350x250")

tk.Label(ventana, text="Nombre:").pack(pady=5)
entry_nombre = tk.Entry(ventana, width=30)
entry_nombre.pack()

tk.Label(ventana, text="Costo:").pack(pady=5)
entry_costo = tk.Entry(ventana, width=30)
entry_costo.pack()

tk.Label(ventana, text="Tiempo (minutos):").pack(pady=5)
entry_tiempo = tk.Entry(ventana, width=30)
entry_tiempo.pack()

tk.Button(ventana, text="Guardar Receta", command=guardar_receta, bg="green", fg="white").pack(pady=15)

ventana.mainloop()
