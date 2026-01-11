"""
Assignment 2 - Question 1
Text encryption and decryption stuff
"""

import os

# Function to encrypt one character
def encrypt_char(char, n, m):
    # Check if it is a lowercase letter
    if 'a' <= char <= 'z':
        # First half a-m
        if char <= 'm':
            # Calculate shift amount: n times m
            move = n * m
            # Find position from 'a'
            index = ord(char) - ord('a')
            # Move it, circle around 13 letters
            new_index = (index + move) % 13
            # Make it back to a letter
            return chr(ord('a') + new_index)
        else:
            # Second half n-z
            # This time n plus m
            move = n + m
            # Position from 'n'
            index = ord(char) - ord('n')
            # Move backwards (minus), math handles the negative wrap
            new_index = (index - move) % 13
            return chr(ord('n') + new_index)
            
    # Check if uppercase
    elif 'A' <= char <= 'Z':
        # First half A-M
        if char <= 'M':
            # Rule says go back n spots
            move = n
            index = ord(char) - ord('A')
            new_index = (index - move) % 13
            return chr(ord('A') + new_index)
        else:
            # Second half N-Z
            # Rule says go forward m squared
            move = m ** 2
            index = ord(char) - ord('N')
            new_index = (index + move) % 13
            return chr(ord('N') + new_index)
            
    # Leave other symbols alone
    else:
        return char

# Decrypt function, basically the reverse of encrypt
def decrypt_char(char, n, m):
    # Lowercase
    if 'a' <= char <= 'z':
        # If inside a-m
        if char <= 'm':
            # Encrypt was + (n*m), so decrypt is - (n*m)
            move = n * m
            index = ord(char) - ord('a')
            new_index = (index - move) % 13
            return chr(ord('a') + new_index)
        else:
            # If inside n-z
            # Encrypt was minus, so decrypt is plus
            move = n + m
            index = ord(char) - ord('n')
            new_index = (index + move) % 13
            return chr(ord('n') + new_index)

    # Uppercase
    elif 'A' <= char <= 'Z':
        if char <= 'M':
            # Was back n, now forward n
            move = n
            index = ord(char) - ord('A')
            new_index = (index + move) % 13
            return chr(ord('A') + new_index)
        else:
            # Was forward m^2, now back
            move = m ** 2
            index = ord(char) - ord('N')
            new_index = (index - move) % 13
            return chr(ord('N') + new_index)
            
    # Ignore others
    else:
        return char

# Helper to read and write files
def work_on_file(filename, out_filename, n, m, mode):
    try:
        # Read the file
        f = open(filename, 'r', encoding='utf-8')
        text = f.read()
        f.close()
            
        result_list = []
        # Loop through every char
        for c in text:
            if mode == 'encrypt':
                # Do encryption
                new_c = encrypt_char(c, n, m)
                result_list.append(new_c)
            else:
                # Do decryption
                new_c = decrypt_char(c, n, m)
                result_list.append(new_c)
                
        # Join them all together
        final_text = "".join(result_list)
        
        # Write to the new file
        f_out = open(out_filename, 'w', encoding='utf-8')
        f_out.write(final_text)
        f_out.close()
            
        return True, final_text
    except:
        print("File problem or missing: " + filename)
        return False, ""

def main():
    print("Assignment 2 - Question 1")
    
    # Get inputs, keep it simple
    try:
        s1 = int(input("Enter first number (n/shift1): "))
        s2 = int(input("Enter second number (m/shift2): "))
    except:
        print("That's not a number! Exiting.")
        return

    # Check for raw_text.txt, make one if missing
    if not os.path.exists('raw_text.txt'):
        print("Can't find raw_text.txt, making a test one...")
        f = open('raw_text.txt', 'w')
        f.write("The quick brown fox jumps over the lazy dog.")
        f.close()
    
    # Do encryption
    ok, cipher = work_on_file('raw_text.txt', 'encrypted_text.txt', s1, s2, 'encrypt')
    if ok:
        print("Encryption done. Look at encrypted_text.txt")
        
    # Do decryption
    ok, plain = work_on_file('encrypted_text.txt', 'decrypted_text.txt', s1, s2, 'decrypt')
    if ok:
        print("Decryption done. Look at decrypted_text.txt")
        
    # Check if it worked
    print("\nChecking if decrypt matches original...")
    try:
        f = open('raw_text.txt', 'r', encoding='utf-8')
        orig = f.read()
        f.close()
        
        if orig == plain:
            print("Perfect match! Congratulations!")
        else:
            print("Something is wrong...")
            print("Original:", orig)
            print("Decrypted:", plain)
    except:
        pass

if __name__ == "__main__":
    main()
