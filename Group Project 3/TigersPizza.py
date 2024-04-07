import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class PizzaOrderingSystem:
    def __init__(self, root, inventory=None):
        self.root = root
        self.root.title("Pizza Ordering and Inventory Management System")
        self.bg_color = "#FFD166"  # Cheddar cheese color for the background
        self.button_color = "#FFA500"  # Orange color for buttons
        self.label_color = "#333333"  # Dark gray color for labels
        self.font_style = ("Arial", 12, "bold")  # Custom font style

        # Define pizza sizes, crusts, and toppings
        self.sizes = ["Small", "Medium", "Large"]
        self.crusts = ["Thin Crust", "Regular Crust", "Thick Crust"]
        self.toppings = ["Cheese", "Tomatoes", "Basil", "Pepperoni", "Peppers", "Olives", "Onions", "Mushrooms", "Ham", "Pineapple"]
        
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = {
                        "Margherita": {"Cheese": 2, "Tomatoes": 1, "Basil": 1},
                        "Pepperoni": {"Cheese": 2, "Pepperoni": 3},
                        "Vegetarian": {"Cheese": 2, "Peppers": 1, "Olives": 1, "Onions": 1, "Mushrooms": 1},
                        "Hawaiian": {"Cheese": 2, "Ham": 2, "Pineapple": 1}
                    }        
        
        # Initialize order variables
        self.selected_pizza = tk.StringVar(root)
        self.selected_pizza.set("Select Pizza")
        self.selected_size = tk.StringVar(root)
        self.selected_size.set(self.sizes[0])  # Default size
        self.selected_crust = tk.StringVar(root)
        self.selected_crust.set(self.crusts[0])  # Default crust
        self.selected_toppings = [tk.BooleanVar(root, value=False) for _ in range(len(self.toppings))]
        self.quantity = tk.StringVar(root)
        self.quantity.set("1")
        self.customer_name = tk.StringVar(root)
        self.customer_phone = tk.StringVar(root)
        
        # Load orders from JSON file
        self.orders = []
        try:
            with open("orders.json", "r") as file:
                self.orders = json.load(file)
        except FileNotFoundError:
            pass
        
        # Create ordering GUI
        self.create_order_gui()

    def create_order_gui(self):
        label = tk.Label(self.root, text="Order Pizza", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        label.grid(row=0, column=0, columnspan=2, pady=10)
        
        pizza_label = tk.Label(self.root, text="Pizza:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        pizza_label.grid(row=1, column=0, sticky="w")
        pizza_dropdown = tk.OptionMenu(self.root, self.selected_pizza, *self.inventory.keys())
        pizza_dropdown.grid(row=1, column=1)
        
        size_label = tk.Label(self.root, text="Size:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        size_label.grid(row=2, column=0, sticky="w")
        size_dropdown = tk.OptionMenu(self.root, self.selected_size, *self.sizes)
        size_dropdown.grid(row=2, column=1)
        
        crust_label = tk.Label(self.root, text="Crust:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        crust_label.grid(row=3, column=0, sticky="w")
        crust_dropdown = tk.OptionMenu(self.root, self.selected_crust, *self.crusts)
        crust_dropdown.grid(row=3, column=1)
        
        toppings_label = tk.Label(self.root, text="Toppings:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        toppings_label.grid(row=4, column=0, sticky="w")
        for idx, topping in enumerate(self.toppings):
            topping_checkbox = tk.Checkbutton(self.root, text=topping, variable=self.selected_toppings[idx], bg=self.bg_color, fg=self.label_color, font=self.font_style)
            topping_checkbox.grid(row=4+idx, column=1, sticky="w")
        
        quantity_label = tk.Label(self.root, text="Quantity:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        quantity_label.grid(row=5+len(self.toppings), column=0, sticky="w")
        quantity_entry = tk.Entry(self.root, textvariable=self.quantity)
        quantity_entry.grid(row=5+len(self.toppings), column=1)
        
        customer_name_label = tk.Label(self.root, text="Customer Name:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        customer_name_label.grid(row=6+len(self.toppings), column=0, sticky="w")
        customer_name_entry = tk.Entry(self.root, textvariable=self.customer_name)
        customer_name_entry.grid(row=6+len(self.toppings), column=1)
        
        customer_phone_label = tk.Label(self.root, text="Customer Phone:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        customer_phone_label.grid(row=7+len(self.toppings), column=0, sticky="w")
        customer_phone_entry = tk.Entry(self.root, textvariable=self.customer_phone)
        customer_phone_entry.grid(row=7+len(self.toppings), column=1)
        
        order_button = tk.Button(self.root, text="Place Order", command=self.place_order, bg=self.button_color, fg=self.label_color, font=self.font_style)
        order_button.grid(row=8+len(self.toppings), column=0, columnspan=2, pady=10)
        order_button.bind("<Enter>", lambda event: order_button.config(bg="orange"))  # Hover effect
        order_button.bind("<Leave>", lambda event: order_button.config(bg=self.button_color))

        switch_button = tk.Button(self.root, text="Switch to Inventory Management", command=self.switch_to_management, bg=self.button_color, fg=self.label_color, font=self.font_style)
        switch_button.grid(row=9+len(self.toppings), column=0, columnspan=2, pady=10)
        switch_button.bind("<Enter>", lambda event: switch_button.config(bg="orange"))  # Hover effect
        switch_button.bind("<Leave>", lambda event: switch_button.config(bg=self.button_color))

        self.root.configure(bg=self.bg_color)  # Set background color of the main window

    def place_order(self):
        pizza = self.selected_pizza.get()
        size = self.selected_size.get()
        crust = self.selected_crust.get()
        quantity = self.quantity.get()
        customer_name = self.customer_name.get()
        customer_phone = self.customer_phone.get()

        # Validate user input
        if pizza == "Select Pizza" or pizza not in self.inventory:
            tk.messagebox.showerror("Error", "Please select a valid pizza.")
            return

        if size not in self.sizes:
            tk.messagebox.showerror("Error", "Please select a valid size.")
            return

        if crust not in self.crusts:
            tk.messagebox.showerror("Error", "Please select a valid crust.")
            return

        if not customer_name:
            tk.messagebox.showerror("Error", "Please enter customer name.")
            return

        if not customer_phone:
            tk.messagebox.showerror("Error", "Please enter customer phone number.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        # Check if inventory is sufficient for each ingredient needed for the pizza
        sufficient_inventory = True
        for topping, amount in self.inventory[pizza].items():
            if self.inventory[pizza][topping] < quantity * amount:
                sufficient_inventory = False
                break

        if not sufficient_inventory:
            tk.messagebox.showerror("Error", "Insufficient ingredients for the pizza. Please adjust your order!")
            return
        else:
            # Deduct ingredients from inventory
            for topping, amount in self.inventory[pizza].items():
                self.inventory[pizza][topping] -= quantity * amount

            # Create and save the order
            order = {
                "pizza": pizza,
                "size": size,
                "crust": crust,
                "quantity": quantity,
                "customer_name": customer_name,
                "customer_phone": customer_phone,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.orders.append(order)
            with open("orders.json", "w") as file:
                json.dump(self.orders, file, indent=4)

            tk.messagebox.showinfo("Order Placed", f"{quantity} {size} {crust} {pizza} pizza(s) ordered for {customer_name}!")

    def switch_to_management(self):
        self.root.destroy()
        root = tk.Tk()
        management_system = InventoryManagementSystem(root, self.inventory)
        root.mainloop()


class InventoryManagementSystem:
    def __init__(self, root, inventory):
        self.root = root
        self.root.title("Pizza Ordering and Inventory Management System")
        self.bg_color = "#FFD166"  # Cheddar cheese color for the background
        self.button_color = "#FFA500"  # Orange color for buttons
        self.label_color = "#333333"  # Dark gray color for labels
        self.font_style = ("Arial", 12, "bold")  # Custom font style
        
        # Initialize inventory
        self.inventory = inventory        
        # Load orders from JSON file
        self.orders = []
        try:
            with open("orders.json", "r") as file:
                self.orders = json.load(file)
        except FileNotFoundError:
            pass
        
        # Create management GUI
        self.create_management_gui()

    def create_management_gui(self):
        label = tk.Label(self.root, text="Inventory Management", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        label.grid(row=0, column=0, columnspan=2, pady=10)
        
        inventory_label = tk.Label(self.root, text="Inventory:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        inventory_label.grid(row=1, column=0, sticky="w")
        
        self.inventory_listbox = tk.Listbox(self.root, width=20, height=8)
        self.inventory_listbox.grid(row=1, column=1)
        self.update_inventory_list()
        
        revenue_label = tk.Label(self.root, text="Revenue:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        revenue_label.grid(row=2, column=0, sticky="w")
        
        self.revenue_label = tk.Label(self.root, text="$0", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        self.revenue_label.grid(row=2, column=1)
        self.calculate_revenue()
        
        switch_button = tk.Button(self.root, text="Switch to Pizza Ordering", command=self.switch_to_ordering, bg=self.button_color, fg=self.label_color, font=self.font_style)
        switch_button.grid(row=3, column=0, columnspan=2, pady=10)
        switch_button.bind("<Enter>", lambda event: switch_button.config(bg="orange"))  # Hover effect
        switch_button.bind("<Leave>", lambda event: switch_button.config(bg=self.button_color))

        self.update_inventory_list()

        self.timesheet_system = TimesheetSystem(self.root)

        search_label = tk.Label(self.root, text="Search Orders by Full Name:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        search_label.grid(row=10, column=0, sticky="w", pady=(10, 0))
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=10, column=1, pady=(10, 0))
        
        search_button = tk.Button(self.root, text="Search", command=self.search_orders, bg=self.button_color, fg=self.label_color, font=self.font_style)
        search_button.grid(row=11, column=0, columnspan=2)
        search_button.bind("<Enter>", lambda event: search_button.config(bg="orange"))  # Hover effect
        search_button.bind("<Leave>", lambda event: search_button.config(bg=self.button_color))
        
        self.search_results_listbox = tk.Listbox(self.root, width=50, height=10)
        self.search_results_listbox.grid(row=12, column=0, columnspan=2, pady=(5, 0))

    def search_orders(self):
        last_name = self.search_entry.get().strip()
        if not all(x.isalpha() or x.isspace() for x in last_name):
            messagebox.showerror("Error", "Last name must contain only letters.")
            return
        
        self.search_results_listbox.delete(0, tk.END)  # Clear previous search results
        for order in self.orders:
            customer_name = order.get("customer_name", "")
            if last_name.lower() in customer_name.split()[-1].lower():  # Assuming the last word in customer_name is the last name
                order_details = f"{customer_name} - {order['pizza']} - {order['quantity']} pcs"
                self.search_results_listbox.insert(tk.END, order_details)

    def update_inventory_list(self):
        self.inventory_listbox.delete(0, tk.END)
        for pizza, toppings in self.inventory.items():
            self.inventory_listbox.insert(tk.END, f"{pizza}:")
            for topping, quantity in toppings.items():
                self.inventory_listbox.insert(tk.END, f"  {topping}: {quantity}")

    def calculate_revenue(self):
        revenue = sum(order["quantity"] * 10 for order in self.orders)  # Assuming each pizza costs $10
        self.revenue_label.config(text=f"${revenue}")

    def switch_to_ordering(self):
        self.root.destroy()
        root = tk.Tk()
        ordering_system = PizzaOrderingSystem(root, self.inventory)
        root.mainloop()

class TimesheetSystem:
    def __init__(self, root):
        self.root = root
        self.timeslots = {
            "6 AM - 10 AM": [],
            "10 AM - 2 PM": [],
            "2 PM - 6 PM": [],
            "6 PM - 10 PM": [],
        }

        # Preset employees
        self.employees = ["Alice", "Bob", "Charlie", "Dana", "Evan"]
        
        # Create timesheet GUI below the management GUI
        self.create_timesheet_gui()

    def create_timesheet_gui(self):
        label = tk.Label(self.root, text="Employee Timesheet", bg="#FFD166", fg="#333333", font=("Arial", 12, "bold"))
        label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        self.timeslot_listbox = tk.Listbox(self.root, width=30, height=8)
        self.timeslot_listbox.grid(row=5, column=0, columnspan=2)
        self.update_timeslot_list()
        
        add_employee_label = tk.Label(self.root, text="Add/Remove Employee:", bg="#FFD166", fg="#333333", font=("Arial", 12, "bold"))
        add_employee_label.grid(row=6, column=0, sticky="w")
        self.employee_name_entry = tk.Entry(self.root)
        self.employee_name_entry.grid(row=6, column=1)

        self.timeslot_var = tk.StringVar(self.root)
        self.timeslot_var.set("Select Timeslot")
        timeslot_dropdown = tk.OptionMenu(self.root, self.timeslot_var, *self.timeslots.keys())
        timeslot_dropdown.grid(row=7, column=1, sticky="w")
        
        add_button = tk.Button(self.root, text="Add Employee", command=self.add_employee_to_timeslot, bg="#FFA500", fg="#333333", font=("Arial", 12, "bold"))
        add_button.grid(row=8, column=0, sticky="w")
        
        remove_button = tk.Button(self.root, text="Remove Employee", command=self.remove_employee_from_timeslot, bg="#FFA500", fg="#333333", font=("Arial", 12, "bold"))
        remove_button.grid(row=8, column=1, sticky="w")

    def update_timeslot_list(self):
        self.timeslot_listbox.delete(0, tk.END)
        for timeslot, employees in self.timeslots.items():
            self.timeslot_listbox.insert(tk.END, f"{timeslot}: {', '.join(employees) if employees else 'Empty'}")

    def add_employee_to_timeslot(self):
        employee = self.employee_name_entry.get()
        if not all(x.isalpha() or x.isspace() for x in employee):
            messagebox.showerror("Error", "Employee name must contain only letters.")
            return
        timeslot = self.timeslot_var.get()
        if timeslot not in self.timeslots or employee == "":
            tk.messagebox.showerror("Error", "Invalid timeslot or employee name.")
            return
        if employee not in self.timeslots[timeslot]:
            self.timeslots[timeslot].append(employee)
            self.update_timeslot_list()

    def remove_employee_from_timeslot(self):
        employee = self.employee_name_entry.get()
        if not all(x.isalpha() or x.isspace() for x in employee):
            messagebox.showerror("Error", "Employee name must contain only letters.")
            return
        timeslot = self.timeslot_var.get()
        if timeslot not in self.timeslots or employee == "":
            tk.messagebox.showerror("Error", "Invalid timeslot or employee name.")
            return
        if employee in self.timeslots[timeslot]:
            self.timeslots[timeslot].remove(employee)
            self.update_timeslot_list()

if __name__ == "__main__":
    root = tk.Tk()
    ordering_system = PizzaOrderingSystem(root)
    root.mainloop()