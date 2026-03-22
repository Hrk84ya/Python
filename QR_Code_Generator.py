import qrcode


def generate_qr(data, filename="qrcode.png"):
    """Generate a QR code image from the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename


def main():
    print()
    print("#################################")
    print("|    Python QR Code Generator   |")
    print("#################################")
    print()

    while True:
        data = input("Enter text or URL to encode (or 'exit' to quit): ").strip()

        if data.lower() == "exit":
            print("Goodbye!")
            break

        if not data:
            print("Please enter some text or a URL.\n")
            continue

        filename = input("Output filename (default: qrcode.png): ").strip()
        if not filename:
            filename = "qrcode.png"
        if not filename.endswith(".png"):
            filename += ".png"

        try:
            saved = generate_qr(data, filename)
            print(f"QR code saved to: {saved}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
