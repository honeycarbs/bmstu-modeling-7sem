import tkinter
from turtle import color

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


from probability.gaussian import Gaussian
from probability.uniform import Uniform

import numpy as np


def buildGaussian():
    try:
        mu = mu_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле µ.")
        return
    
    try:
        sigma = sigma_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле σ².")
        return
    
    if sigma <= 0.0:
        tkinter.messagebox.showerror("Ошибка", "σ² не может быть отрицательным.")
        return

    try:
        upper = upperGaussian_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле верхней границы.")
        return

    try:
        lower = lowerGaussian_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле нижней границы.")
        return

    g = Gaussian(mu, sigma)
    xs = np.arange(lower, upper, .1)
    ysPDFGaussian = []
    ysCDFGaussian = []
    for x in xs:
        ysPDFGaussian.append(g.PDF(x))
        ysCDFGaussian.append(g.CDF(x))

    axCDFGaussian.set_xlim([lower, upper])
    axCDFGaussian.set_ylim([-0.1, 1.1])

    axPDFGaussian.set_xlim([lower, upper])
    axPDFGaussian.set_ylim([-0.1, 1.1])

    linePDFGaussian.set_data(xs, ysPDFGaussian)
    lineCDFGaussian.set_data(xs, ysCDFGaussian)

    canvasPDFGaussian.draw()
    canvasCDFGaussian.draw()


def buildUniform():
    try:
        minv = min_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле a.")
        return
    
    try:
        maxv = max_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле b.")
        return

    print(f'{minv} <= {maxv} - {minv <= maxv}')
    
    if maxv <= minv:
        tkinter.messagebox.showerror("Ошибка", "a должно быть меньше b.")
        return

    try:
        upper = upperUniform_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле верхней границы.")
        return

    try:
        lower = lowerUniform_field.get()
    except tkinter.TclError:
        tkinter.messagebox.showerror("Ошибка", "Неверно заполнено поле нижней границы.")
        return

    u = Uniform(minv, maxv)
    xs = np.arange(lower, upper, .1)
    ysPDFUniform = []
    ysCDFUniform = []
    for x in xs:
        ysPDFUniform.append(u.PDF(x))
        ysCDFUniform.append(u.CDF(x))

    axCDFUniform.set_xlim([lower, upper])
    axCDFUniform.set_ylim([-0.1, 1.1])

    axPDFUniform.set_xlim([lower, upper])
    axPDFUniform.set_ylim([-0.1, 1.1])

    linePDFUniform.set_data(xs, ysPDFUniform)
    lineCDFUniform.set_data(xs, ysCDFUniform)

    canvasPDFUniform.draw()
    canvasCDFUniform.draw()

root = tkinter.Tk()
root.wm_title("Лабораторная работа 1")

figCDFGaussian = Figure(figsize=(5, 4), dpi=100)
figPDFGaussian = Figure(figsize=(5, 4), dpi=100)

figCDFUniform = Figure(figsize=(5, 4), dpi=100)
figPDFUniform = Figure(figsize=(5, 4), dpi=100)

xs = np.arange(-5, 5, .1)

u = Uniform(-2, 2)
ysPDFUniform = []
ysCDFUniform = []

g = Gaussian(0, 1)
ysPDFGaussian = []
ysCDFGaussian = []

for x in xs:
    ysPDFGaussian.append(g.PDF(x))
    ysCDFGaussian.append(g.CDF(x))

    ysPDFUniform.append(u.PDF(x))
    ysCDFUniform.append(u.CDF(x))

axCDFGaussian = figCDFGaussian.add_subplot()
lineCDFGaussian, = axCDFGaussian.plot(xs, ysCDFGaussian, color='xkcd:mauve')

axPDFGaussian = figPDFGaussian.add_subplot()
linePDFGaussian, = axPDFGaussian.plot(xs, ysPDFGaussian, color='xkcd:avocado')

axCDFGaussian.set_xlim([-5, 5])
axCDFGaussian.set_ylim([-0.1, 1.1])

axPDFGaussian.set_xlim([-5, 5])
axPDFGaussian.set_ylim([-0.1, 1.1])

axCDFGaussian.set_xlabel("X")
axCDFGaussian.set_ylabel("F(x)")
axCDFGaussian.grid(visible=True,color='xkcd:light grey')

axPDFGaussian.set_xlabel("X")
axPDFGaussian.set_ylabel("f(x)")
axPDFGaussian.grid(visible=True,color='xkcd:light grey')

canvasPDFGaussian = FigureCanvasTkAgg(figPDFGaussian, master=root)  # A tk.DrawingArea.
canvasPDFGaussian.draw()

canvasCDFGaussian = FigureCanvasTkAgg(figCDFGaussian, master=root)  # A tk.DrawingArea.
canvasCDFGaussian.draw()

toolbarCDFGaussian = NavigationToolbar2Tk(canvasCDFGaussian, root, pack_toolbar=False)
toolbarCDFGaussian.update()

toolbarPDFGaussian = NavigationToolbar2Tk(canvasPDFGaussian, root, pack_toolbar=False)
toolbarPDFGaussian.update()

axCDFUniform = figCDFUniform.add_subplot()
lineCDFUniform, = axCDFUniform.plot(xs, ysCDFUniform, 
                                    color='xkcd:greyish purple')

axPDFUniform = figPDFUniform.add_subplot()
linePDFUniform, = axPDFUniform.plot(xs, ysPDFUniform, 
                                    color='xkcd:yellow orange')

axCDFUniform.set_xlim([-5, 5])
axCDFUniform.set_ylim([-0.1, 1.1])
axPDFUniform.set_xlim([-5, 5])
axPDFUniform.set_ylim([-0.1, 1.1])

axCDFUniform.grid(visible=True,color='xkcd:light grey')

axCDFUniform.set_xlabel("X")
axCDFUniform.set_ylabel("F(x)")

axPDFUniform.set_xlabel("X")
axPDFUniform.set_ylabel("f(x)")
axPDFUniform.grid(visible=True,color='xkcd:light grey')

canvasPDFUniform = FigureCanvasTkAgg(figPDFUniform, master=root)  # A tk.DrawingArea.
canvasPDFUniform.draw()

canvasCDFUniform = FigureCanvasTkAgg(figCDFUniform, master=root)  # A tk.DrawingArea.
canvasCDFUniform.draw()

toolbarCDFUniform = NavigationToolbar2Tk(canvasCDFUniform, root, pack_toolbar=False)
toolbarCDFUniform.update()

toolbarPDFUniform = NavigationToolbar2Tk(canvasPDFUniform, root, pack_toolbar=False)
toolbarPDFUniform.update()


mu_field = tkinter.DoubleVar()
mu_field.set(0.0)

sigma_field = tkinter.DoubleVar()
sigma_field.set(1.0)

min_field = tkinter.DoubleVar()
min_field.set(-2.0)

max_field = tkinter.DoubleVar()
max_field.set(2.0)

lowerGaussian_field = tkinter.DoubleVar()
upperGaussian_field = tkinter.DoubleVar()

lowerGaussian_field.set(-5.0)
upperGaussian_field.set(5.0)

lowerUniform_field = tkinter.DoubleVar()
upperUniform_field = tkinter.DoubleVar()

lowerUniform_field = tkinter.DoubleVar()
upperUniform_field = tkinter.DoubleVar()

lowerUniform_field.set(-5.0)
upperUniform_field.set(5.0)

tkinter.Label(root, text="Нормальное распределение").grid(row=0, column=0, columnspan=6, rowspan=2)
tkinter.Label(root, text="Равномерное распределение").grid(row=0, column=6, columnspan=6, rowspan=2)

tkinter.Label(root, text="µ").grid(row=3, column=3)
tkinter.Label(root, text="σ²").grid(row=4, column=3)

tkinter.Label(root, text="a").grid(row=3, column=9)
tkinter.Label(root, text="b").grid(row=4, column=9)

tkinter.Label(root, text="Нижняя граница интервала").grid(row=5, column=3)
tkinter.Label(root, text="Верхняя граница интервала").grid(row=6, column=3)

tkinter.Label(root, text="Нижняя граница интервала").grid(row=5, column=9)
tkinter.Label(root, text="Верхняя граница интервала").grid(row=6, column=9)

entry_mean = tkinter.Entry(root, textvariable=mu_field).grid(row=3, column=4)
entry_sigma = tkinter.Entry(root, textvariable=sigma_field).grid(row=4, column=4)
entry_lowerGaussian = tkinter.Entry(root, textvariable=lowerGaussian_field).grid(row=5, column=4)
entry_upperGaussian = tkinter.Entry(root, textvariable=upperGaussian_field).grid(row=6, column=4)

entry_min = tkinter.Entry(root, textvariable=min_field).grid(row=3, column=10)
entry_max = tkinter.Entry(root, textvariable=max_field).grid(row=4, column=10)
entry_lowerUniform = tkinter.Entry(root, textvariable=lowerUniform_field).grid(row=5, column=10)
entry_upperUniform = tkinter.Entry(root, textvariable=upperUniform_field).grid(row=6, column=10)

buttonBuildGaussian = tkinter.Button(master=root, text="Построить", command=buildGaussian).grid(row=7, column=3, columnspan=2)

buttonBuildUniform = tkinter.Button(master=root, text="Построить", command=buildUniform).grid(row=7, column=10, columnspan=2)


canvasPDFGaussian.get_tk_widget().grid(row=3, column=0, rowspan= 12, columnspan=3)
toolbarPDFGaussian.grid(row=15, column=0, columnspan=3)
canvasCDFGaussian.get_tk_widget().grid(row=16, column=0, rowspan= 12, columnspan=3)
toolbarCDFGaussian.grid(row=28, column=0, columnspan=3)

canvasPDFUniform.get_tk_widget().grid(row=3, column=6, rowspan= 12, columnspan=3)
toolbarPDFUniform.grid(row=15, column=6, columnspan=3)
canvasCDFUniform.get_tk_widget().grid(row=16, column=6, rowspan= 12, columnspan=3)
toolbarCDFUniform.grid(row=28, column=6, columnspan=3)



tkinter.mainloop()