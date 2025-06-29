def get_file():
    file = input("Please enter a file: ")
    return file


def get_binary_file(file_path):
    with open(file_path, "rb") as f:
        byte_data = f.read()

    return byte_data


def encrypt(binary_file, file_path):
    encrypted = bytes(byte ^ 5 for byte in binary_file)

    with open(file_path, "wb") as f:
        f.write(encrypted)


def main():
    file_path = get_file()
    bitstring = get_binary_file(file_path)
    encrypt(bitstring, file_path)
    encrypt(bitstring, file_path)

     
if __name__ == "__main__":
    main()






    


