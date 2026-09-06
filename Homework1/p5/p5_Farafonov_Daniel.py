def caesar_cipher(text, shift):
    result = ""
    for i in range(len(text)):
        ch = text[i]
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


def caesar_decipher(cyphertext, shift):
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    freq = {}
    for ch in text.lower():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
    return freq


def main():
    text = input("Enter your message: ")
    shift = int(input("Enter shift value: "))

    ciphered = caesar_cipher(text, shift)
    print("Ciphered text:", ciphered)

    freq = letter_frequency(text)
    print("Letter frequency:", freq)

    deciphered = caesar_decipher(ciphered, shift)
    print("Deciphered text:", deciphered)


if __name__ == "__main__":
    main()
