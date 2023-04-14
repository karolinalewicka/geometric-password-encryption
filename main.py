import math
from decimal import *

getcontext().prec = 1000


def get_coefficients(P, Q):
    a = Q[1] - P[1]
    b = P[0] - Q[0]
    c = a * (P[0]) + b * (P[1])
    return Decimal(-a) / Decimal(b), Decimal(c) / Decimal(b)


def compare(a, b):
    return math.isclose(a, b, rel_tol=1e-100)


class Validator:
    def __init__(self):
        self.alphabet = None
        self.order = None

    def set_alphabet(self, text):
        words = text.split()[1:]
        if not len(words) % 2 == 0:
            raise RuntimeError("Wrong alphabet input")
        local_alphabet = {}
        local_order = []
        for i in range(0, len(words) // 2):
            left_index = 2 * i
            right_index = 2 * i + 1
            key = words[left_index]
            local_order.append(key)
            try:
                value = int(words[right_index])
            except ValueError:
                raise RuntimeError("Wrong value provided")
            local_alphabet[key] = value
        self.alphabet = local_alphabet
        self.order = local_order

    def get_letter(self, index):
        return self.order[index]

    def process_points(self, points, password):
        output = []
        for index, p in enumerate(points):
            if (index + 1) in password.keys():
                output.append([p[0], p[1] + password[index + 1]])
        if len(output) == 0:
            raise RuntimeError("Wrong password given")
        return output

    def validate(self, text):
        words = text.split()[1:]
        identifier = words[0]
        if len(words) <= 1:
            raise RuntimeError("Not enough data")
        cross = Decimal(words[1])

        remaining = words[2:]
        points = []
        password = {}
        for word in remaining:
            if word[0] == "(" and word[-1] == ")":
                points.append(word)
        for word in points:
            remaining.remove(word)

        def convert_to_point(txt):
            data = txt[1:][:-1]
            values = [Decimal(v) for v in data.split(",")]
            return [values[0], values[1]]

        points = [convert_to_point(p) for p in points]

        assert len(remaining) % 2 == 0
        for i in range(0, len(remaining) // 2):
            left_index = 2 * i
            right_index = 2 * i + 1
            key = remaining[left_index]
            value = int(remaining[right_index])
            if not key in self.alphabet:
                raise RuntimeError(f"'{key}' not in alphabet")
            password[value] = self.alphabet[key]

        translated_points = self.process_points(points, password)
        first_point = translated_points[0]
        second_point = translated_points[1]
        line_coefs = get_coefficients(first_point, second_point)

        a = line_coefs[0]
        b = line_coefs[1]

        points_to_check = translated_points
        for point_to_check in points_to_check:
            x = point_to_check[0]
            y = point_to_check[1]
            result = a * x + b  # - y
            if not compare(result, y):
                return False

        if not compare(cross, b):
            return False

        return True


def main():
    validator = Validator()
    while True:
        text = input()
        words = text.split()
        assert len(words) > 0
        command = words[0]
        if command == "KONIEC":
            break
        elif command == "ALFABET":
            try:
                validator.set_alphabet(text)
            except RuntimeError as e:
                print("BLAD")
        elif command == "SPRAWDZ":
            try:
                result = validator.validate(text)
                print(f"{words[1]} {'Ok' if result else 'NotOk'}")
            except RuntimeError as e:
                print("BLAD")



if __name__ == "__main__":
    main()

