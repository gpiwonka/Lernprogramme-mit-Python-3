import random
from fractions import Fraction

def bruch():
    zaehler = random.randint(1, 10)
    nenner = random.randint(zaehler + 1, 10)
    fraction = Fraction(zaehler, nenner)
    return fraction

def antwort_berechnen(fraction1, fraction2, operator):
    if operator == '+':
        result = fraction1 + fraction2
    elif operator == '-':
        result = fraction1 - fraction2
    elif operator == '*':
        result = fraction1 * fraction2
    elif operator == '/':
        result = fraction1 / fraction2
    else:
        raise ValueError("Falsche Operation")

    decimal_answer = result.numerator / result.denominator
    return decimal_answer, result

def parse_fraction(fraction_str):
    try:
        fraction = Fraction(fraction_str)
        return fraction
    except ValueError:
        return None

def main():
    print("Willkommen beim Bruchrechnen!")
    score = 0
    num_Frage = 5

    operators = ['+', '-', '*', '/']

    for _ in range(num_Frage):
        fraction1 = bruch()
        fraction2 = bruch()
        operator = random.choice(operators)

        print(f"Was ergibt {fraction1} {operator} {fraction2}?")
        user_input = input("Deine Antwort: ")

        user_fraction = parse_fraction(user_input)
        if user_fraction is not None:
            user_antwort_decimal, user_antwort_fraction = antwort_berechnen(fraction1, fraction2, operator)
            if user_fraction == user_antwort_fraction:
                print("Super! Richtig!")
                score += 1
            else:
                print(f"Falsch! Die richtige Antwort ist {user_antwort_decimal} oder {user_antwort_fraction}.")
        else:
            print("Ungueltige Eingabe. Bitte geben Sie eine gueltige Bruch- oder Dezimalzahl ein.")

        print()

    print(f"Quiz abgeschlossen! Du hast {score}/{num_Frage} richtig! Gut gemacht!")

if __name__ == "__main__":
    main()
