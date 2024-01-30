import cmd 
import random
import datetime
import argparse

from src.skcli.aux_funcs.visuals import *
from src.skcli.aux_funcs.command_docstrings import *
from src.skcli.aux_funcs.err_mssg import *

from src.skcomponents.search_algorithms import *


class GRABBED_Interface(cmd.Cmd):

    prompt = '>> '
    def __init__(self, parent_cli):
        super().__init__()
        self.parent_cli = parent_cli

        print(f"(SYS: Started edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        self.display()

        self.cmdloop()

    def display(self, represent_bars=True):

        if len(self.parent_cli.grabbed_nodes) == 0:
            print("No nodes grabbed yet.")
        else:
            padded_print(f'Grabbed {len(self.parent_cli.grabbed_nodes)} nodes:')
            algorithm_output = centrality(self.parent_cli.grabbed_nodes)
            sorted_output = dict(sorted(algorithm_output.items(), key=lambda item: item[1], reverse=True))

            self.parent_cli.grabbed_nodes = list(sorted_output.keys()) # to match indexes when accesed via 'rm'
            
            contents = ["{:.4f}".format(round(n,3)) for n in sorted_output.values()]
            formatted_nodes = [f"{i}) {node._convert_header_to_str_format()}"for i, node in enumerate(sorted_output.keys(), start=1)]          
            sep = ':'

            if represent_bars:
                contents = [f'{content} | {"█" * round(float(content) * 20)}' for content in contents]
            padded_print(get_label_aligned_lines(formatted_nodes, sep, contents), tab=1)

    def do_help(self, arg):
        if arg:
            help_text = COMMAND_DOCSTRINGS_GRABBED.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for '{arg}'.")
        else:
            def get_description_from_docstring(docstring): return docstring.strip().split('\n')[0][8:]
            commands = COMMAND_DOCSTRINGS_GRABBED.keys()
            contents = [get_description_from_docstring(COMMAND_DOCSTRINGS_GRABBED[command]) for command in commands]
            formatted_lines = get_label_aligned_lines(commands, ':', contents)
            padded_print("Available commands:", formatted_lines, tab=0)
    
    def do_rm(self, idxs):
        idxs = [int(_) for _ in idxs.split()]
        for idx in idxs:
            if idx > 0:
                target_node = self.parent_cli.grabbed_nodes[idx-1]
            self.parent_cli.grabbed_nodes.remove(target_node)
        print(f"Deleted {len(idxs)} nodes.")
    
    def do_clear(self, arg):
        self.parent_cli.grabbed_nodes = []
        print(f"Cleared grabbed nodes.")
    
    def do_grab(self, arg):
        self.parent_cli.do_grab(arg)

    def do_grabbed(self, arg):
        self.display()
    
    def emptyline(self):
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True

class LS_Interface(cmd.Cmd):

    prompt = '>> '
    def __init__(self, listed_nodes, parent_cli, ls_args):
        super().__init__()
        self.ls_node = parent_cli.placeholder.node
        self.listed_nodes = listed_nodes
        self.parent_cli = parent_cli
        self.ls_args = ls_args
        self.cmdloop()

    def do_del(self, idxs):
        idxs = [int(_) for _ in idxs.split()]
        for idx in idxs:
            target_node = self.listed_nodes[idx-1]
            field_symb = self.parent_cli.placeholder.fields[0]

            field = ('synset' if field_symb[0] == 'y' else 'semset') + field_symb[1]

            self.parent_cli.G.unbind(self.ls_node, field, target_node)

        padded_print(f"Deleted {len(idxs)} nodes.")

    def do_add(self, name):

        if not name:  # Exit add loop if the name is empty
            print("(SYS: 'add' command requires <name> argument)")
 
        else:

            while True:

                if not name:
                    break
                
                name = name[0].upper() + name[1:]
                matched_nodes = self.parent_cli.G.select(name=name)
                selected_node = None

                if len(matched_nodes)>1:
                    selection_interface = SelectInterface(matched_nodes, self, "Did you mean...", "(Press Enter to select none)")
                    selection_interface.cmdloop()
                    selected_index = self.response

                    if selected_index and selected_index.isdigit():
                        selected_node = matched_nodes[int(selected_index) - 1]
                
                if len(matched_nodes)==1:
                    selected_node = matched_nodes[0]

                if not selected_node and input(" "*3+"| Do you want to create this node? [Y/N] : ").strip().lower() in ['Y','y']:
                    creation_input = input(" "*3+"| Enter <lang> <type> <lemma> in this format:\n"+" "*3+'> ')
                    lang, type, *lemma = creation_input.split()
                    lemma = 'NA' if lemma == [] else lemma
                    self.parent_cli.G.create_node(lang, type, name, lemma)
                    selected_node = self.parent_cli.G.select(lang, type, name, lemma)
                    print(" "*3+"| Node created and binded.")

                elif selected_node:
                    current_node = self.ls_node
                    edge_type = self.parent_cli.placeholder.fields[0]

                    field = ('synset' if edge_type[0] == 'y' else 'semset') + edge_type[1]

                    self.parent_cli.G.bind(current_node, field, selected_node)

                name = input(">> add ")
            
            print('(SYS: Resumed edit-session)')

    def do_cp(self, arg):
        args = arg.split()
        indices = [int(i) for i in args if i.isdigit()]
        target_fields = [i for i in args if i.isalnum() and not i.isdigit()]

        target_nodes = [self.listed_nodes[i-1] for i in indices]

        for target_field in target_fields:
            formatted_target_field = self._format_field(target_field)

            # Copiar nodos a los campos objetivo
            for node in target_nodes:
                self.parent_cli.G.bind(self.ls_node, formatted_target_field, node)

        print(f"Copied {len(target_nodes)} nodes to '{', '.join(target_fields)}'.")


    def do_mv(self, arg):

        args = arg.split()
        indices = [int(i) for i in args if i.isdigit()]
        target_fields = [i for i in args if i.isalnum() and not i.isdigit()]

        target_nodes = [self.listed_nodes[i-1] for i in indices]

        for target_field in target_fields:
            formatted_target_field = self._format_field(target_field)

            field_to_remove_from = self.parent_cli.placeholder.fields[0]
            field_to_remove_from = ('synset' if field_to_remove_from[0] == 'y' else 'semset') + field_to_remove_from[1]

            # Copiar nodos a los campos objetivo
            for node in target_nodes:
                self.parent_cli.G.unbind(self.ls_node, field_to_remove_from, node)
                self.parent_cli.G.bind(self.ls_node, formatted_target_field, node)
        
        self._update_listed_nodes()

        print(f"Moved {len(target_nodes)} nodes to '{', '.join(target_fields)}'.")

    def default(self, line):
        line = line.strip()
        if line[0] in {'y', 'e'} and line[1] in {'0', '1', '2'} and len(line)==2:
            self.parent_cli.placeholder.fields = []
            self.parent_cli.placeholder.update_field('add', line)
            self.do_ls()
        else:
            padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)
        
    def _format_field(self, field):
        if field.strip().startswith('y'):
            return 'synset' + field.strip()[1:]
        elif field.strip().startswith('e'):
            return 'semset' + field.strip()[1:]
        else:
            raise ValueError("Invalid field specification")
    
    def cmdloop(self, intro=None):
        super().cmdloop(intro)

    def do_help(self, arg=None):
        """Provide help for a specified command or list all commands if none is specified."""
        if arg:
            # User asked for help on a specific command
            help_text = COMMAND_DOCSTRINGS_LS.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for '{arg}'")
        else:
            # User typed "help" without specifying a command
            padded_print("Available commands:")
            mini_prompt = ''
            right_padding = max([len(command) for command in COMMAND_DOCSTRINGS_LS]) + len(mini_prompt)
            for command in COMMAND_DOCSTRINGS_LS:
                # Only print the first line of each help text for an overview
                first_line = COMMAND_DOCSTRINGS_LS[command].strip().split('\n')[0]
                padded_print(f"{command+mini_prompt:<{right_padding}} : {first_line[8:]}")
        pass
    
    def emptyline(self): #finished
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True

    def do_cd(self, index): # finisehd
        self.parent_cli._set_node(self.listed_nodes[int(index)-1])
        return True

    def _update_listed_nodes(self):
        self.listed_nodes = list(self.ls_node.get_neighbors(self.placeholder.fields))
        # We update internal object self.listed_nodes to reflect changes that might have been made during the session
        self.listed_nodes = sorted(self.listed_nodes, key=lambda node: node.name)
        # We sort these nodes for readibility (by name)

    def do_ls(self, arg=None):
        if arg:
            print("(SYS: arguments for 'ls' are disabled within the edit session)")
        self._update_listed_nodes()
        if not self.listed_nodes:
            print("The set field for the target node is empty.")
        strings_to_display = [f'| {i + 1}. {name}' for i, name in enumerate([node.name for node in self.listed_nodes])]
        get_n_columns_from_elements(strings_to_display, ncol=self.ls_args.ncol, col_width=self.ls_args.width)

class NEW_Interface(cmd.Cmd):

    prompt = '<Name> : '
    def __init__(self, parent_cli):
        super().__init__()
        self.parent_cli = parent_cli
        self.default_lang = 'es'
        self.default_type = 'n'
        self.update_prompt()
        self.display()
        self.cmdloop()

    def update_prompt(self):
        self.prompt = f"[{self.default_lang}][{self.default_type}][<name>] : "
    
    def cmdloop(self, intro=None):
        super().cmdloop(intro)

    def display(self):
        print(f"(SYS: Started create-session at {datetime.datetime.now().strftime('%H:%M:%S')})")

    def do_help(self, arg):
        # estaria bien trasladar esto a command_docstrings.py
        padded_print("Desc. This sub-session allows for the interactive creation of new entries.")
        padded_print("Actions.")
        padded_print("  1. Name")
        padded_print("     Write the intended <name> in the input prompt.")
        padded_print("  2. Target Switch")
        padded_print("     Enter 2-char <lang> or 1-char <type> in the input prompt.")
        padded_print("Circumstance : Homologous Search")
        padded_print("  Upon entering <name>, the system checks for homologous matches (that is,")
        padded_print("  nodes with the same name yet different lang, type or lemma).")
        padded_print("     If found, a menu shows existing nodes, helping users decide whether to")
        padded_print("  add a new one or not (allowing for lemma definition).")
        padded_print("     Otherwise, it will automatically create the node with default lemma 'NA'.")

    def default(self, line):

        self.response = None
        if len(line)==2 and line.isalpha() and line.islower():
            self.default_lang = line
        elif len(line)==1 and line.isalpha() and line.islower():
            self.default_type = line
        else:
            name = line[0].upper() + line[1:]
            homologous = self.parent_cli.G.find(name=name,
                                   lang=self.default_lang,
                                   type=self.default_type)
            if len(homologous) > 0:
                statement_1 = f"Found {len(homologous)} homologous."
                statement_2 = "(Press Enter to move on.)"
                interface_popup = SelectInterface(homologous, self, statement_1, statement_2, 'Lemma: ')
                interface_popup.cmdloop()
                if isinstance(self.response, str):
                    if self.response not in [node.lemma for node in homologous]:
                        self.parent_cli.G.create_node(lang=self.default_lang,type=self.default_type,name=name,lemma=self.response)
                        print(f"OK : [{self.default_lang}][{self.default_type}][{name}]@[{self.response}]")
                    else:
                        padded_print("Already existing. Did nothing.")
            else:
                lemma = "NA"
                self.parent_cli.G.create_node(lang=self.default_lang,type=self.default_type,name=name,lemma=lemma)
                print(f"OK : [{self.default_lang}][{self.default_type}][{name}]@[{lemma}]")
        
        self.update_prompt()

    def emptyline(self):
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True

# POPUP CLIs ----------------------
    
    # These CLIs don't require HELP of any kind.
    
class SelectInterface(cmd.Cmd):

    def __init__(self, options, parent_cli, header_statement="", tail_statement="", prompt='>> '):
        # Requires :
        # - set of options (<Node>s)
        # - statement to be displayed, indicating what can be entered.
        # - reference to the parent_cli to which the resulting option will be sent.
        #   (if [int] is entered -> return the <Node> (at 'n'th position)
        #   (if [str] is entered -> return the <String>)
        #   Note. It returns it by delivering it at .response attr from the parent_cli.
        super().__init__()
        self.options = options
        self.header_statement = header_statement
        self.tail_statement = tail_statement
        self.parent_cli = parent_cli
        self.prompt = prompt
        self.display()
    
    def display(self):
        padded_print(self.header_statement)
        for index, option in enumerate(self.options, start=1):
            string_index = str(index).zfill(2 if len(self.options)>10 else 1)
            padded_print(f"{string_index}) {option}", tab=1)
        padded_print(self.tail_statement)

    def deliver_result(self, response):
        self.parent_cli.response = None
        self.parent_cli.response = response

    def default(self, line):
        """
        The default method in a cmd.Cmd subclass is called when a command is entered
        that doesn't match any existing do_*
        """
        try:
            if isinstance(line, str) and not line.isdigit():
                self.deliver_result(line.strip())
            else:
                index = int(line) - 1  # Convert to zero-based index.
                if 0 <= index < len(self.options):
                    self.deliver_result(line)
                else:
                    print("Please enter a valid index.")
        except ValueError:
            print("Please enter a number to select an option or just press Enter to exit.")
        return True # exits loops
    
    def emptyline(self):
        # To exit with an empty Enter key press
        return True
    
    def do_exit(self, arg):
        return True 