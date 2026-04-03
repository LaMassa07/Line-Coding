import tkinter as tk

bits = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
H = 0
r = 0
p1 = 0
p0 = 0

window = tk.Tk()
window.title("Data and Characteristics")
window.geometry("420x300")
window.configure(bg="#f4f6fb")

main = tk.Frame(window, padx=20, pady=20, bg="#f4f6fb")
main.pack(fill="both", expand=True)

# Titolo
title = tk.Label(
    main,
    text="Signal Statistics",
    font=("Segoe UI", 20, "bold"),
    bg="#f4f6fb"
)
title.pack(pady=(0,15))


# -------- BITS --------
bits_frame = tk.LabelFrame(
    main,
    text="Bits",
    font=("Segoe UI", 11, "bold"),
    padx=10,
    pady=10
)
bits_frame.pack(fill="x", pady=5)

bits_label = tk.Label(
    bits_frame,
    text=str(bits),
    font=("Consolas", 14),
    anchor="w"
)
bits_label.pack(fill="x")


# -------- PROBABILITIES --------
prob_frame = tk.LabelFrame(
    main,
    text="Probabilities",
    font=("Segoe UI", 11, "bold"),
    padx=10,
    pady=10
)
prob_frame.pack(fill="x", pady=5)

tk.Label(prob_frame, text="p(0):", font=("Consolas", 13)).grid(row=0, column=0, sticky="w")
tk.Label(prob_frame, text=f"{p0:.3f}", font=("Consolas", 13)).grid(row=0, column=1, sticky="e")

tk.Label(prob_frame, text="p(1):", font=("Consolas", 13)).grid(row=1, column=0, sticky="w")
tk.Label(prob_frame, text=f"{p1:.3f}", font=("Consolas", 13)).grid(row=1, column=1, sticky="e")


# -------- INFORMATION --------
info_frame = tk.LabelFrame(
    main,
    text="Information",
    font=("Segoe UI", 11, "bold"),
    padx=10,
    pady=10
)
info_frame.pack(fill="x", pady=5)

tk.Label(info_frame, text="Entropy H:", font=("Consolas", 13)).grid(row=0, column=0, sticky="w")
tk.Label(info_frame, text=f"{H:.4f}", font=("Consolas", 13)).grid(row=0, column=1, sticky="e")

tk.Label(info_frame, text="Redundancy r:", font=("Consolas", 13)).grid(row=1, column=0, sticky="w")
tk.Label(info_frame, text=f"{r:.4f}", font=("Consolas", 13)).grid(row=1, column=1, sticky="e")

window.mainloop()