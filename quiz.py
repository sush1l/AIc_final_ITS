import random

class FractionQuiz:
    def __init__(self):
        self.current_fraction = None
        self.correct_answer = None

    def new_question(self):
        n = random.randint(1, 9)
        d = random.randint(2, 9)
        self.current_fraction = (n, d)
        self.correct_answer = round(n / d, 5)
        return f"{n}/{d}", self.correct_answer

    def check_answer(self, user_input):
        try:
            user_val = float(user_input)
            if abs(user_val - self.correct_answer) < 0.0001:
                return "Correct! Great job!"
            else:
                return f"Incorrect. Try again!"
        except:
            return "Invalid input. Enter a number."
