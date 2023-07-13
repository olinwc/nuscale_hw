import numpy as np
import matplotlib.pyplot as plt

#question_3_part_1

# Ok I guess you don't need scipy or the datetime for this.
# I used VSCode with the latest version of Python available (3.11.4 64-bit) from the Microsoft Store
# Installed numpy and matplotlib via pip

h = 1.20e+5
k_c = 13.0
k_f = 3.60
q_tp = 1.0e+6
l_f = 0.01
l_c = 0.001
T_inf = 350

x_vals = []
y_vals = []

for x in range(0,110):
    x_vals.append(x * 0.0001)

for x in x_vals:
    if x > l_f:
        y = ((q_tp * l_f)*(l_f + l_c - x)/k_c) + (q_tp * l_f)/h + T_inf
        y_vals.append(y)
    else:
        y = (q_tp * l_f * l_f)*(1 - (x * x)/(l_f * l_f))/(2 * k_f) + ((q_tp * l_f * l_c)/k_c) + (q_tp * l_f)/h + T_inf
        y_vals.append(y)

fig, ax = plt.subplots()

ax.scatter(x_vals, y_vals, label='T', c="k", marker='.')
ax.set_xlabel("Distance from Insulation [m]")
ax.set_ylabel("Temperature [degree C]")

plt.show()

fig.savefig("question_3_part1_plot.pdf", format='PDF', bbox_inches='tight')