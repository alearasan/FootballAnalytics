import matplotlib.pyplot as plt

# Definir las listas de datos
cuotas_05 = [1.375, 1.4, 1.4, 1.425, 1.425, 1.45, 1.475, 1.5, 1.5, 1.525, 1.525, 1.575, 1.575, 1.6, 1.65, 1.65, 1.7, 1.775, 1.8, 1.85, 1.9, 1.95, 2.0, 1.975, 2.075, 2.1, 2.2, 2.3, 2.375, 2.425, 2.5, 2.6, 2.675, 2.75, 2.85, 3.3, 3.45, 3.7, 4.1, 4.1]
cuotas_075 = [1.5, 1.525, 1.55, 1.575, 1.6, 1.625, 1.65, 1.725, 1.7, 1.75, 1.8, 1.85, 1.875, 1.9, 2.0, 2.025, 2.075, 2.1, 2.15, 2.2, 2.3, 2.35, 2.4, 2.4, 2.625, 2.625, 2.825, 2.95, 3.2, 3.4, 3.5, 3.5, 3.6, 3.9, 4.15, 4.8, 5.2, 5.4, 6.4, 6.4]
cuotas_10 = [1.8, 1.85, 1.9, 1.975, 2.025, 2.075, 2.1, 2.1, 2.1, 2.250, 2.3, 2.4, 2.4, 2.55, 2.625, 2.825, 2.95, 3.075, 3.2, 3.4, 3.6, 3.8, 4.0, 4.45, 4.8, 5.0, 5.6, 6.6]

# Crear una figura con subgráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Gráfica 1 - Resultados de encontrar_cuota_media_para_ganancia_cero
minutos = list(range(1, 16))
cuotas_necesarias = []  # Debes calcular los valores de cuotas_necesarias
ax1.bar(minutos, cuotas_necesarias, color='b')
ax1.set_xlabel('Minuto')
ax1.set_ylabel('Cuota necesaria')
ax1.set_title('Cuota necesaria para ganancia cero por minuto')

# Gráfica 2 - Cuotas 0.5, 0.75 y 1.0
max_length = max(len(cuotas_05), len(cuotas_075), len(cuotas_10))
ax2.plot(range(1, max_length + 1), cuotas_05, label='Cuotas 0.5')
ax2.plot(range(1, max_length + 1), cuotas_075, label='Cuotas 0.75')
ax2.plot(range(1, max_length + 1), cuotas_10, label='Cuotas 1.0')
ax2.set_xlabel('Minuto')
ax2.set_ylabel('Cuota')
ax2.set_title('Evolución de Cuotas por Minuto')
ax2.legend()

# Ajustar los subgráficos para que no se superpongan
plt.tight_layout()

# Mostrar la figura
plt.show()