import tkinter as tk
from tkinter import messagebox, ttk
from decimal import Decimal, ROUND_HALF_UP

# DARK MODE REFUND CALCULATOR - AUTH: TRAVIS DUNN


# 🎨 UI Enhancements
# - Improved formatting of result output label for better alignment and readability.
# - Unified font usage (Segoe UI, Courier New) for consistency.
# - Dark mode styling applied to all components including popup window.
# - Button states enhanced with highlight color on hover and press.

# 🧹 Other Improvements
# - Added "Clear" button to reset all input fields and result display.
# - Button frame layout updated to evenly space Calculate, Clear, and Client Summary buttons.
# - Result label uses custom style (Result.TLabel) with consistent padding and formatting.

# ==============================================================================

# Main color scheme
BG_COLOR = "#2e2e2e"      # Dark background
FG_COLOR = "#ffffff"      # Bright white for maximum text visibility
ENTRY_BG = "#3e3e3e"      # Slightly lighter for entry fields
BUTTON_BG = "#333333"     # Darker gray for buttons to contrast with text
HIGHLIGHT_COLOR = "#00c4b4"  # Bright teal for active button state
FONT = ("Segoe UI", 10)
MONO_FONT = ("Courier New", 10)

class RefundCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Refund Calculator v1.3")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)  # Prevent window resizing
        self.setup_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def validate_numeric(self, action, value_if_allowed):
        # Allow only numeric input and one decimal point
        if action != '1':  # If not inserting
            return True
        try:
            if value_if_allowed == '':
                return True
            float(value_if_allowed)
            return True
        except ValueError:
            return False

    def calculate_refund(self):
        try:
            # Use Decimal for precise financial calculations
            total_cost = Decimal(self.entry_total_cost.get()).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            total_paid = Decimal(self.entry_total_paid.get()).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            tpp = Decimal(self.entry_tpp.get()).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            deposit = Decimal(self.entry_deposit.get()).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

            # Input validation
            if any(x < 0 for x in [total_cost, total_paid, tpp, deposit]):
                messagebox.showerror("Input Error", "Values cannot be negative.")
                return

            twenty_percent = (total_cost * Decimal('0.20')).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            greater_non_refundable = max(deposit, twenty_percent)

            reason = (f"Deposit used (${deposit:.2f} > ${twenty_percent:.2f})" if deposit > twenty_percent
                     else f"20% used (${twenty_percent:.2f} > ${deposit:.2f})" if twenty_percent > deposit
                     else "Deposit and 20% are equal")

            non_refundable = (tpp + greater_non_refundable).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            refund = max(Decimal('0.00'), (total_paid - non_refundable)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

            result_text = (
                f"     Refund Summary\n"
                f"{'='*26}\n"
                f"Total Package Cost:     ${total_cost:>9.2f}\n"
                f"Amount Paid:            ${total_paid:>9.2f}\n"
                f"TPP:                    ${tpp:>9.2f}\n"
                f"Deposit:                ${deposit:>9.2f}\n"
                f"20% of Cost:            ${twenty_percent:>9.2f}\n"
                f"{reason}\n"
                f"{'-'*26}\n"
                f"Non-Refundable Total:   ${non_refundable:>9.2f}\n"
                f"{'-'*26}\n"
                f"Refund Due:             ${refund:>9.2f}"
            )

            self.result_label.config(text=result_text, style="Result.TLabel")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

            

    def clear_fields(self):
        """Clear all input fields and reset result"""
        for entry in [self.entry_total_cost, self.entry_total_paid, 
                     self.entry_tpp, self.entry_deposit]:
            entry.delete(0, tk.END)
        self.result_label.config(text="", style="Result.TLabel")

    def setup_gui(self):
        # Set a consistent theme to avoid system overrides
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme for consistent rendering

        # Register validation function
        vcmd = (self.root.register(self.validate_numeric), '%d', '%P')

        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style="Main.TFrame")

        # Style configuration for consistent dark theme
        style.configure("Main.TFrame", background=BG_COLOR)
        # Label style for input labels
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=FONT)
        # Result label style for numbers
        style.configure("Result.TLabel", background=BG_COLOR, foreground=FG_COLOR, 
                       font=MONO_FONT, padding=5)
        # Entry style
        style.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG_COLOR, 
                       insertbackground=FG_COLOR, padding=5)
        # Button style
        style.configure("TButton", background=BUTTON_BG, foreground=FG_COLOR, 
                       font=FONT, padding=5)
        style.map("TButton", 
                 background=[('active', HIGHLIGHT_COLOR), ('pressed', HIGHLIGHT_COLOR)],
                 foreground=[('active', FG_COLOR), ('pressed', FG_COLOR)])

        # Labels & Entry Fields
        fields = [
            ("Total Trip Booking Cost ($):", 0),
            ("Amount Paid by Client ($):", 1),
            ("TPP Amount ($):", 2),
            ("Deposit Amount ($):", 3)
        ]

        self.entries = {}
        for text, row in fields:
            ttk.Label(main_frame, text=text, style="TLabel").grid(row=row, column=0, sticky="e", padx=10, pady=5)
            entry = ttk.Entry(main_frame, validate="key", validatecommand=vcmd, style="TEntry")
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[text] = entry

        self.entry_total_cost = self.entries["Total Trip Booking Cost ($):"]
        self.entry_total_paid = self.entries["Amount Paid by Client ($):"]
        self.entry_tpp = self.entries["TPP Amount ($):"]
        self.entry_deposit = self.entries["Deposit Amount ($):"]

        # Button frame
        button_frame = ttk.Frame(main_frame, style="Main.TFrame")
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        # Calculate and Clear Buttons
        ttk.Button(button_frame, text="Calculate Refund", 
                  command=self.calculate_refund, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_fields, style="TButton").grid(row=0, column=1, padx=5)

        # Result Label - Using ttk.Label with custom style for consistency
        self.result_label = ttk.Label(
            main_frame, text="", justify="left", style="Result.TLabel", anchor="w"
        )
        self.result_label.grid(row=5, column=0, columnspan=2, padx=15, pady=10, sticky="w")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = RefundCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
