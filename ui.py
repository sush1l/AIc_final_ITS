import tkinter as tk
from tkinter import ttk, messagebox
from logic import convert_fraction, step_by_step, fraction_hint, ontology_lookup
from quiz import FractionQuiz

PRIMARY = "#4A90E2"
SECONDARY = "#D9EFFF"
ACCENT = "#5CDB95"
BG = "#F7F9FC"
TEXT = "#333333"

class FractionTutorUI:
    def __init__(self, root, ontology_graph, ns):
        self.root = root
        self.graph = ontology_graph
        self.ns = ns

        self.quiz = FractionQuiz()

        root.configure(bg=BG)

        self._setup_styles()
        self.build_ui()

    # --------------------------------------------------------------------
    # STYLE SECTION
    # --------------------------------------------------------------------
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Button style
        style.configure(
            "TButton",
            font=("Arial", 11, "bold"),
            foreground="white",
            background=PRIMARY,
            padding=6,
            borderwidth=0,
            relief="flat"
        )
        style.map(
            "TButton",
            background=[("active", "#3A78C2")],
        )

        style.configure("Accent.TButton", background=ACCENT)

        style.configure("Header.TLabel",
                        font=("Arial", 16, "bold"),
                        foreground=PRIMARY,
                        background=BG)

        style.configure("TLabel",
                        background=BG,
                        foreground=TEXT,
                        font=("Arial", 11))

        style.configure("TEntry",
                        padding=3)

    # --------------------------------------------------------------------
    # UI BUILDING
    # --------------------------------------------------------------------
    def build_ui(self):
        frm = tk.Frame(self.root, bg=BG, padx=20, pady=20)
        frm.pack()

        ttk.Label(frm,
                  text="Fraction → Decimal Tutor",
                  style="Header.TLabel").grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Label(frm, text="Numerator:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(frm, text="Denominator:").grid(row=2, column=0, sticky="e")

        self.num_var = tk.StringVar()
        self.den_var = tk.StringVar()

        ttk.Entry(frm, textvariable=self.num_var, width=12).grid(row=1, column=1)
        ttk.Entry(frm, textvariable=self.den_var, width=12).grid(row=2, column=1)

        button_frame = tk.Frame(frm, bg=BG)
        button_frame.grid(row=3, column=0, columnspan=4, pady=15)

        ttk.Button(button_frame, text="Convert", command=self.on_convert).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Steps", command=self.on_step).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Hint", command=self.on_hint).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Quiz Me!", style="Accent.TButton",
                   command=self.start_quiz).grid(row=0, column=3, padx=5)

        self.output = tk.Text(frm,
                              height=14,
                              width=72,
                              bg=SECONDARY,
                              fg=TEXT,
                              font=("Consolas", 11),
                              borderwidth=3,
                              relief="groove")
        self.output.grid(row=4, column=0, columnspan=4, pady=10)

    # --------------------------------------------------------------------
    # BUTTON HANDLERS
    # --------------------------------------------------------------------
    def on_convert(self):
        try:
            n, d = int(self.num_var.get()), int(self.den_var.get())
        except ValueError:
            messagebox.showerror("Input error", "Enter integer numerator and denominator.")
            return

        if d == 0:
            messagebox.showerror("Math error", "Denominator cannot be zero.")
            return

        decimal_value = convert_fraction(n, d)
        self.output.insert(tk.END, f"Result: {n}/{d} = {decimal_value}\n")

        # Ontology lookup
        if self.graph:
            ont_result = ontology_lookup(self.graph, self.ns, n, d)
            self.output.insert(tk.END, ont_result + "\n")

    def on_step(self):
        try:
            n, d = int(self.num_var.get()), int(self.den_var.get())
        except ValueError:
            return

        steps = step_by_step(n, d)
        for s in steps:
            self.output.insert(tk.END, s + "\n")

    def on_hint(self):
        try:
            n, d = int(self.num_var.get()), int(self.den_var.get())
        except:
            self.output.insert(tk.END, "Hint: Enter a valid fraction.\n")
            return

        hint = fraction_hint(n, d)
        self.output.insert(tk.END, hint + "\n")

    # --------------------------------------------------------------------
    # QUIZ UI
    # --------------------------------------------------------------------
    def start_quiz(self):
        q_win = tk.Toplevel(self.root)
        q_win.title("Fraction Quiz")
        q_win.configure(bg=BG)

        question, answer = self.quiz.new_question()

        ttk.Label(q_win, text=f"Convert: {question}",
                  font=("Arial", 14, "bold"),
                  background=BG,
                  foreground=PRIMARY).pack(pady=10)

        ans_var = tk.StringVar()
        ttk.Entry(q_win, textvariable=ans_var, width=20).pack(pady=5)

        def check_answer():
            user_ans = ans_var.get().strip()
            result = self.quiz.check_answer(user_ans)
            messagebox.showinfo("Quiz Result", result)

        def show_answer():
            messagebox.showinfo("Correct Answer", f"{answer}")

        ttk.Button(q_win, text="Submit", command=check_answer).pack(pady=5)
        ttk.Button(q_win, text="Show Answer", style="Accent.TButton", command=show_answer).pack(pady=5)
