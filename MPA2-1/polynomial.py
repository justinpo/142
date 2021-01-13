from loop import *


class Term:
    def __init__(self, string: str):
        self._coefficient = 0
        self._var = ""
        string += " "

        coefPos: int = -1
        for i in range(len(string)):
            if (
                string[i] >= "0"
                and string[i] <= "9"
                and string[i + 1] != ")"
                and string[i - 1] != "/"
            ) or string[i] == "-":
                coefPos += 1
            else:
                self._var += string[i:][:1]

        if coefPos != -1:
            self._coefficient = int(string[: coefPos + 1])

    def setCoefficient(self, coef: int) -> bool:
        self._coefficient = coef

        return True

    def getCoefficient(self) -> int:
        return self._coefficient

    def getVar(self) -> int:
        return self._var

    def __str__(self) -> str:
        string: str = ""

        if self._coefficient != 0:
            string += str(self._coefficient)
        if "log" in self._var:
            self._var = " " + self._var[:6] + " " + self._var[-2:][:1] + " "
        elif "rt(n)" in self._var:
            self._var = " " + self._var

        string += self._var

        return string


class Polynomial:
    def __init__(self, string: str):
        self._polynomial: [Term] = []
        string = removeWhitespace(string)
        temp: str = ""

        for i, ch in enumerate(string):
            if ch != "+" and ch != "-":
                temp += string[i:][:1]
            elif ch == "-":
                term = Term(temp)
                self._polynomial.append(term)
                temp = ""
                temp += string[i:][:1]
            elif ch == "+":
                term = Term(temp)
                self._polynomial.append(term)
                temp = ""

        term = Term(temp)
        self._polynomial.append(term)

    def simplify(self):
        for i in range(len(self._polynomial) - 1):
            if i < len(self._polynomial):
                currCoef: int = self._polynomial[i].getCoefficient()
                currVar: str = self._polynomial[i].getVar()
                j: int = i + 1

                while j < len(self._polynomial):
                    if self._polynomial[j].getVar() == currVar:
                        currCoef += self._polynomial[j].getCoefficient()
                        self._polynomial.remove(self._polynomial[j])
                        j -= 1
                    j += 1

                self._polynomial[i].setCoefficient(currCoef)
            else:
                break

    def __str__(self):
        string: str = ""
        for i, term in enumerate(self._polynomial):
            if term.getCoefficient() < 0 and i > 0:
                term.setCoefficient(term.getCoefficient() * -1)
                string += "- "
            elif term.getCoefficient() > 0 and i > 0:
                string += "+ "
            string += str(term)

        return string