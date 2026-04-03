import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

print("Iniciando programa...")

# ---------- Conexión a BD ----------
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10822167",
            password="9mPm8WpZUY",
            database="sql10822167",
            port=3306
        )
        print("Conexión exitosa a BD")
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None

def crear_tabla():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recetas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE,
                costo DECIMAL(10,2),
                tiempo DECIMAL(10,2)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabla verificada/creada")

# ---------- Funciones de la app ----------
def guardar():
    nombre = entry_nombre.get().strip()
    costo = entry_costo.get().strip()
    tiempo = entry_tiempo.get().strip()
    
    if not nombre or not costo or not tiempo:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos")
        return
    
    try:
        costo = float(costo)
        tiempo = float(tiempo)
    except:
        messagebox.showerror("Error", "Costo y tiempo deben ser números")
        return
    
    conn = conectar_bd()
    if not conn:
        messagebox.showerror("Error", "No se pudo conectar a la BD")
        return
    
    cursor = conn.cursor()
    # Verificar duplicado
    cursor.execute("SELECT * FROM recetas WHERE nombre = %s", (nombre,))
    if cursor.fetchone():
        messagebox.showerror("Error", f"La receta '{nombre}' ya existe")
        cursor.close()
        conn.close()
        return
    
    cursor.execute("INSERT INTO recetas (nombre, costo, tiempo) VALUES (%s, %s, %s)",
                   (nombre, costo, tiempo))
    conn.commit()
    cursor.close()
    conn.close()
    
    messagebox.showinfo("Éxito", f"Receta '{nombre}' guardada en BD compartida")
    limpiar_campos()
    mostrar_recetas()

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_costo.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)

def mostrar_recetas():
    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)
    
    conn = conectar_bd()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, costo, tiempo FROM recetas ORDER BY id")
    datos = cursor.fetchall()
    
    for i, (nombre, costo, tiempo) in enumerate(datos, start=1):
        tabla.insert("", "end", values=(i, nombre, f"${costo}", f"{tiempo} min"))
    
    cursor.close()
    conn.close()
    lbl_estado.config(text=f"Total recetas: {len(datos)}")

def eliminar():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Seleccionar", "Selecciona una receta de la tabla")
        return
    
    nombre = tabla.item(seleccion)["values"][1]
    if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}' de la BD compartida?"):
        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recetas WHERE nombre = %s", (nombre,))
            conn.commit()
            cursor.close()
            conn.close()
            mostrar_recetas()
            messagebox.showinfo("Eliminado", "Receta eliminada correctamente")

# ---------- Construcción de la interfaz ----------
print("Creando ventana principal...")
ventana = tk.Tk()
ventana.title("Sistema de Recetas - BD Compartida")
ventana.geometry("700x450")
ventana.configure(bg='white')

# Forzar que la ventana se muestre arriba
ventana.lift()
ventana.attributes('-topmost', True)
ventana.after(100, lambda: ventana.attributes('-topmost', False))

# Título
tk.Label(ventana, text="🍽️ SISTEMA DE RECETAS (BD COMPARTIDA)", 
         font=("Arial", 14, "bold"), fg="blue", bg='white').pack(pady=10)

lbl_estado = tk.Label(ventana, text="Conectando...", font=("Arial", 9), bg='white')
lbl_estado.pack()

# Frame de entrada
frame = tk.Frame(ventana, bg='white')
frame.pack(pady=10)

tk.Label(frame, text="Nombre:", bg='white').grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame, width=30)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Costo ($):", bg='white').grid(row=1, column=0, padx=5, pady=5)
entry_costo = tk.Entry(frame, width=30)
entry_costo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Tiempo (min):", bg='white').grid(row=2, column=0, padx=5, pady=5)
entry_tiempo = tk.Entry(frame, width=30)
entry_tiempo.grid(row=2, column=1, padx=5, pady=5)

# Botones
frame_botones = tk.Frame(ventana, bg='white')
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="💾 GUARDAR", command=guardar, 
          bg="green", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="🗑️ ELIMINAR", command=eliminar, 
          bg="red", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="🔄 ACTUALIZAR", command=mostrar_recetas, 
          bg="blue", fg="white", width=12).pack(side=tk.LEFT, padx=5)

# Tabla
tabla = ttk.Treeview(ventana, columns=("#", "Nombre", "Costo", "Tiempo"), show="headings", height=12)
tabla.heading("#", text="#")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Costo", text="Costo")
tabla.heading("Tiempo", text="Tiempo")
tabla.column("#", width=50, anchor="center")
tabla.column("Nombre", width=250)
tabla.column("Costo", width=100, anchor="center")
tabla.column("Tiempo", width=100, anchor="center")
tabla.pack(pady=10, fill="both", expand=True)

# Pie
tk.Label(ventana, text="📡 Datos compartidos con todo el grupo", 
         font=("Arial", 8), bg='white', fg="gray").pack()

# Inicializar
crear_tabla()
mostrar_recetas()

print("Ventana lista, iniciando mainloop...")
ventana.mainloop()
print("Programa terminado")