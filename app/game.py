from random import randint, choice


def makeEquation(digits, problemType):
    a = randint(1, 10**digits - 1)
    b = randint(1, 10**digits - 1)

    match problemType:
        case "+-":
            return addSub(a, b)
        case "*":
            return multiply(a, b)
        case "/":
            return divide(a, b)


def addSub(a, b):
    operator = choice(["+", "-"])
    equation = f"{a} {operator} {b}"

    return equation


def multiply(a, b):
    equation = f"{a} * {b}"
    return equation


def divide(a, b):
    equation = f"{a} / {b}"
    return equation
