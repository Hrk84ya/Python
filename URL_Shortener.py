import pyshorteners


def shorten_url(url):
    """Shorten a URL using TinyURL via pyshorteners."""
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)


def main():
    print()
    print("#################################")
    print("|    Python URL Shortener       |")
    print("#################################")
    print()

    while True:
        url = input("Enter a URL to shorten (or 'exit' to quit): ").strip()

        if url.lower() == "exit":
            print("Goodbye!")
            break

        if not url:
            print("Please enter a valid URL.\n")
            continue

        try:
            short = shorten_url(url)
            print(f"Shortened URL: {short}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
