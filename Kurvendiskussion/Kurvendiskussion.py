import numpy as np
import matplotlib.pyplot as plt

# Definiere die Funktion
def f(x):
    return x**3 - 3*x**2 + 1

# Definiere die Ableitung der Funktion
def f_prime(x):
    return 3*x**2 - 6*x

# Definiere den Definitionsbereich der Funktion
x = np.linspace(-2, 4, 400)

# Berechne die Funktionswerte und Ableitungswerte für jeden x-Wert
y = f(x)
y_prime = f_prime(x)

# Plotte die Funktion und ihre Ableitung
plt.figure(figsize=(10, 6))

# Funktion
plt.plot(x, y, label='f(x) = $x^3 - 3x^2 + 1$')

# Ableitung
plt.plot(x, y_prime, label="f'(x) = $3x^2 - 6x$", linestyle='dashed')

# Markiere die Nullstellen der Ableitung (Extremstellen der Funktion)
roots = np.roots([3, -6])
plt.scatter(roots, f(roots), color='red', marker='o', label='Extremstellen')

# Markiere die Wendepunkte der Funktion (Nullstellen der zweiten Ableitung)
second_derivative = np.polyder([3, -6])
inflection_points = np.roots(second_derivative)
plt.scatter(inflection_points, f(inflection_points), color='green', marker='o', label='Wendepunkte')

plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)

plt.legend()
plt.title('Kurvendiskussion')
plt.xlabel('x-Achse')
plt.ylabel('y-Achse')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.show()
