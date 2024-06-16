import sys

if __name__ == "__main__":
    print("This is a test file.")
    print("This are the arguments passed to the script:")
    print(sys.argv)
    print("This is the name of the script:")
    print(sys.argv[0])
    print("This is the first argument:")
    print(sys.argv[1])
    print("This is the second argument:")
    print(sys.argv[2])
    print("This is the third argument:")
    print(sys.argv[3])
    sys.exit(0)