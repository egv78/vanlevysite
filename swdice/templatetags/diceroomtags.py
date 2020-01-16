from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_range(value):
    return range(value)


@register.filter
def split_string(string):
    faces_list = string.split(",")
    return faces_list


@register.filter
def split_name(string):
    display_name = ""
    words = ["Name:"]
    word = ""
    stripped = string.lstrip()
    short_name = stripped
    # short_name = stripped[:45]
    i = 0
    while i < len(short_name):
        char = short_name[i]
        if char.isspace():
            words.append(word)
            word = ""
        else:
            word += char
        i += 1
    words.append(word)
    del words[0]

    lines = 4
    max_breaks = lines - 1
    max_word_length = 9
    line_breaks = 0
    line = ""
    line_chars = 0
    i = 0
    while i < len(words) and line_breaks < lines:
        word = words[i]
        space_left = max_word_length - line_chars
        if i + 1 < len(words):
            next_word = words[(i + 1)]
        else:
            next_word = ""

        if len(word) <= space_left and line_breaks <= (lines - 2):
            # word fits in line and not last line
            # add word; update counters
            line += word
            line_chars += len(word)
            space_left = max_word_length - line_chars
            # test for next word
            if next_word != "":
                if ((len(next_word)) <= (space_left - 1)) or\
                        ((len(next_word) > max_word_length) and space_left > 3):
                    # next word will fit or be cut and part inserted
                    line += " "
                    line_chars += 1
                    i += 1
                    # no new line
                else:
                    # add line to display name; reset line counter; increment word; add new line
                    line += " "
                    display_name += line
                    line_chars = 0
                    line = ""
                    i += 1
                    line_breaks += 1
            else:
                # last word in name; incrementing i pops out of while
                display_name += line
                i += 1
        elif len(word) > max_word_length and space_left > 3 and line_breaks <= (lines - 2):
            # split word;
            cut = space_left - 1
            front, end = word[:cut], word[cut:]
            words[i] = front
            words.insert(i+1, end)
            line += " "
            line += front
            line += '- '
            display_name += line
            line = ""
            line_chars = 0
            line_breaks += 1
            i += 1
        elif line_breaks <= (lines - 2):
            display_name += line
            if line_breaks == max_breaks:
                display_name += "..."
            line = ""
            line_chars = 0
            line_breaks += 1
        else:
            # in last line
            if next_word == "":
                if len(word) < space_left:
                    line += word
                    display_name += line
                    line_breaks += 1
                else:
                    cut = space_left - 4
                    front = word[:cut]
                    line += front + "..."
                    display_name += line
                    line_breaks += 1
            elif space_left > 3:
                if len(word) > space_left:
                    cut = space_left - 3
                    front = word[:cut]
                    line += front + "..."
                    display_name += line
                    line_breaks += 1
                else:
                    line += word + " "
                    line_chars += len(word) + 1
                    i += 1
            else:
                spaces_to_delete = 3 - space_left
                end = line
                length = len(line)
                line = end[:(length - spaces_to_delete)]
                line += "..."
                display_name += line
                line_breaks += 1

    return display_name