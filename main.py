import random
import string
import sqlite3
from datetime import datetime

# Initialize database connection and table
def initialize_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_password(length):
    if length < 1:
        return "Password length must be at least 1."
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    all_characters = lowercase + uppercase + digits + special_chars
    
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

# Function to save password to database
def save_password_to_db(password):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO passwords (password, created_at)
        VALUES (?, ?)
    ''', (password, created_at))
    
    conn.commit()
    conn.close()
    print("Password saved to database.")

# Function to view saved passwords
def view_saved_passwords():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, password, created_at FROM passwords')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nSaved Passwords:")
        for row in rows:
            print(f"ID: {row[0]}, Password: {row[1]}, Created At: {row[2]}")
        print()
    else:
        print("No saved passwords found.\n")

def main():
    initialize_db()  # Initialize the database and table
    print("Welcome to the Password Generator!")
    
    while True:
        print("\nMenu:")
        print("1. Generate a new password")
        print("2. View saved passwords")
        print("0. Quit")
        
        try:
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                length = int(input("Enter the desired length of the password: "))
                if length < 1:
                    print("Password length must be at least 1.")
                    continue

                password = generate_password(length)
                print(f"Generated Password: {password}")
                
                # Save the password to the database
                save_password_to_db(password)
            
            elif choice == 2:
                view_saved_passwords()
            
            elif choice == 0:
                print("Exiting the password generator. Goodbye!")
                break
            
            else:
                print("Invalid choice! Please enter 1, 2, or 0.")
        
        except ValueError:
            print("Invalid input! Enter a number.")

if __name__ == "__main__":
    main()
