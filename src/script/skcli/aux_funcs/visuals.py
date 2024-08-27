def padded_print(*contents, tab=0, tab_width=2):
    """Enables tabbing for lines"""
    """Accepts either str/str_lists of *args"""
    for content in contents:
        if isinstance(content, list):
            for line in content:
                print('| '+' '*tab*tab_width+str(line))
        elif isinstance(content, str):
            print('| '+' '*tab*tab_width+str(content))

def get_label_aligned_lines(labels, sep, contents):
    """Zips each 'label' to a 'content' separedet by 'sep', which forms a line."""
    formatted_lines = []
    mini_prompt = ''
    right_padding = max([len(label) for label in labels]) + len(mini_prompt)
    for i, label in enumerate(labels):
        formatted_lines.append(f"{label+mini_prompt:<{right_padding}} {sep} {contents[i]}")
    return formatted_lines

def get_n_columns_from_elements(elements, ncol, col_width=None):
    col_width = float('inf') if not col_width else col_width
    # Initialize columns as a dictionary of empty lists
    cols = {i: [] for i in range(1, ncol+1)}

    # Distribute the elements into columns
    for i, element in enumerate(elements):
        col_num = (i // (len(elements) // ncol + (len(elements) % ncol > 0))) + 1
        cols[col_num].append(element)

    # Determine the actual width of each column based on the longest word

    actual_col_widths = {}
    for col in cols:
        # Verifica si cols[col] está vacío
        if cols[col]:
            actual_col_width = min(max(len(word) for word in cols[col]), col_width)
        else:
            actual_col_width = 0  # o cualquier valor predeterminado que elijas

        actual_col_widths[col] = actual_col_width

    # Truncate words in each column if they exceed the max col_width
    for col, words in cols.items():
        cols[col] = [word if len(word) <= actual_col_widths[col] else word[:actual_col_widths[col]-3] + '...' for word in words]

    # Find the maximum number of rows needed
    max_rows = max(len(cols[col]) for col in cols)

    formatted_lines = []
    # Print the columnized output
    for row in range(max_rows):
        line = ""
        for col in range(1, ncol+1):
            word = cols[col][row] if row < len(cols[col]) else ""
            # Print each word right-aligned within its column width
            line += f"{word:<{actual_col_widths[col]}}  "
        formatted_lines.append(line.rstrip())
    return formatted_lines

