import sys 
import string

def get_file_as_list():
    file = input("Enter file name please: ")
    
    with open(file, 'r') as f:
        data = f.read()
        translator = str.maketrans("","", string.punctuation)
        data = data.translate(translator)
        data = data.lower()
        return data.split()
    
def count_words(file):
    count = {}
    for word in file:
        if word in count:
            count[word]+=1
        else:
            count[word] = 1
    return count

def print_most_frequent(word_count):
    n = int(sys.argv[1])
    sorted_count = sorted(word_count.items(), key= lambda item: item[1], reverse=True)
    if n <= len(sorted_count):
        for i in range(1, n+1):
            print(f"{i}. Word '{sorted_count[i-1][0]}' {sorted_count[i-1][1]} times")


def main():
    file_list = get_file_as_list()
    count = count_words(file_list)
    print_most_frequent(count)


if __name__ == "__main__":
    main()





    




