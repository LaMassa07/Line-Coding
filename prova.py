import tkinter as tk

# crea la finestra principale
window = tk.Tk()
window.title("Finestra di esempio")
window.geometry("300x200")

# crea un testo (label)
label = tk.Label(window, text="Ciao, questo è del testo")
label.pack()

# avvia il loop della finestra
window.mainloop()