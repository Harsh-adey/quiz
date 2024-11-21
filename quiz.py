import random

# File paths
REGISTRATION_FILE = "registration.txt"
LOGIN_FILE = "login_details.txt"

# Questions for the quiz
QUESTIONS = [
    {"question": "What is the capital of France?", "options": ["A. Paris", "B. London", "C. Berlin"], "answer": "A"},
    {"question": "What is 5 + 3?", "options": ["A. 5", "B. 8", "C. 10"], "answer": "B"},
    {"question": "Who wrote 'Romeo and Juliet'?", "options": ["A. Charles Dickens", "B. William Shakespeare", "C. Mark Twain"], "answer": "B"},
    {"question": "Which planet is known as the Red Planet?", "options": ["A. Earth", "B. Mars", "C. Jupiter"], "answer": "B"},
    {"question": "What is the boiling point of water?", "options": ["A. 50°C", "B. 100°C", "C. 150°C"], "answer": "B"}
]

# Load user profiles
def load_profiles():
    profiles = {}
    try:
        with open(REGISTRATION_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                profiles[data[3]] = {  # data[3] is username
                    "name": data[0],
                    "enrollment": data[1],
                    "college": data[2],
                    "score": 0,
                }
    except FileNotFoundError:
        pass
    return profiles

# Load login credentials
def load_login_details():
    credentials = {}
    try:
        with open(LOGIN_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                credentials[username] = password
    except FileNotFoundError:
        pass
    return credentials

# Save user profiles
def save_profile(profiles):
    with open(REGISTRATION_FILE, "w") as file:
        for username, details in profiles.items():
            file.write(f"{details['name']},{details['enrollment']},{details['college']},{username}\n")

# Save login credentials
def save_login(credentials):
    with open(LOGIN_FILE, "w") as file:
        for username, password in credentials.items():
            file.write(f"{username},{password}\n")

# User registration
def registration(profiles, credentials):
    print("\n--- Registration ---")
    name = input("Enter your full name: ").strip()
    enrollment = input("Enter your enrollment number: ").strip()
    college = input("Enter your college name: ").strip()
    username = input("Enter your username: ").strip()
    if username in credentials:
        print("Username already exists. Please try logging in.")
        return None
    password = input("Enter your password: ").strip()

    # Save user details
    profiles[username] = {"name": name, "enrollment": enrollment, "college": college, "score": 0}
    credentials[username] = password
    save_profile(profiles)
    save_login(credentials)
    print("Registration successful!")
    return username

# User login
def login(credentials):
    print("\n--- Login ---")
    username = input("Enter username: ").strip()
    if username not in credentials:
        print("Username not found. Please register first.")
        return None
    password = input("Enter password: ").strip()
    if credentials[username] == password:
        print(f"Welcome, {username}!")
        return username
    else:
        print("Incorrect password.")
        return None

# Quiz attempt
def attempt_quiz(username, profiles):
    shuffled_questions = QUESTIONS[:]
    random.shuffle(shuffled_questions)
    score = 0

    print("\n--- Starting the Quiz ---")
    for i, question in enumerate(shuffled_questions, 1):
        print(f"\nQ{i}: {question['question']}")
        for option in question["options"]:
            print(option)
        answer = input("Your answer (A/B/C): ").strip().upper()
        if answer == question["answer"]:
            print("Correct!")
            score += 1
        else:
            print("Wrong.")

    print(f"\nQuiz completed! Your score is {score}/{len(QUESTIONS)}.")
    profiles[username]["score"] = score
    save_profile(profiles)

# Show profile of the user
def show_profile(username, profiles):
    print("\n--- User Profile ---")
    user_data = profiles[username]
    print(f"Name: {user_data['name']}")
    print(f"Enrollment Number: {user_data['enrollment']}")
    print(f"College: {user_data['college']}")
    print(f"Username: {username}")
    print(f"Last Quiz Score: {user_data['score']}/{len(QUESTIONS)}")

# Main menu
def main():
    profiles = load_profiles()
    credentials = load_login_details()
    username = None

    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Attempt Quiz")
        print("4. Show Results")
        print("5. Show Profile")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            username = registration(profiles, credentials)
        elif choice == "2":
            username = login(credentials)
        elif choice == "3":
            if username:
                attempt_quiz(username, profiles)
            else:
                print("Please login first.")
        elif choice == "4":
            if username:
                print(f"\n--- Results ---\nUsername: {username}\nScore: {profiles[username]['score']}/{len(QUESTIONS)}")
            else:
                print("Please login first.")
        elif choice == "5":
            if username:
                show_profile(username, profiles)
            else:
                print("Please login first.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
