import random

WORDS = [
    "python", "javascript", "hangman", "programming", "developer",
    "keyboard", "monitor", "algorithm", "function", "variable",
    "database", "terminal", "compiler", "software", "hardware",
    "network", "internet", "browser", "framework", "library"
]

STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    """,
]


def play():
    """Run a single game of Hangman."""
    word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = len(STAGES) - 1

    print("\nLet's play Hangman!")

    while wrong_guesses < max_wrong:
        display = " ".join(ch if ch in guessed_letters else "_" for ch in word)
        print(STAGES[wrong_guesses])
        print(f"  Word: {display}")
        print(f"  Guessed: {', '.join(sorted(guessed_letters)) if guessed_letters else 'none'}")
        print(f"  Attempts left: {max_wrong - wrong_guesses}")

        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"Nice! '{guess}' is in the word.")
            if all(ch in guessed_letters for ch in word):
                print(f"\nYou win! The word was: {word}")
                return
        else:
            wrong_guesses += 1
            print(f"Nope! '{guess}' is not in the word.")

    print(STAGES[wrong_guesses])
    print(f"\nGame over! The word was: {word}")


def main():
    print()
    print("#################################")
    print("|       Python Hangman          |")
    print("#################################")

    while True:
        play()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
