import math

def get_user_input():
    while(True):
        decimal = int(input("Please enter a decimal: "))
        bits = int(input("Please enter the number of bits: "))
        if decimal > 0 and bits > 0 and math.floor(math.log2(decimal)) + 1 <= bits:
            return decimal, bits
        
def decimal_to_binary(decimal, bits):
    binary = bin(decimal)
    binary = binary[2:].zfill(bits)
    print(binary)
    return binary


def twos_complement(binary):
    opp = "".join("1" if bit == "0" else "0" for bit in binary)
    twos = int(opp, base=2) + 1
    return bin(twos)[2:]


def main():
    decimal, bits = get_user_input()
    binary = decimal_to_binary(decimal, bits)
    twos = twos_complement(binary)
    print(twos)


if __name__ == "__main__":
    main()
