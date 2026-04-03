import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# -------------------------
# CONEXIÓN A MYSQL
# -------------------------
conexion = mysql.connector.connect(
    host="sql10.freesqldatabase.com",
    user="sql10822167",
    password="9mPm8WpZUY",
    database="sql10822167",
    port=3306
)

cursor = conexion.cursor()

# -------------------------
# FUNCIONES
# -------------------------
def guardar():
    nombre = entry_nombre.get().strip()
    costo = entry_costo.get().strip()
    tiempo = entry_tiempo.get().strip()

    if nombre == "" or costo == "" or tiempo == "":
        messagebox.showwarning("Error", "Complete todos los campos")
        return

    try:
        cursor.execute(
            "INSERT INTO recetas (nombre, costo, tiempo) VALUES (%s, %s, %s)",
            (nombre, float(costo), float(tiempo))
        )
        conexion.commit()

        messagebox.showinfo("Éxito", "Receta guardada")
        limpiar()
        mostrar_datos()

    except:
        messagebox.showerror("Error", "La receta ya existe o datos inválidos")


def eliminar():
    seleccionado = tabla.selection()

    if not seleccionado:
        messagebox.showwarning("Error", "Seleccione una receta")
        return

    item = tabla.item(seleccionado)
    id_receta = item["values"][0]

    cursor.execute("DELETE FROM recetas WHERE id=%s", (id_receta,))
    conexion.commit()

    mostrar_datos()


def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_costo.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)


def mostrar_datos():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT * FROM recetas")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)


# -------------------------
# VENTANA DE COMPARACIÓN
# -------------------------
def ventana_comparacion():
    nueva = tk.Toplevel()
    nueva.title("Comparación de Recetas")
    nueva.geometry("400x350")

    tiempo_base = 5

    tk.Label(nueva, text="Receta base: Sándwich", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(nueva, text=f"Tiempo base: {tiempo_base} minutos").pack(pady=5)

    tk.Label(nueva, text="Seleccione receta a comparar:").pack(pady=5)

    lista = ttk.Combobox(nueva)

    cursor.execute("SELECT nombre FROM recetas")
    recetas = [fila[0] for fila in cursor.fetchall()]

    lista["values"] = recetas
    lista.pack(pady=5)

    resultado_label = tk.Label(nueva, text="", justify="left")
    resultado_label.pack(pady=10)

    def calcular():
        nombre = lista.get()

        if nombre == "":
            messagebox.showwarning("Error", "Seleccione una receta")
            return

        cursor.execute("SELECT costo, tiempo FROM recetas WHERE nombre=%s", (nombre,))
        dato = cursor.fetchone()

        if dato:
            costo, tiempo = dato
            equivalencia = round(tiempo / tiempo_base)

            resultado = f"""
Receta: {nombre}
Tiempo: {tiempo} min
Costo: {costo}

Equivale a: {equivalencia} sándwich(es)
"""
            resultado_label.config(text=resultado)

    tk.Button(nueva, text="Comparar", command=calcular).pack(pady=5)


# -------------------------
# INTERFAZ
# -------------------------
ventana = tk.Tk()
ventana.title("Sistema de Recetas")
ventana.geometry("500x400")

tk.Label(ventana, text="Nombre Receta").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="Costo").pack()
entry_costo = tk.Entry(ventana)
entry_costo.pack()

tk.Label(ventana, text="Tiempo (min)").pack()
entry_tiempo = tk.Entry(ventana)
entry_tiempo.pack()

tk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)
tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=5)
tk.Button(ventana, text="Comparación", command=ventana_comparacion).pack(pady=5)

tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Costo", "Tiempo"), show="headings")

tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Costo", text="Costo")
tabla.heading("Tiempo", text="Tiempo")

tabla.pack(pady=10, fill="both", expand=True)

mostrar_datos()

ventana.mainloop()