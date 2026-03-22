import random

WORDS = [
    "crane", "slate", "trace", "audio", "raise", "stare", "arise",
    "learn", "resin", "stern", "crate", "parse", "heart", "stone",
    "blaze", "charm", "drift", "flame", "globe", "haste", "joker",
    "knelt", "lemon", "mango", "nerve", "olive", "plumb", "quest",
    "rover", "swift", "tiger", "ultra", "vivid", "whale", "youth",
    "zebra", "brave", "cloud", "dream", "eagle", "frost", "grape",
]

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def color_guess(guess, target):
    """Return a colored string showing correct, misplaced, and wrong letters."""
    result = []
    target_chars = list(target)

    # First pass: mark greens
    marks = [None] * WORD_LENGTH
    for i, ch in enumerate(guess):
        if ch == target_chars[i]:
            marks[i] = "green"
            target_chars[i] = None

    # Second pass: mark yellows
    for i, ch in enumerate(guess):
        if marks[i] is None:
            if ch in target_chars:
                marks[i] = "yellow"
                target_chars[target_chars.index(ch)] = None
            else:
                marks[i] = "gray"

    for i, ch in enumerate(guess):
        if marks[i] == "green":
            result.append(f"{GREEN}{ch.upper()}{RESET}")
        elif marks[i] == "yellow":
            result.append(f"{YELLOW}{ch.upper()}{RESET}")
        else:
            result.append(f"{GRAY}{ch.upper()}{RESET}")

    return " ".join(result)


def play():
    """Run a single game of Wordle."""
    target = random.choice(WORDS)
    attempts = []

    print(f"\nGuess the {WORD_LENGTH}-letter word. You have {MAX_ATTEMPTS} attempts.")
    print(f"  {GREEN}GREEN{RESET} = correct spot | {YELLOW}YELLOW{RESET} = wrong spot | {GRAY}GRAY{RESET} = not in word\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        while True:
            guess = input(f"  Attempt {attempt}/{MAX_ATTEMPTS}: ").strip().lower()
            if len(guess) != WORD_LENGTH:
                print(f"  Please enter a {WORD_LENGTH}-letter word.")
            elif not guess.isalpha():
                print("  Letters only.")
            else:
                break

        colored = color_guess(guess, target)
        attempts.append(colored)

        # Redisplay all guesses
        print()
        for line in attempts:
            print(f"  {line}")
        print()

        if guess == target:
            print(f"  You got it in {attempt} attempt(s)!")
            return

    print(f"  Out of attempts! The word was: {target.upper()}")


def main():
    print()
    print("#################################")
    print("|      Python Wordle Clone      |")
    print("#################################")

    while True:
        play()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
