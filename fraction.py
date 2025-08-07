from typing import Union
import math


class Fraction:
    def __init__(self, numerator: int | float | str = 0, denominator: int = 1):
        if denominator == 0:
            raise ZeroDivisionError("Error raised by Fraction class' constructor")
        if isinstance(numerator, str):
            f = Fraction.from_str(numerator)
            self.num = f.num
            self.den = f.den
        else:
            self.num = int(numerator)
            power_of_ten: int = 1
            while self.num != numerator:
                numerator *= 10
                power_of_ten = power_of_ten * 10
                self.num = int(numerator)
            self.den = power_of_ten * denominator
            self.simplify()

    def simplify(self):
        greatest_common_divisor = math.gcd(self.num, self.den)
        self.num //= greatest_common_divisor
        self.den //= greatest_common_divisor
        if self.den < 0:  # Ensure denominator is positive
            self.num *= -1
            self.den *= -1

    @classmethod
    def from_str(cls, fraction_as_string: str) -> "Fraction":
        numerator, denominator = fraction_as_string.split("/")
        numerator = int(numerator)
        denominator = int(denominator)
        return Fraction(numerator, denominator)

    def __add__(self, other: "Fraction") -> "Fraction":
        num = self.num * other.den + other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __sub__(self, other: "Fraction") -> "Fraction":
        num = self.num * other.den - other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __mul__(self, other: "Fraction") -> "Fraction":
        num = self.num * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __truediv__(self, other: "Fraction") -> "Fraction":
        if other.num == 0:
            raise ZeroDivisionError("Error raised by division operator")
        num = self.num * other.den
        den = self.den * other.num
        return Fraction(num, den)

    def __eq__(self, other: Union["Fraction", int]) -> bool:
        if isinstance(other, Fraction):
            return self.num * other.den == self.den * other.num
        elif isinstance(other, int):
            return self.num == self.den * other
        raise TypeError("Comparasion between Fraction and invalid type")

    def __ne__(self, other: Union["Fraction", int]) -> bool:
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.num}/{self.den}"

    def __repr__(self):
        return f"Fraction({self.num}, {self.den})"


if __name__ == "__main__":
    fraction = Fraction()
    print(fraction)
    fraction = Fraction(3)
    print(fraction)
    fraction = Fraction(2, 5)
    print(fraction)
    fraction = Fraction(2.3)
    print(fraction.num)
    print(fraction)
