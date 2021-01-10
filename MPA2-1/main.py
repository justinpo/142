from polynomial import *


def moveBracketPos(code: str, bracketPos: int) -> int:
    return code.find("}", bracketPos + 1)


def extractFor(code: str) -> str:
    forPos: int = code.find("for")
    bracketPos: int = code.find("}")

    # if there is a conditional, move the closing bracket position
    if bracketPos > code.find("if") and code.find("if") != -1:
        bracketPos = moveBracketPos(code, bracketPos)

        if "else" in code:
            bracketPos = moveBracketPos(code, bracketPos)

    return code[forPos : bracketPos + 1] if forPos != -1 and bracketPos != -1 else ""


def extractConditional(code: str) -> str:
    ifPos: int = code.find("if")
    bracketPos: int = code.find("}")

    # if there is a loop, move the closing bracket position
    if bracketPos > code.find("for") and code.find("for") != -1:
        bracketPos = moveBracketPos(code, bracketPos)

    if "else" in code:
        bracketPos = moveBracketPos(code, bracketPos)

        if bracketPos > code.find("for") and code.find("for") != -1:
            bracketPos = moveBracketPos(code, bracketPos)

    return code[ifPos : bracketPos + 1] if ifPos != -1 and bracketPos != -1 else ""


def handleFor(code: str) -> str:
    timeComplexity: str = ""

    if "if" in code:
        ifPortion = extractConditional(code)
        code = code.replace(ifPortion, "")
        timeComplexity += handleConditional(ifPortion) + "+"

    loop: Loop = Loop(code)
    loopTime = loop.getTimeComplexity()

    timeComplexity += loopTime

    return timeComplexity


def handleConditional(code: str) -> str:
    timeComplexity: str = ""
    condition: str = code.split("(")[1].split(")")[0]
    ifProcesses: str = code.split(")")[1]
    elseProcesses: str = ""

    if "else" in ifProcesses:
        elseProcesses = ifProcesses.split("else")[1]
        ifProcesses = ifProcesses.split("else")[0]

    ifComplexity: int = getLineCount(ifProcesses)
    elseComplexity: int = getLineCount(elseProcesses)
    timeComplexity = (
        str(ifComplexity) if ifComplexity > elseComplexity else str(elseComplexity)
    )
    timeComplexity += "+" + str(getLineCount(condition))

    return timeComplexity


def main():
    cases: int = int(input())
    infinite: bool = False
    timeComplexity: str = ""
    code: str = ""
    forLoop: str = ""
    ifPortion: str = ""
    time: str = ""
    processes: str = ""
    processesTime: int = 0

    # get input
    for x in range(cases):
        code += input()

    # remove whitespace
    code = removeWhitespace(code)

    # if there is both a loop and conditional in the code
    if code.find("for") != -1 and code.find("if") != -1:
        # if the loop happens before the conditional
        if code.find("for") < code.find("if"):
            forLoop = extractFor(code)
            code = code.replace(forLoop, "")
            timeComplexity += handleFor(forLoop)

            if len(extractConditional(code)) > 0:
                ifPortion = extractConditional(code)
                code = code.replace(ifPortion, "")
                timeComplexity += "+" + handleConditional(ifPortion)

            processesTime = getLineCount(processes)

            if processesTime > 0:
                timeComplexity += "+" + str(processesTime)
        # if the conditional happens before the loop
        elif code.find("if") < code.find("for"):
            if len(extractFor(code)) > 0:
                forLoop = extractFor(code)
                code = code.replace(forLoop, "")
                timeComplexity += handleFor(forLoop) + "+"

            ifPortion = extractConditional(code)
            code = code.replace(ifPortion, "")
            timeComplexity += handleConditional(ifPortion)

            if processesTime > 0:
                timeComplexity += "+" + str(processesTime)

    # if there is only a for loop
    elif "for" in code:
        forLoop = extractFor(code)
        processes += code.split("for")[0]
        processesTime = getLineCount(processes)
        timeComplexity += handleFor(forLoop)

        if processesTime > 0:
            timeComplexity += "+"
            timeComplexity += str(processesTime)
    # if there is only a conditional statement
    elif "if" in code:
        ifPortion = extractConditional(code)
        processes += code.split("if")[0]

        if "else" in code:
            processes += code.split("}")[2]
        else:
            processes += code.split("}")[1]

        processesTime = getLineCount(processes)
        timeComplexity += handleConditional(ifPortion)

        if processesTime > 0:
            timeComplexity += "+" + str(processesTime)
    # if there is no loop or conditional
    else:
        timeComplexity += getLineCount(code)

    if timeComplexity == "infinite":
        infinite = True

    if not infinite:
        poly = Polynomial(timeComplexity)
        poly.simplify()
        print("T(n) = " + str(poly))
    else:
        print("T(n) = infinite")


if __name__ == "__main__":
    main()