import os

def sort_file_lines(filename):
    try:
        # Read the contents of the file
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Sort the lines alphabetically
        sorted_lines = sorted(lines)
        
        # Write the sorted lines back to the file
        with open(filename, 'w') as file:
            file.writelines(sorted_lines)
        
        print(f"Successfully sorted the contents of {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    filename = "file.txt"
    if os.path.exists(filename):
        sort_file_lines(filename)
    else:
        print(f"{filename} does not exist.")