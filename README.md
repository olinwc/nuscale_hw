# nuscale_hw
NuScale HW Jul 13 2023

The solutions to Questions 1, 2, and Part 1 of Question 3 are in the pdf file *nuscale_hw_questions1_2_3.pdf*

I've included the spreadsheet I used for steam table interpolation (ODS and XLSX versions)

I've also included the source LaTeX file for the *nuscale_hw_questions1_2_3.pdf* in *main.tex*

Plotting for Part 1 of Question 3 is done in Python in *question_3_part1.py* with the associated *question_3_part1_plot.pdf*

The remainder of Question 3 is done in Python in *question_3_parts2and3.py* the script fails to accurately calculate the temperature distribution but the user input and file I/O work.
*user_input.csv* specifies the user input for the system.
First row is, in order, the initial temperature (float), the size of the timesteps to take in seconds (float), and the number of timesteps to take (int)
Second row must be of at least size 1, and determines which timesteps to print the plots and temperature data for.
These values must be greater than 0 and less than or equal to the number of timesteps requested.

*T_output.csv* is a sample of the CSV file printed.

*question_3_part3_test_plot_t_step_X.pdf* are examples of the plots printed by the Python script.