import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import scienceplots
from scipy.stats import linregress


plt.style.use(['science', 'nature', 'no-latex'])

# Daten aus der Kalibrierungsdatei lesen
steps = []
avg_weights = []
std_weight = []
std_rel_weight = []
with open('/Users/leahnuss/Desktop/Slurry_Bot/PaperTest/report_cal_id_5_Tue_Jun__4_142036_2024.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        steps.append(float(row['Steps']))
        avg_weights.append(float(row['AVG_weight']))
        std_weight.append(float(row['STD_weight']))
        std_rel_weight.append(float(row['STD_rel_weight']))

# Linearen Fit durchführen
slope, intercept, r_value, _, _ = linregress(steps, avg_weights)
line = slope * np.array(steps) + intercept

# R2-Score berechnen
r2_score = r_value**2

# Plot1
plt.figure(figsize=(3.5, 3.5)) 
plt.errorbar(steps, avg_weights, yerr=std_rel_weight, fmt='o', capsize=5, label='Measured Weights with RSE')  # Fehlerbalken hinzufügen
plt.plot(steps, line, color='red', label=f'Linear Fit (R2 Score: {r2_score:.2f})')  # Linearen Fit hinzufügen
plt.xlabel('Steps [ ]')  # x-Achse mit Einheit
plt.ylabel('Measured Weight [g]')  # y-Achse mit Einheit
plt.title('Calibration Measurement of Hard Carbon')  # Titel des Plots
plt.legend()  # Legende hinzufügen
plt.grid(True)  # Gitter hinzufügen
plt.tight_layout()  # Layout anpassen, um Überlappungen zu vermeiden

# Export Plot
#plt.savefig('CalibrationCurve_plot.svg', format='svg')
plt.savefig('CalibrationCurve_plot.png', format='png')
plt.show()

# Plot2
Percentage = [value * 100 for value in std_rel_weight]
plt.figure(figsize=(3.5, 3.5))
plt.plot(steps, Percentage, label='Relative Standard Error(RSE)')
plt.xlabel('Steps [ ]')  # x-Achse mit Einheit
plt.ylabel('Relative Standard Error [%]')  # y-Achse mit Einheit
plt.title('Relative Standard Error(RSE) for different amount of steps')  # Titel des Plots
plt.legend()  # Legende hinzufügen
plt.grid(True)  # Gitter hinzufügen
plt.tight_layout()  # Layout anpassen, um Überlappungen zu vermeiden

# Export Plot
#plt.savefig('Error_plot.svg', format='svg')
plt.savefig('Error_plot.png', format='png')

# Anzeigen
plt.show()
