import tkinter as tk
import math

# ---------- Circular Button ----------
class CircularButton(tk.Canvas):
    def __init__(self, parent, text, command=None, diameter=86, bg="#00ff88", fg="#000000", hover_bg="#00cc66"):
        super().__init__(parent, width=diameter, height=diameter, highlightthickness=0, bg=parent["bg"])
        self.command = command
        self.bg_color = bg
        self.hover_bg = hover_bg
        self.text_value = text
        self.diameter = diameter

        # Draw circle and label
        margin = 3
        self.circle = self.create_oval(margin, margin, diameter - margin, diameter - margin, fill=bg, outline="")
        self.text_id = self.create_text(diameter/2, diameter/2, text=text, fill=fg, font=("Consolas", 20, "bold"))

        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_click(self, event):
        if self.command:
            self.command(self.text_value)

    def on_hover(self, event):
        self.itemconfig(self.circle, fill=self.hover_bg)

    def on_leave(self, event):
        self.itemconfig(self.circle, fill=self.bg_color)

# ---------- Calculator App ----------
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Circular Calculator + Unit Converter")
        # maximize window (cross-platform best-effort)
        try:
            self.state('zoomed')
        except:
            self.attributes('-zoomed', True)
        self.config(bg="#000000")

        self.expression = ""
        self.history = []

        self.create_widgets()

    # ---------------- UI ----------------
    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#000000")
        main_frame.pack(expand=True, fill="both", padx=24, pady=18)

        # Left: display + keypad
        left_frame = tk.Frame(main_frame, bg="#000000")
        left_frame.pack(side="left", expand=True, fill="both")

        # Right: history + converter
        right_frame = tk.Frame(main_frame, bg="#000000", width=360)
        right_frame.pack(side="right", fill="y", padx=(16,0))

        # Display (rounded feel via highlight)
        self.display = tk.Entry(
            left_frame, font=("Fira Code", 46, "bold"), bd=0,
            bg="#111111", fg="#00ff88", justify="right", insertbackground="#00ff88"
        )
        self.display.pack(fill="x", pady=(0,18), ipady=20)
        self.display.config(highlightthickness=3, highlightbackground="#00ff88", highlightcolor="#00ff88")

        # Button layout (UI shows × instead of *)
        button_layout = [
            ["(", ")", "%", "C", "√"],
            ["7", "8", "9", "/", "×"],
            ["4", "5", "6", "*", "^"],
            ["1", "2", "3", "-", "π"],
            ["0", ".", "=", "+", "ANS"]
        ]

        btn_grid = tk.Frame(left_frame, bg="#000000")
        btn_grid.pack(expand=True, fill="both")

        # Create buttons in a grid with consistent spacing
        diameter = 86
        for r, row in enumerate(button_layout):
            for c, txt in enumerate(row):
                # place circular buttons using grid manager
                btn = CircularButton(btn_grid, txt, command=self.on_button_click, diameter=diameter)
                btn.grid(row=r, column=c, padx=14, pady=14, sticky="nsew")

        # Make columns/rows expand evenly
        rows = len(button_layout)
        cols = len(button_layout[0])
        for i in range(rows):
            btn_grid.rowconfigure(i, weight=1)
        for j in range(cols):
            btn_grid.columnconfigure(j, weight=1)

        # ---------------- History ----------------
        hist_label = tk.Label(right_frame, text="History", font=("Consolas", 16, "bold"), bg="#000000", fg="#00ff88")
        hist_label.pack(pady=(6,4))

        self.history_list = tk.Listbox(
            right_frame, bg="#111111", fg="#00ff88", font=("Consolas", 12),
            selectbackground="#00ff88", selectforeground="#000000", highlightthickness=0
        )
        self.history_list.pack(fill="both", expand=False, padx=6, pady=(0,8))
        self.history_list.config(height=12)
        self.history_list.bind("<Double-Button-1>", self.use_history)

        # ---------------- Unit Converter ----------------
        conv_label = tk.Label(right_frame, text="Unit Converter", font=("Consolas", 14, "bold"), bg="#000000", fg="#00ff88")
        conv_label.pack(pady=(6,4))

        conv_frame = tk.Frame(right_frame, bg="#000000")
        conv_frame.pack(fill="both", padx=6, pady=6)

        # Category selector
        tk.Label(conv_frame, text="Category:", bg="#000000", fg="#00ff88", font=("Consolas",11)).grid(row=0, column=0, sticky="w")
        self.category_var = tk.StringVar(value="Length")
        categories = ["Length", "Weight", "Temperature", "Time", "Data"]
        self.category_menu = tk.OptionMenu(conv_frame, self.category_var, *categories, command=self.update_units)
        self.style_optionmenu(self.category_menu)
        self.category_menu.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)

        # From / To units
        tk.Label(conv_frame, text="From:", bg="#000000", fg="#00ff88", font=("Consolas",11)).grid(row=1, column=0, sticky="w")
        self.from_var = tk.StringVar()
        self.from_menu = tk.OptionMenu(conv_frame, self.from_var, "")
        self.style_optionmenu(self.from_menu)
        self.from_menu.grid(row=1, column=1, sticky="ew", padx=(0,6), pady=4)

        tk.Label(conv_frame, text="To:", bg="#000000", fg="#00ff88", font=("Consolas",11)).grid(row=1, column=2, sticky="w")
        self.to_var = tk.StringVar()
        self.to_menu = tk.OptionMenu(conv_frame, self.to_var, "")
        self.style_optionmenu(self.to_menu)
        self.to_menu.grid(row=1, column=3, sticky="ew", pady=4)

        # Value entry
        tk.Label(conv_frame, text="Value:", bg="#000000", fg="#00ff88", font=("Consolas",11)).grid(row=2, column=0, sticky="w", pady=(6,0))
        self.conv_value = tk.Entry(conv_frame, bg="#111111", fg="#00ff88", insertbackground="#00ff88", font=("Consolas",12), bd=0)
        self.conv_value.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(6,0))

        # Convert button and result
        conv_btn = tk.Button(conv_frame, text="Convert", command=self.perform_conversion, bg="#00ff88", fg="#000000", bd=0, font=("Consolas",12,"bold"))
        conv_btn.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=(0,6))
        self.style_button(conv_btn)

        self.conv_result = tk.Label(conv_frame, text="", bg="#000000", fg="#00ff88", font=("Consolas",12))
        self.conv_result.grid(row=3, column=2, columnspan=2, sticky="ew")

        # Configure grid weights in converter
        for col in range(4):
            conv_frame.columnconfigure(col, weight=1)

        # initialize unit lists
        self.units = self.full_units_dictionary()
        self.update_units("Length")

        # store last answer (ANS) for button
        self.last_answer = ""

    # ---------------- Styling helpers ----------------
    def style_optionmenu(self, om):
        om.config(bg="#1e1e1e", fg="#00ff88", bd=0, activebackground="#111111", highlightthickness=0, font=("Consolas", 11))
        menu = om["menu"]
        menu.config(bg="#111111", fg="#00ff88", bd=0)

    def style_button(self, b):
        b.config(activebackground="#00cc66", relief="flat")

    # ---------------- Units dictionary ----------------
    def full_units_dictionary(self):
        return {
            "Length": {
                "meter": 1.0,
                "kilometer": 1000.0,
                "centimeter": 0.01,
                "millimeter": 0.001,
                "mile": 1609.344,
                "yard": 0.9144,
                "foot": 0.3048,
                "inch": 0.0254
            },
            "Weight": {
                "kilogram": 1.0,
                "gram": 0.001,
                "milligram": 1e-6,
                "pound": 0.45359237,
                "ounce": 0.028349523125
            },
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": {
                "second": 1.0,
                "minute": 60.0,
                "hour": 3600.0,
                "day": 86400.0
            },
            "Data": {
                "bit": 1/8.0,
                "byte": 1.0,
                "kilobyte": 1024.0,
                "megabyte": 1024.0**2,
                "gigabyte": 1024.0**3,
                "terabyte": 1024.0**4
            }
        }

    # ---------------- Unit UI update ----------------
    def update_units(self, category):
        u = self.units.get(category)
        from_menu = self.from_menu["menu"]
        to_menu = self.to_menu["menu"]
        from_menu.delete(0, "end")
        to_menu.delete(0, "end")

        if isinstance(u, dict):
            keys = list(u.keys())
        else:
            keys = u[:]  # list for temperature

        # populate
        for k in keys:
            from_menu.add_command(label=k, command=lambda val=k: self.from_var.set(val))
            to_menu.add_command(label=k, command=lambda val=k: self.to_var.set(val))

        # set defaults
        if keys:
            self.from_var.set(keys[0])
            self.to_var.set(keys[1] if len(keys) > 1 else keys[0])

    # ---------------- Conversion logic ----------------
    def perform_conversion(self):
        cat = self.category_var.get()
        frm = self.from_var.get()
        to = self.to_var.get()
        val_text = self.conv_value.get().strip()
        if val_text == "":
            self.conv_result.config(text="Enter value")
            return
        try:
            value = float(val_text)
        except:
            self.conv_result.config(text="Invalid number")
            return

        # Temperature special cases
        if cat == "Temperature":
            res = self.convert_temperature(value, frm, to)
        else:
            mapping = self.units.get(cat)
            if not isinstance(mapping, dict):
                self.conv_result.config(text="Invalid units")
                return
            # convert value -> base -> target
            base_val = value * mapping[frm]   # mapping values chosen so base is meter/kg/second/byte
            result = base_val / mapping[to]
            res = result

        # format nicely
        res_str = f"{value} {frm} = {self.format_number(res)} {to}"
        self.conv_result.config(text=self.format_number(res) + " " + to)
        self.add_to_history(res_str)
        # also set last_answer for ANS reuse
        self.last_answer = str(self.format_number(res))

    def convert_temperature(self, v, frm, to):
        # convert to Celsius base
        def to_celsius(val, unit):
            if unit == "Celsius":
                return val
            if unit == "Fahrenheit":
                return (val - 32.0) * 5.0/9.0
            if unit == "Kelvin":
                return val - 273.15
            raise ValueError("Unknown temp")

        def from_celsius(cval, unit):
            if unit == "Celsius":
                return cval
            if unit == "Fahrenheit":
                return cval * 9.0/5.0 + 32.0
            if unit == "Kelvin":
                return cval + 273.15
            raise ValueError("Unknown temp")

        c = to_celsius(v, frm)
        return from_celsius(c, to)

    # ---------------- Helpers ----------------
    def format_number(self, n):
        # pretty format: remove trailing zeros
        if isinstance(n, float):
            if abs(n) < 1e-12:
                return "0"
            s = f"{n:.12g}"
            return s
        return str(n)

    # ---------------- Button behavior ----------------
    def on_button_click(self, char):
        # Special keys
        if char == "C":
            self.clear()
            return
        if char == "=":
            self.evaluate_expression()
            return
        if char == "√":
            # attempt sqrt of current display
            try:
                v = float(self.display.get())
                res = math.sqrt(v)
                self.add_to_history(f"√({v}) = {self.format_number(res)}")
                self.set_display(self.format_number(res))
                self.last_answer = str(self.format_number(res))
            except:
                self.set_display("Error")
            return
        if char == "π":
            self.expression += str(math.pi)
            self.update_display(self.expression)
            return
        if char == "ANS":
            self.expression += self.last_answer
            self.update_display(self.expression)
            return
        if char == "×":
            self.expression += "*"
            self.update_display(self.expression)
            return
        if char == "^":
            self.expression += "**"
            self.update_display(self.expression)
            return
        if char == "%":
            # percent of current number (simple behavior: divide last number by 100)
            try:
                # if display is empty, ignore
                current = self.display.get()
                if current:
                    val = float(current)
                    val = val / 100.0
                    self.expression = str(val)
                    self.update_display(self.expression)
                    self.last_answer = str(self.expression)
                else:
                    pass
            except:
                self.set_display("Error")
            return
        # default append (including parentheses and digits and operators)
        self.expression += str(char)
        self.update_display(self.expression)

    def update_display(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(0, text)

    def set_display(self, text):
        self.expression = str(text)
        self.update_display(self.expression)

    def clear(self):
        self.expression = ""
        self.update_display("")

    def evaluate_expression(self):
        # evaluate safely-ish (local app). Use math namespace for convenience.
        try:
            # allow math functions: sin, cos, etc. if user types them, we provide math namespace
            allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            # also allow builtins safe constants
            allowed_names.update({"__builtins__": {}})
            # evaluate
            result = eval(self.expression, {"__builtins__": {}}, allowed_names)
            res_str = self.format_number(result)
            self.add_to_history(f"{self.expression} = {res_str}")
            self.set_display(res_str)
            self.last_answer = str(res_str)
        except Exception as e:
            self.set_display("Error")

    # ---------------- History ----------------
    def add_to_history(self, text):
        self.history.append(text)
        self.history_list.insert(tk.END, text)

    def use_history(self, event):
        sel = self.history_list.curselection()
        if not sel:
            return
        item = self.history_list.get(sel[0])
        # if there's an =, take the RHS as result; else put entire item
        if "=" in item:
            rhs = item.split("=")[-1].strip()
            # try to extract numeric part if like "123 unit"
            try:
                # split first token if "num unit"
                first_token = rhs.split()[0]
                val = float(first_token)
                self.set_display(str(self.format_number(val)))
                self.last_answer = str(self.format_number(val))
            except:
                # fallback: put rhs text
                self.set_display(rhs)
        else:
            self.set_display(item)

# ---------- Run ----------
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
