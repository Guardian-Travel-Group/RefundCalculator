# -*- coding: utf-8 -*-
"""Refund Calculator
"""
## Auth: Travis Dunn 
##refund calculator for TPP trip refunds.

##remaking the GUI  because it got a bit too complicated.

#CHANGE LOG

### Input Validation ##
# A helper function get_non_negative_float ensures all inputs 
# (total cost, amount paid, TPP, and deposit) are valid, non-negative numbers.

## Simple Introduction ##
# At the start of each calculation, a welcome message explains 
# what the program does so users know what to expect.

## Multiple Calculations ##
# The code runs in a loop, allowing multiple refund calculations 
# in one session. After each result, it asks the user if they'd 
# like to calculate another (type "yes" or "y" to continue).

## Calculation Timestamp ##
# Each output includes the date and time the calculation was performed 
# using the datetime module — useful for record-keeping.

## Clear Comments ##
# Comments are added above key sections (inputs, calculations, outputs)
# to make the code easier to read, understand, and maintain.

## Zero Refund Explanation ##
# If the refund equals $0, the program prints a note explaining 
# why (e.g., total paid doesn't exceed the non-refundable portion),
# making the summary more informative.



import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Initialize dark mode state
is_dark_mode = False

# Color schemes for light and dark modes
light_mode = {
    "bg": "#f0f0f0",  # Light gray background
    "fg": "black",     # Black text
    "button_bg": "#4CAF50",  # Green for Calculate button
    "clear_button_bg": "#d3d3d3",  # Gray for Clear/Toggle buttons
    "result_bg": "#f0f0f0"  # Light gray for result area
}

dark_mode = {
    "bg": "#2d2d2d",  # Dark gray background
    "fg": "#e0e0e0",  # Light gray text
    "button_bg": "#45a049",  # Slightly darker green for Calculate button
    "clear_button_bg": "#555555",  # Darker gray for Clear/Toggle buttons
    "result_bg": "#2d2d2d"  # Dark gray for result area
}

# Function to calculate the refund and display detailed output
def calculate():
    try:
        # Get inputs from the entry fields
        total_cost = float(entry_total_cost.get())
        amount_paid = float(entry_amount_paid.get())
        tpp = float(entry_tpp.get())
        deposit = float(entry_deposit.get())

        # Check for negative values
        if total_cost < 0 or amount_paid < 0 or tpp < 0 or deposit < 0:
            raise ValueError("Negative values are not allowed")

        # Perform calculations
        twenty_percent = 0.20 * total_cost
        if deposit >= twenty_percent:
            tnr = tpp + deposit
        else:
            tnr = tpp + twenty_percent
        refund = max(amount_paid - tnr, 0)

        # Format the output to match the original command-line version
        result_text = "=== Calculation Summary ===\n"
        result_text += f"    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result_text += f"           \n"
        result_text += f"Total Package Cost: ${total_cost:.2f}\n"
        result_text += f"Total Paid: ${amount_paid:.2f}\n"
        result_text += f"TPP: ${tpp:.2f}\n"
        result_text += f"Deposit: ${deposit:.2f}\n"
        result_text += f"20% of Package Cost: ${twenty_percent:.2f}\n"
        result_text += "----------------------------\n"
        result_text += f"Total Paid: ${amount_paid:.2f}\n"
        result_text += f"Total Non-Refundable (TNR): ${tnr:.2f}\n"
        result_text += f"Refund Due: ${refund:.2f}\n"
        if refund == 0:
            result_text += "No refund is due"

        # Update the result label
        label_result.config(text=result_text)

    except ValueError:
        # Show error message for invalid inputs
        messagebox.showerror("Error", "Please enter valid non-negative numbers.")

# Function to toggle between light and dark modes
def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode  # Toggle the state

    # Select the appropriate color scheme
    colors = dark_mode if is_dark_mode else light_mode

    # Update colors for all widgets
    root.configure(bg=colors["bg"])
    main_frame.configure(bg=colors["bg"])
    button_frame.configure(bg=colors["bg"])
    label_total_cost.configure(bg=colors["bg"], fg=colors["fg"])
    label_amount_paid.configure(bg=colors["bg"], fg=colors["fg"])
    label_tpp.configure(bg=colors["bg"], fg=colors["fg"])
    label_deposit.configure(bg=colors["bg"], fg=colors["fg"])
    button_calculate.configure(bg=colors["button_bg"], fg="white")
    button_clear.configure(bg=colors["clear_button_bg"], fg="white")
    button_toggle_mode.configure(bg=colors["clear_button_bg"], fg="white")
    label_result.configure(bg=colors["result_bg"], fg=colors["fg"])
    entry_total_cost.configure(bg=colors["result_bg"], fg=colors["fg"])
    entry_amount_paid.configure(bg=colors["result_bg"], fg=colors["fg"])
    entry_tpp.configure(bg=colors["result_bg"], fg=colors["fg"])
    entry_deposit.configure(bg=colors["result_bg"], fg=colors["fg"])

    # Update button text to reflect current mode
    button_toggle_mode.config(text="Light Mode" if is_dark_mode else "Dark Mode")

# Create the main window
root = tk.Tk()
root.title("TPP Refund Calculator")
root.configure(bg=light_mode["bg"])  # Start in light mode

# Create a main frame for better organization
main_frame = tk.Frame(root, bg=light_mode["bg"], padx=20, pady=20)
main_frame.grid(row=0, column=0, sticky='nsew')

# Configure fonts for a professional look
label_font = ("Arial", 10)
entry_font = ("Arial", 10)
result_font = ("Courier New", 10)  # Monospaced for aligned output

# Create labels and entry fields for inputs
label_total_cost = tk.Label(main_frame, text="Total Trip Booking Cost:", font=label_font, bg=light_mode["bg"], fg=light_mode["fg"])
label_total_cost.grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry_total_cost = tk.Entry(main_frame, width=15, font=entry_font, bg=light_mode["result_bg"], fg=light_mode["fg"])
entry_total_cost.grid(row=0, column=1, padx=5, pady=5)

label_amount_paid = tk.Label(main_frame, text="Amount Client Paid:", font=label_font, bg=light_mode["bg"], fg=light_mode["fg"])
label_amount_paid.grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_amount_paid = tk.Entry(main_frame, width=15, font=entry_font, bg=light_mode["result_bg"], fg=light_mode["fg"])
entry_amount_paid.grid(row=1, column=1, padx=5, pady=5)

label_tpp = tk.Label(main_frame, text="TPP Amount:", font=label_font, bg=light_mode["bg"], fg=light_mode["fg"])
label_tpp.grid(row=2, column=0, sticky='e', padx=5, pady=5)
entry_tpp = tk.Entry(main_frame, width=15, font=entry_font, bg=light_mode["result_bg"], fg=light_mode["fg"])
entry_tpp.grid(row=2, column=1, padx=5, pady=5)

label_deposit = tk.Label(main_frame, text="Deposit Amount:", font=label_font, bg=light_mode["bg"], fg=light_mode["fg"])
label_deposit.grid(row=3, column=0, sticky='e', padx=5, pady=5)
entry_deposit = tk.Entry(main_frame, width=15, font=entry_font, bg=light_mode["result_bg"], fg=light_mode["fg"])
entry_deposit.grid(row=3, column=1, padx=5, pady=5)

# Create a frame for buttons
button_frame = tk.Frame(main_frame, bg=light_mode["bg"])
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

# Create the calculate button
button_calculate = tk.Button(button_frame, text="Calculate", command=calculate, font=label_font, bg=light_mode["button_bg"], fg="white", width=10)
button_calculate.grid(row=0, column=0, padx=5)

# Create a clear button to reset inputs
def clear_fields():
    entry_total_cost.delete(0, tk.END)
    entry_amount_paid.delete(0, tk.END)
    entry_tpp.delete(0, tk.END)
    entry_deposit.delete(0, tk.END)
    label_result.config(text=" ")
    entry_total_cost.focus_set()

button_clear = tk.Button(button_frame, text="Clear", command=clear_fields, font=label_font, bg=light_mode["clear_button_bg"], fg="white", width=10)
button_clear.grid(row=0, column=1, padx=5)

# Create the dark mode toggle button
button_toggle_mode = tk.Button(button_frame, text="Dark Mode", command=toggle_dark_mode, font=label_font, bg=light_mode["clear_button_bg"], fg="white", width=10)
button_toggle_mode.grid(row=0, column=2, padx=5)

# Create the result label without a border or fixed size
label_result = tk.Label(main_frame, text=" ", font=result_font, justify="left", anchor="w", bg=light_mode["result_bg"], fg=light_mode["fg"])
label_result.grid(row=5, column=0, columnspan=2, sticky='w', padx=5, pady=5)

# Set initial focus to the first entry field
entry_total_cost.focus_set()

# Function to handle window close event with confirmation
def on_closing():
    if messagebox.askyesno("Confirm Close", "Are you sure you want to close?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# Start the Tkinter event loop
root.mainloop()
