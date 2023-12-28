def padded_print(*content):
    for line in content:
        print('| '+str(line))

def columnize(elements, ncol, col_width=None):
    col_width = float('inf') if not col_width else col_width
    # Initialize columns as a dictionary of empty lists
    cols = {i: [] for i in range(1, ncol+1)}

    # Distribute the elements into columns
    for i, element in enumerate(elements):
        col_num = (i // (len(elements) // ncol + (len(elements) % ncol > 0))) + 1
        cols[col_num].append(element)

    # Determine the actual width of each column based on the longest word
    actual_col_widths = {col: min(max(len(word) for word in cols[col]), col_width) for col in cols}

    # Truncate words in each column if they exceed the max col_width
    for col, words in cols.items():
        cols[col] = [word if len(word) <= actual_col_widths[col] else word[:actual_col_widths[col]-3] + '...' for word in words]

    # Find the maximum number of rows needed
    max_rows = max(len(cols[col]) for col in cols)

    # Print the columnized output
    for row in range(max_rows):
        for col in range(1, ncol+1):
            word = cols[col][row] if row < len(cols[col]) else ""
            # Print each word right-aligned within its column width
            print(f"{word:<{actual_col_widths[col]}}", end='  ')
        print()

