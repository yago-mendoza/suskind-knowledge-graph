import cmd 
import argparse

from src.skcli.aux_funcs.visuals import *

class SelectNodeInterface(cmd.Cmd):
    prompt = '>> '

    def __init__(self, nodes, parent_cli):
        super().__init__()
        self.nodes = nodes
        self.parent_cli = parent_cli
        self.display()
    
    def display(self):
        padded_print("Do you mean ...")
        for index, node in enumerate(self.nodes, start=1):
            lang, type, name, lemma = node.identify()
            string_index = str(index).zfill(2 if len(self.nodes)>10 else 1)
            print(f"| {string_index}) [{lang}][{type}][{name}]@[({lemma or ''})]")
        padded_print("(Press Enter without any input to exit)")

    def default(self, line):
        """
        The default method in a cmd.Cmd subclass is called when a command is entered
        that doesn't match any existing do_*
        """
        try:
            index = int(line) - 1  # Convert to zero-based index.
            if 0 <= index < len(self.nodes):
                selected_node = self.nodes[index]
                self.parent_cli._set_node(selected_node)  # Updated line
                return True  # Return to the main CLI.
            else:
                print("Please enter a valid number from the list.")
        except ValueError:
            print("Please enter a number to select a node or just press Enter to exit.")
    
    def emptyline(self):
        # To exit with an empty Enter key press
        return True
    
    def do_exit(self, arg):
        """Exit back to the main interface."""
        return True 