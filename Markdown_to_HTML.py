import markdown
import sys
import os


def convert_file(input_path, output_path=None):
    """Convert a Markdown file to HTML."""
    if not os.path.isfile(input_path):
        print(f"Error: '{input_path}' not found.")
        return

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".html"

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(input_path)}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f4f4f4; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Converted: {input_path} -> {output_path}")


def main():
    print()
    print("#####################################")
    print("|  Markdown to HTML Converter       |")
    print("#####################################")
    print()

    input_path = input("Enter the Markdown file path: ").strip()

    if not input_path:
        print("No file provided.")
        return

    output_path = input("Output HTML file (leave blank for default): ").strip() or None

    convert_file(input_path, output_path)


if __name__ == "__main__":
    main()
