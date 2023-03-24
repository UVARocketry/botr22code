import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()
root.geometry("800x600")

fig1 = Figure(figsize=(5, 4), dpi=100)
ax1 = fig1.add_subplot(111)
ax1.plot([1, 2, 3, 4, 5], [10, 15, 13, 17, 20], 'r')

fig2 = Figure(figsize=(5, 4), dpi=100)
ax2 = fig2.add_subplot(111)
ax2.plot([1, 2, 3, 4, 5], [5, 9, 8, 6, 10], 'b')

fig3 = Figure(figsize=(5, 4), dpi=100)
ax3 = fig3.add_subplot(111)
ax3.plot([1, 2, 3, 4, 5], [2, 4, 3, 1, 5], 'g')

fig4 = Figure(figsize=(5, 4), dpi=100)
ax4 = fig4.add_subplot(111)
ax4.plot([1, 2, 3, 4, 5], [20, 18, 16, 19, 17], 'y')

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()
canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.draw()
canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas4 = FigureCanvasTkAgg(fig4, master=root)
canvas4.draw()
canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()