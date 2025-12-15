import tkinter as tk
from ui import FractionTutorUI
from ontology_loader import load_ontology

def main():
    root = tk.Tk()
    root.title("Fraction → Decimal Tutor")

    ontology_graph, ns = load_ontology()

    app = FractionTutorUI(root, ontology_graph, ns)
    root.mainloop()

if __name__ == "__main__":
    main()
