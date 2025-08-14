import random
import string

def generate_password(length, use_letters=True, use_digits=True, use_symbols=True):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "Error: No character types selected."

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    try:
        length = int(input("Enter password length: "))
        use_letters = input("Include letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

        if length <= 0:
            print("Password length must be greater than 0.")
            return

        password = generate_password(length, use_letters, use_digits, use_symbols)
        print("Generated Password:", password)

    except ValueError:
        print("Invalid input. Please enter numeric values where required.")

if __name__ == "__main__":
    main()
