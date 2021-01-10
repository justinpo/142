from enum import Enum


def removeWhitespace(string: str) -> str:
    return string.replace(" ", "").replace(" ", "\r").replace(" ", "\n")


def getLineCount(string: str) -> int:
    count: int = 0
    i: int = 0
    string += " "

    while i < len(string):
        if (
            string[i] == ">"
            or string[i] == "<"
            or string[i] == "="
            or string[i] == "*"
            or string[i] == "/"
            or string[i] == "+"
            or string[i] == "-"
        ):
            if (
                string[i + 1] == ">"
                or string[i + 1] == "<"
                or string[i + 1] == "="
                or string[i + 1] == "*"
                or string[i + 1] == "/"
                or string[i + 1] == "+"
                or string[i + 1] == "-"
            ):
                i += 1

            count += 1

        i += 1

    return count


class VariableType(Enum):
    INT_INT = "INT_INT"
    INT_VAR = "INT_VAR"
    VAR_INT = "VAR_INT"


class ConditionType(Enum):
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN_EQUAL = "LESS_THAN_EQUAL"
    GREATER_THAN_EQUAL = "GREATER_THAN_EQUAL"


class IteratorType(Enum):
    ADD_ONE = "ADD_ONE"
    SUBTRACT_ONE = "SUBTRACT_ONE"
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "MULTIPLY"


class Initializer:
    def __init__(self, string: str):
        self._string = string
        self._var = string[:1]

        pos: int = string.find("=") + 1
        self._value = string[pos:]

    def getVar(self):
        return self._var

    def getValue(self):
        return self._value

    def __str__(self):
        return self._string


class Condition:
    def __init__(self, string: str):
        self._string = string

        exponentCount: int = 1
        modifierEnd: int = (
            string.find(">") if string.find(">") != -1 else string.find("<")
        )

        self._modifier = string[:modifierEnd]
        self._equality = (
            string[len(self._modifier) :][:2]
            if string.find("=") != -1
            else string[len(self._modifier) :][:1]
        )
        modifierEqualityLength: int = len(self._modifier) + len(self._equality)
        self._bound = string[modifierEqualityLength:]

        for ch in self._modifier:
            if ch == "*":
                exponentCount += 1

        if exponentCount > 1:
            self._modifier = self._modifier[0]
            self._modifier += "^"
            self._modifier += str(exponentCount)

    def getModifier(self) -> str:
        return self._modifier

    def getEquality(self) -> str:
        return self._equality

    def getBound(self) -> str:
        return self._bound

    def __str__(self) -> str:
        return self._string


class Iterator:
    def __init__(self, string: str):
        self._value = ""
        self._string = string
        operationStart: int = 0

        for i, ch in enumerate(string):
            if ch == "+" or ch == "-" or ch == "/" or ch == "*":
                operationStart = i
                break

        self._operation = string[operationStart:][:2]

        if len(string) > 3:
            self._value = string[3:]

    def getOperation(self) -> str:
        return self._operation

    def getValue(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._string


class Loop:
    def __init__(self, string: str):
        self._initializer = ""
        self._condition = ""
        self._iterator = ""
        self._processes = ""
        self._timeComplexity = ""
        self._varType = ""
        self._conditionType = ""
        self._iteratorType = ""

        self._initializer = Initializer(string.split("int")[1].split(";")[0])
        self._condition = Condition(string.split(";")[1])
        self._iterator = Iterator(string.split(";")[2].split(")")[0])
        self._processes = string.split("{")[1]
        self.setType()
        self.setTimeComplexity()

    def setType(self) -> bool:
        initializerValue = self._initializer.getValue()
        conditionBound = self._condition.getBound()
        conditionEquality = self._condition.getEquality()
        iteratorOperation = self._iterator.getOperation()

        if initializerValue != "n" and conditionBound != "n":
            self._varType = VariableType.INT_INT
        elif initializerValue != "n" and conditionBound == "n":
            self._varType = VariableType.INT_VAR
        elif initializerValue == "n" and conditionBound != "n":
            self._varType = VariableType.VAR_INT

        if conditionEquality == "<":
            self._conditionType = ConditionType.LESS_THAN
        elif conditionEquality == ">":
            self._conditionType = ConditionType.GREATER_THAN
        elif conditionEquality == "<=":
            self._conditionType = ConditionType.LESS_THAN_EQUAL
        elif conditionEquality == ">=":
            self._conditionType = ConditionType.GREATER_THAN_EQUAL

        if iteratorOperation == "++":
            self._iteratorType = IteratorType.ADD_ONE
        elif iteratorOperation == "--":
            self._iteratorType = IteratorType.SUBTRACT_ONE
        elif iteratorOperation == "+=":
            self._iteratorType = IteratorType.ADD
        elif iteratorOperation == "-=":
            self._iteratorType = IteratorType.SUBTRACT
        elif iteratorOperation == "*=":
            self._iteratorType = IteratorType.MULTIPLY
        elif iteratorOperation == "/=":
            self._iteratorType = IteratorType.DIVIDE

        return True

    def setTimeComplexity(self) -> bool:
        loopTime: int = (
            getLineCount(str(self._condition))
            + getLineCount(str(self._iterator))
            + getLineCount(self._processes)
        )
        a: int = 0
        b: int = 0
        c: int = 0
        constant: int = 0

        # For Logarithms
        if (
            (
                self._varType == VariableType.INT_VAR
                or self._varType == VariableType.VAR_INT
            )
            and (
                self._conditionType == ConditionType.LESS_THAN
                or self._conditionType == ConditionType.LESS_THAN_EQUAL
            )
            and self._iteratorType == IteratorType.MULTIPLY
        ):
            a = int(self._initializer.getValue())
            c = 2 if self._conditionType == ConditionType.LESS_THAN else 1

            self._timeComplexity += (
                str(loopTime) + " log(" + self._iterator.getValue() + ") n"
            )

            constant = (
                -(loopTime * (a - c))
                + getLineCount(str(self._initializer))
                + getLineCount(str(self._condition))
            )

            if constant < 0:
                self._timeComplexity += " - "
                constant *= -1
            else:
                self._timeComplexity += " + "

            self._timeComplexity += str(constant)

        # For Infinites
        elif (
            (
                self._varType == VariableType.INT_INT
                or self._varType == VariableType.INT_VAR
            )
            and (
                self._conditionType == ConditionType.LESS_THAN
                or self._conditionType == ConditionType.LESS_THAN_EQUAL
            )
            and (
                self._iteratorType == IteratorType.SUBTRACT_ONE
                or self._iteratorType == IteratorType.SUBTRACT
                or self._iteratorType == IteratorType.DIVIDE
            )
        ) or (
            self._varType == VariableType.VAR_INT
            and (
                self._conditionType == ConditionType.GREATER_THAN
                or self._conditionType == ConditionType.GREATER_THAN_EQUAL
            )
            and (
                self._iteratorType == IteratorType.ADD_ONE
                or self._iteratorType == IteratorType.ADD
                or self._iteratorType == IteratorType.MULTIPLY
            )
        ):
            self._timeComplexity += "infinite"

        # For Constants
        elif (
            (
                self._varType == VariableType.INT_INT
                or self._varType == VariableType.INT_VAR
            )
            and (
                self._conditionType == ConditionType.GREATER_THAN
                or self._conditionType == ConditionType.GREATER_THAN_EQUAL
            )
            or (
                self._varType == VariableType.VAR_INT
                and (
                    self._conditionType == ConditionType.LESS_THAN
                    or self._conditionType == ConditionType.LESS_THAN_EQUAL
                )
            )
        ):
            self._timeComplexity += "2"

        # For Numerical Bounds
        elif (
            self._varType == VariableType.INT_INT
            and (
                self._conditionType == ConditionType.LESS_THAN
                or self._conditionType == ConditionType.LESS_THAN_EQUAL
            )
            and (
                self._iteratorType == IteratorType.ADD_ONE
                or self._iteratorType == IteratorType.ADD
            )
        ):
            a = int(self._initializer.getValue())
            b = int(self._condition.getBound())
            c = 2 if self._conditionType == ConditionType.LESS_THAN else 1

            if self._iteratorType == IteratorType.ADD_ONE:
                self._timeComplexity += str(
                    (loopTime * (b - (a - c)))
                    + getLineCount(str(self._initializer))
                    + getLineCount(str(self._condition))
                )
            elif self._iteratorType == IteratorType.ADD:
                self._timeComplexity += str(
                    (loopTime * (b - (a - c)) / int(self._iterator.getValue()))
                    + getLineCount(str(self._initializer))
                    + getLineCount(str(self._condition))
                )

        # For Variable Bounds
        elif (
            self._varType == VariableType.INT_VAR
            and (
                self._conditionType == ConditionType.LESS_THAN
                or self._conditionType == ConditionType.LESS_THAN_EQUAL
            )
            and (
                self._iteratorType == IteratorType.ADD_ONE
                or self._iteratorType == IteratorType.ADD
            )
        ):
            a = int(self._initializer.getValue())
            c = 2 if self._conditionType == ConditionType.LESS_THAN else 1

            self._timeComplexity += str(loopTime)

            if self._condition.getModifier().find("^2") != -1:
                self._timeComplexity += " sqrt(n)"
            elif self._condition.getModifier().find("^3") != -1:
                self._timeComplexity += " cubert(n)"
            else:
                self._timeComplexity += "n"

            if a > 0:
                constant = (
                    -(loopTime * (a - c))
                    + getLineCount(str(self._initializer))
                    + getLineCount(str(self._condition))
                )
            else:
                constant = getLineCount(str(self._initializer)) + getLineCount(
                    str(self._condition)
                )

            if (
                self._iterator.getValue() != ""
                and self._iteratorType == IteratorType.ADD
            ):
                self._timeComplexity += "/" + self._iterator.getValue()

            if constant < 0:
                self._timeComplexity += " - "
                constant *= -1
            else:
                self._timeComplexity += " + "

            self._timeComplexity += str(constant)

        return True

    def getTimeComplexity(self) -> str:
        return self._timeComplexity

    def __str__(self):
        string: str = ""
        string += "initializer: " + self._initializer.getValue() + "\n"
        string += (
            "conditions: "
            + self._condition.getModifier()
            + self._condition.getEquality()
            + self._condition.getBound()
            + "\n"
        )
        string += (
            "iterator: "
            + self._iterator.getOperation()
            + self._iterator.getValue()
            + "\n"
        )
        string += "processes: " + self._processes + "\n"
        string += (
            "types: "
            + str(self._varType)
            + " "
            + str(self._conditionType)
            + " "
            + str(self._iteratorType)
        )

        return string
