def add(numbers:list [int | float]) -> int | float:
    res = 0
    for i in numbers:
        res += i
    return res

def subtract(numbers: list [int | float]) -> int | float:
    if len(numbers) == 0:
        return 0
    res = numbers[0]
    for i in range(1, len(numbers)):
        res -= numbers[i]
    return res

def multiplication(numbers: list [int | float]) -> int | float:
    res = 1
    for i in numbers:
        res *= i
    return res

def divide(numbers: list [int | float]) -> int | float:
    if len(numbers) == 0:
        return 0
    res = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        res /= numbers[i]
    return res


