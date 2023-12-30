def justify_text(text, width):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line) + len(word) + 1 <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    justified_lines = []
    for line in lines:
        words_in_line = line.split()
        total_spaces = width - sum(len(word) for word in words_in_line)
        num_gaps = len(words_in_line) - 1

        if num_gaps == 0:
            justified_lines.append(words_in_line[0] + " " * total_spaces)
        else:
            spaces_between_words = total_spaces // num_gaps
            extra_spaces = total_spaces % num_gaps

            justified_line = ""
            for i, word in enumerate(words_in_line[:-1]):
                justified_line += word + " " * (spaces_between_words + (1 if i < extra_spaces else 0))

            justified_line += words_in_line[-1]
            justified_lines.append(justified_line)

    return '\n'.join(justified_lines)

# Example usage:
text = """Diamond is a solid form of carbon with its atoms arranged in a crystal structure known as diamond cubic. 
It is metastable at standard temperature and pressure, converting to the chemically stable form graphite 
under those conditions but at a negligible rate."""

width = int(input("Enter the width for the line: "))

justified_text = justify_text(text, width)
print(justified_text)
