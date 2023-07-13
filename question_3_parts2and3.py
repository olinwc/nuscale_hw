import numpy as np
import matplotlib.pyplot as plt
import copy as cp
import csv

# Values will be overridden
T_inf = 350
t = 3.0e-3
num_t_steps = 10000

# list of the timesteps to print the plots and the temperature data for
t_steps_to_print_plot = []

# First row of the CSV file (which must be titled 'user_input.csv') should have three entries
# First is the initial temperature of the entire domain (float)
# Second is the size of the time step to take (float)
# Third is the number of timesteps to take (int)

# The second row can be of any size 1 or larger and is the timesteps to generate temperature plots to print for
# Cannot print 0 because that would just be the initial condition

# Cannot specify a time discretization scheme because the code doesn't really work
# Probably a problem with handling boundary conditions and the fuel-cladding interface
# System does not converge to steady-state solution

with open('user_input.csv') as csvfile:
    reader = csv.reader(csvfile)
    num_rows = 0
    for row in reader:
        if num_rows == 0:
            T_inf = float(row[0])
            print(row[0])
            t = float(row[1])
            print(row[1])
            num_t_steps = int(row[2])
            print(row[2])
        elif num_rows == 1:
            for string in row:
                if int(string) <= 0:
                    print("ERROR: Requested to plot timestep ", int(string), " this is not allowed")
                    quit()
                elif int(string) > num_t_steps:
                    print("ERROR: Requested to plot timestep ", int(string), " this is not allowed as the maximum allowed is ", num_t_steps)
                    quit()
                t_steps_to_print_plot.append(int(string))
        else:
            print("ERROR reached row ", num_rows+1, " this is not allowed")
        num_rows += 1


h_inf = 1.20e+5   # W/m^2*K
k_c   = 13.0      # W/m*K
k_f   = 3.6       # W/m*K
rho_c = 6500.0    # kg/m^3
rho_f = 9670.0    # kg/m^3
c_p_c = 330.0     # J/kg*K
c_p_f = 247.0     # J/kg*K
q_tp  = 1.0e+6    # W/m^3
l_f   = 0.01      # m
l_c   = 0.001     # m

# W/m*K / (kg/m^3 * J/kg*K) = m^2*K/s
a_f = k_f / (rho_f * c_p_f)

T_f_0 = T_inf
T_c_0 = T_inf

# x = l_f + l_c, T_x = 350
# rho * c_p dT/dt - k grad^2 T = q'''
# 1D
# rho * c_p dT/dt - k d^2T/dx^2 = q'''

# assume cladding has same temperature as T_inf for boundary condition initially

# dT_dt = (T_t+1 - T_t) / dt
# d^2T_dx^2 = (T_i+1 - 2 T_i + T_i-1) / dx^2

num_clad_points = 5
# Keep the number of points to have the same spatial size
num_fuel_points = num_clad_points * 10

dx = l_f / num_fuel_points

x_vals = []

x_vals.append(dx/2)

for i in range(1,num_fuel_points+num_clad_points):
    x_vals.append(x_vals[i-1]+dx)

fuel_temps = []
old_fuel_temps = []
clad_temps = []
old_clad_temps = []

fuel_temp_history = {}
clad_temp_history = {}

for i in range(0, num_fuel_points):
    fuel_temps.append(T_inf)
    old_fuel_temps.append(T_inf)

for i in range(0, num_clad_points):
    clad_temps.append(T_inf)
    old_clad_temps.append(T_inf)

fuel_temp_history[0] = cp.deepcopy(fuel_temps)
clad_temp_history[0] = cp.deepcopy(clad_temps)

# Now that the energy has been added, we can try to achieve spatial convergence

for s in range(1, num_t_steps+1):
    clad_temps[num_clad_points-1] += (t * k_c / (rho_c * c_p_c))*(-old_clad_temps[num_clad_points-1] + old_clad_temps[num_clad_points-2])/(dx**2) - (t*h_inf*dx /(rho_c * c_p_c))*(old_clad_temps[num_clad_points-1] - T_inf)/(dx**2)
    for i in range(num_clad_points-2, 0, -1):
        clad_temps[i] += (t * k_c / (rho_c * c_p_c))*(old_clad_temps[i+1] - 2*old_clad_temps[i] + old_clad_temps[i-1])/(dx**2)
    clad_temps[0] += (t * k_c / (rho_c * c_p_c))*(old_clad_temps[i+1] - 2*old_clad_temps[i] + old_fuel_temps[num_fuel_points-1])/(dx**2)
    fuel_temps[num_fuel_points-1] += (t / (rho_f * c_p_f))*(q_tp + k_f * (old_fuel_temps[num_fuel_points-2] - 2*old_fuel_temps[num_fuel_points-1] + clad_temps[0])/(dx**2))
    # Now we can solve for the rest of the fuel except the fuel-cladding boundary
    for i in range(num_fuel_points-2,0, -1):
        fuel_temps[i] += (t / (rho_f * c_p_f))*(q_tp + k_f * (old_fuel_temps[i-1] - 2*old_fuel_temps[i] + old_fuel_temps[i+1])/(dx**2))

    fuel_temps[0] += (t / (rho_f * c_p_f))*(q_tp + k_f * (- old_fuel_temps[0] + old_fuel_temps[1])/(dx**2))

    fuel_temp_history[s] = cp.deepcopy(fuel_temps)
    clad_temp_history[s] = cp.deepcopy(clad_temps)

    for i in range(0,num_fuel_points):
        old_fuel_temps[i] = cp.deepcopy(fuel_temps[i])

    for i in range(0,num_clad_points):
        old_clad_temps[i] = cp.deepcopy(clad_temps[i])

# Print plots as pdfs
for t_step in t_steps_to_print_plot:
    fig, ax = plt.subplots()

    y_vals = []
    for y in range(0, num_fuel_points):
        y_vals.append(fuel_temp_history[t_step][y])

    for y in range(0, num_clad_points):
        y_vals.append(clad_temp_history[t_step][y])

    ax.scatter(x_vals, y_vals, label='T', c="k", marker='.')
    ax.set_xlabel("Distance from Insulation [m]")
    ax.set_ylabel("Temperature [degree C]")

    pdf_filename = "question_3_part3_test_plot_t_step_" + str(t_step) + ".pdf"

    fig.savefig(pdf_filename, format='PDF', bbox_inches='tight')

# Print temperatures as CSV file
# Header row is the x-coordinate
with open('T_output.csv', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    header_row = []
    header_row.append("Timestep")
    for x in x_vals:
        header_row.append(str(x))
    writer.writerow(header_row)
    for t_step in t_steps_to_print_plot:
        row_to_write = []
        row_to_write.append(t_step)
        for y in range(0, num_fuel_points):
            row_to_write.append(fuel_temp_history[t_step][y])
        for y in range(0, num_clad_points):
            row_to_write.append(clad_temp_history[t_step][y])
        writer.writerow(row_to_write)