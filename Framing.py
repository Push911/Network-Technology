from zlib import crc32


def stuff(data):
    output = ""
    countOne = 0
    for number in data:
        if number == "1":
            countOne = countOne + 1
        else:
            countOne = countOne + 0
        output += number
        if countOne == 5:
            countOne = 0
            output += "0"
    return output


def unstuff(data):
    output = ""
    countOne = 0
    for number in data:
        if countOne == 5:
            countOne = 0
            if number != "0":
                print("Error while stuffing")
                return None
        else:
            if number == "1":
                countOne = countOne + 1
            else:
                countOne = countOne + 0
            output += number
    return output


def framing(data):
    code = "01010101"
    crc = stuff(bin(crc32(data.encode()))[2:].zfill(32))
    output = stuff(data)
    return code + output + crc + code


def unframing(data):
    code = "01010101"
    head = data[:8]
    tail = data[-8:]
    codedString = data[8:-40]
    crc = data[-40:-8]
    data = unstuff(codedString)
    crc1 = bin(crc32(data.encode()))[2:].zfill(32)

    if head != code or tail != code or crc != crc1:
        print("Please enter the right file to decode")

    return data


def encode(data, outputFile):
    data = framing(data)
    with open(outputFile, "w") as file:
        file.write(data)


def decode(data, outputFile):
    data = unframing(data)
    with open(outputFile, "w") as file:
        file.write(data)


def main():
    chosenReadFile = input("Type the name of file to read (with extension)")
    chosenOutputFile = input("Type the name of file to write text in (with extension)")
    chose = input("Choose encode or decode a file")

    with open(chosenReadFile, "r") as file:
        data = file.read()
        if chose == "encode":
            encode(data, chosenOutputFile)
        elif chose == "decode":
            decode(data, chosenOutputFile)
        else:
            print("Check if you entered all properly")


if __name__ == "__main__":
    main()
