import math
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


class CalculadoraGrafica:

  def __init__(self, root):
    self.root = root
    self.root.title("Calculadora Científica Gráfica")
    self.root.geometry("420x550")
    self.root.configure(bg="#202124")

    self.expressao = ""

    # Visor
    self.visor = tk.Entry(
        root,
        font=("Arial", 22),
        bg="#3c4043",
        fg="#ffffff",
        bd=10,
        insertbackground="white",
        justify="right",
    )
    self.visor.grid(
        row=0, column=0, columnspan=7, ipadx=8, ipady=15, padx=10, pady=10
    )

    self.criar_botoes()

  def criar_botoes(self):
    # Layout dos botões adaptado (sem Deg, Rad, x!, Inv e com sinh/cosh)
    botoes = [
        ("sinh", 1, 0),
        ("cosh", 1, 1),
        ("(", 1, 2),
        (")", 1, 3),
        ("%", 1, 4),
        ("AC", 1, 5),
        ("sin", 2, 0),
        ("ln", 2, 1),
        ("7", 2, 2),
        ("8", 2, 3),
        ("9", 2, 4),
        ("÷", 2, 5),
        ("cos", 3, 0),
        ("log", 3, 1),
        ("4", 3, 2),
        ("5", 3, 3),
        ("6", 3, 4),
        ("×", 3, 5),
        ("tan", 4, 0),
        ("√", 4, 1),
        ("1", 4, 2),
        ("2", 4, 3),
        ("3", 4, 4),
        ("-", 4, 5),
        ("π", 5, 0),
        ("e", 5, 1),
        ("0", 5, 2),
        (".", 5, 3),
        ("=", 5, 4),
        ("+", 5, 5),
        ("^", 6, 0),
        ("Plotar", 6, 1),
    ]

    for texto, linha, coluna in botoes:
      colspan = 5 if texto == "Plotar" else 1

      # Estilização de cores
      if texto in ["=", "Plotar"]:
        bg_color = "#8ab4f8"
        fg_color = "#202124"
      elif texto in ["+", "-", "×", "÷", "AC"]:
        bg_color = "#5f6368"
        fg_color = "#ffffff"
      else:
        bg_color = "#3c4043"
        fg_color = "#e8eaed"

      btn = tk.Button(
          self.root,
          text=texto,
          width=5,
          height=2,
          font=("Arial", 11, "bold"),
          bg=bg_color,
          fg=fg_color,
          relief="flat",
          command=lambda t=texto: self.ao_clicar(t),
      )
      btn.grid(
          row=linha,
          column=coluna,
          columnspan=colspan,
          padx=3,
          pady=3,
          sticky="nsew",
      )

  def ao_clicar(self, tecla):
    if tecla == "AC":
      self.expressao = ""
      self.atualizar_visor("")
    elif tecla == "=":
      self.calcular()
    elif tecla == "Plotar":
      self.plotar_grafico()
    else:
      self.expressao += str(tecla)
      self.atualizar_visor(self.expressao)

  def atualizar_visor(self, valor):
    self.visor.delete(0, tk.END)
    self.visor.insert(0, valor)

  def preparar_expressao(self, expr):
    # Substituições para cálculo em Python
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("π", "math.pi").replace("e", "math.e")
    expr = expr.replace("^", "**")
    expr = expr.replace("sin", "math.sin").replace("cos", "math.cos").replace(
        "tan", "math.tan"
    )
    expr = expr.replace("sinh", "math.sinh").replace("cosh", "math.cosh")
    expr = expr.replace("log", "math.log10").replace("ln", "math.log")
    expr = expr.replace("√", "math.sqrt")
    return expr

  def calcular(self):
    try:
      expr_proc = self.preparar_expressao(self.expressao)
      resultado = eval(expr_proc)
      self.expressao = str(resultado)
      self.atualizar_visor(self.expressao)
    except Exception:
      messagebox.showerror("Erro", "Expressão Inválida")

  def plotar_grafico(self):
    expr_original = self.visor.get()
    if not expr_original:
      return

    # Intervalo x de 0 a 2*pi (conforme a imagem do quadro)
    x = np.linspace(0, 2 * np.pi, 500)

    try:
      # Avalia a função ao longo do vetor x
      y = eval(
          expr_original.replace("sin", "np.sin")
          .replace("cos", "np.cos")
          .replace("tan", "np.tan")
          .replace("sinh", "np.sinh")
          .replace("cosh", "np.cosh")
          .replace("π", "np.pi")
          .replace("^", "**")
      )

      plt.figure(figsize=(7, 5))
      plt.plot(x, y, label=f"y = {expr_original}", color="#1f77b4", linewidth=2)

      # Destaque para x = pi/4 (exemplo do quadro)
      x_ponto = np.pi / 4
      y_ponto = float(
          eval(
              expr_original.replace("sin", "np.sin")
              .replace("cos", "np.cos")
              .replace("sinh", "np.sinh")
              .replace("cosh", "np.cosh")
              .replace("π", "np.pi")
              .replace("^", "**"),
              {"x": x_ponto, "np": np},
          )
      )

      # Ponto no gráfico (pi/4, y)
      plt.plot(x_ponto, y_ponto, "ro")
      plt.vlines(
          x=x_ponto,
          ymin=0,
          ymax=y_ponto,
          colors="gray",
          linestyles="dashed",
      )
      plt.text(
          x_ponto + 0.1,
          y_ponto,
          f"(π/4, {y_ponto:.3f})",
          fontsize=10,
          color="black",
      )

      # Estilização dos eixos conforme a imagem do quadro
      plt.axhline(0, color="black", linewidth=1)
      plt.axvline(0, color="black", linewidth=1)
      plt.xticks(
          [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
          ["0", "π/2", "π", "3π/2", "2π"],
      )
      plt.title("Gráfico da Função")
      plt.xlabel("x")
      plt.ylabel("y")
      plt.grid(True, linestyle=":", alpha=0.6)
      plt.legend()
      plt.show()

    except Exception as e:
      messagebox.showerror("Erro", f"Não foi possível plotar a função:\n{e}")


if __name__ == "__main__":
  root = tk.Tk()
  app = CalculadoraGrafica(root)
  root.mainloop()
