import string
from collections import Counter


def analyze_text(text):
    """Analyze text and return stats including word frequency, reading time, etc."""
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_no_spaces = len(text.replace(" ", ""))
    sentence_count = sum(text.count(p) for p in ".!?") or 1
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()])
    avg_word_length = round(char_no_spaces / word_count, 2) if word_count else 0
    reading_time_min = round(word_count / 200, 1)  # ~200 wpm average
    speaking_time_min = round(word_count / 130, 1)  # ~130 wpm average

    # Word frequency (cleaned, lowercase)
    cleaned_words = [
        w.strip(string.punctuation).lower() for w in words if w.strip(string.punctuation)
    ]
    frequency = Counter(cleaned_words).most_common(10)

    return {
        "word_count": word_count,
        "char_count": char_count,
        "char_no_spaces": char_no_spaces,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_word_length": avg_word_length,
        "reading_time": reading_time_min,
        "speaking_time": speaking_time_min,
        "top_words": frequency,
    }


def display_results(stats):
    """Print the analysis results."""
    print("\n--- Text Analysis Results ---\n")
    print(f"  Words:            {stats['word_count']}")
    print(f"  Characters:       {stats['char_count']}")
    print(f"  Characters (no spaces): {stats['char_no_spaces']}")
    print(f"  Sentences:        {stats['sentence_count']}")
    print(f"  Paragraphs:       {stats['paragraph_count']}")
    print(f"  Avg word length:  {stats['avg_word_length']} chars")
    print(f"  Reading time:     {stats['reading_time']} min")
    print(f"  Speaking time:    {stats['speaking_time']} min")
    print("\n  Top 10 words:")
    for word, count in stats["top_words"]:
        print(f"    {word:20s} {count}")
    print()


def main():
    print()
    print("#####################################")
    print("|   Python Text Analyzer            |")
    print("#####################################")
    print()

    choice = input("Analyze (1) text input or (2) a file? [1/2]: ").strip()

    if choice == "2":
        path = input("Enter file path: ").strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: '{path}' not found.")
            return
    else:
        print("Enter your text (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)

    if not text.strip():
        print("No text provided.")
        return

    stats = analyze_text(text)
    display_results(stats)


if __name__ == "__main__":
    main()
