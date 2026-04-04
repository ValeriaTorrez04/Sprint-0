import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# CONEXIÓN A MYSQL
def get_connection():
    return mysql.connector.connect(
        host               = 'sql10.freesqldatabase.com',
        user               = 'sql10822167',
        password           = '9mPm8WpZUY',
        database           = 'sql10822167',
        port               = 3306,
        connection_timeout = 10
    )

# FUNCIONES CRUD
def llenar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, costo, tiempo FROM recetas ORDER BY tiempo ASC")
    for fila in cursor.fetchall():
        tabla.insert('', 'end', values=fila)
    conn.close()

def agregar():
    nombre = entry_nombre.get()
    costo  = entry_costo.get()
    tiempo = entry_tiempo.get()
    if not nombre or not costo or not tiempo:
        messagebox.showwarning("Atención", "Por favor llena todos los campos.")
        return
    try:
        costo_float  = float(costo)
        tiempo_float = float(tiempo)
    except ValueError:
        messagebox.showerror("Error", "Costo y tiempo deben ser números.")
        return
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recetas (nombre, costo, tiempo) VALUES (%s, %s, %s)",
                       (nombre, costo_float, tiempo_float))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Receta agregada correctamente.")
        limpiar()
        llenar_tabla()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", f"Ya existe una receta con el nombre '{nombre}'.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona una receta para eliminar.")
        return
    fila = tabla.item(seleccion[0])['values']
    id_receta = fila[0]
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recetas WHERE id = %s", (id_receta,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Receta eliminada.")
    llenar_tabla()

def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_costo.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)

# INTERFAZ GRÁFICA
root = tk.Tk()
root.title("Recetas de Cocina")
root.geometry("700x520")
root.configure(bg='#f0f0f0')
root.resizable(True, True)

tk.Label(root, text="INGRESE LA RECETA",
         font=("Stencil", 20, "bold"),
         bg='#f0f0f0').pack(pady=15)

frame_campos = tk.Frame(root, bg='#f0f0f0')
frame_campos.pack(pady=5)

tk.Label(frame_campos, text="Nombre:",
         font=("Serif", 14), bg='#f0f0f0').grid(row=0, column=0, padx=10)
entry_nombre = tk.Entry(frame_campos, font=("Serif", 14), width=22)
entry_nombre.grid(row=0, column=1, padx=10)

tk.Label(frame_campos, text="Costo ($):",
         font=("Serif", 14), bg='#f0f0f0').grid(row=0, column=2, padx=10)
entry_costo = tk.Entry(frame_campos, font=("Serif", 14), width=12)
entry_costo.grid(row=0, column=3, padx=10)

tk.Label(frame_campos, text="Tiempo (min):",
         font=("Serif", 14), bg='#f0f0f0').grid(row=0, column=4, padx=10)
entry_tiempo = tk.Entry(frame_campos, font=("Serif", 14), width=12)
entry_tiempo.grid(row=0, column=5, padx=10)

frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=10, padx=40, fill='both', expand=True)

columnas = ('id', 'Nombre', 'Costo', 'Tiempo')
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=12)

tabla.heading('id',     text='id')
tabla.heading('Nombre', text='Nombre')
tabla.heading('Costo',  text='Costo ($)')
tabla.heading('Tiempo', text='Tiempo (min)')

tabla.column('id',     width=50,  anchor='center')
tabla.column('Nombre', width=250, anchor='center')
tabla.column('Costo',  width=120, anchor='center')
tabla.column('Tiempo', width=130, anchor='center')

style = ttk.Style()
style.configure("Treeview", font=("Serif", 13), rowheight=28)
style.configure("Treeview.Heading", font=("Serif", 13, "bold"))

scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=tabla.yview)
tabla.configure(yscroll=scrollbar.set)
scrollbar.pack(side='right', fill='y')
tabla.pack(fill='both', expand=True)

frame_btns = tk.Frame(root, bg='#f0f0f0')
frame_btns.pack(pady=10)

tk.Button(frame_btns, text="Agregar",
          font=("Serif", 14), width=12,
          bg='#4CAF50', fg='white',
          command=agregar).grid(row=0, column=0, padx=40)

tk.Button(frame_btns, text="Eliminar",
          font=("Serif", 14), width=12,
          bg='#f44336', fg='white',
          command=eliminar).grid(row=0, column=1, padx=40)

llenar_tabla()
root.mainloop()
