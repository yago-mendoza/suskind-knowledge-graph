import cmd 
import datetime

from src.skcli.aux_funcs.visuals import *
from src.skcli.aux_funcs.command_docstrings import *
from src.skcli.aux_funcs.err_mssg import *

from src.skcomponents.search_algorithms import *



class LS_Interface(cmd.Cmd):

    prompt = '>> '
    def __init__(self, listed_nodes, parent_cli, ls_args):
        super().__init__()
        self.ls_node = parent_cli.placeholder.node
        self.listed_nodes = listed_nodes
        self.parent_cli = parent_cli
        self.ls_args = ls_args
        self.response = None
        self.cmdloop()
    
    def do_cd(self, index): # finisehd
        if index.isdigit():
            new_current_node = self.listed_nodes[int(index)-1]
            self.parent_cli._set_node(new_current_node)
            return True
        else:
            print('Index must be digit.')
    
    def do_ls(self, arg=None):

        if arg:
            print("(SYS: arguments for 'ls' are disabled within the edit session)")
        self._update_listed_nodes()
        if not self.listed_nodes:
            print("The set field for the target node is empty.")
        strings_to_display = [f'| {i + 1}. {name}' for i, name in enumerate([node.name for node in self.listed_nodes])]

        if len(self.listed_nodes):
            print(f"Showing {len(self.listed_nodes)}/{len(self.listed_nodes)} results.")

        formatted_lines = get_n_columns_from_elements(strings_to_display, ncol=self.ls_args.ncol, col_width=self.ls_args.width)
        for line in formatted_lines:
            print(line)

    def do_clear(self, arg):

        field_symb = self.parent_cli.placeholder.fields[0]
        field = ('synset' if field_symb[0] == 'y' else 'semset') + field_symb[1]

        ch = input(f'SYS: Are you sure you want to clear this field? [Y/N]\n>> ')
        if ch in {'Y','y'}:
            for node in self.listed_nodes:
                self.parent_cli.G.unbind(self.ls_node, node, field)
            print('Field succesfully cleared.')
            return True
        else:
            print('Cleansing process aborted.')
            

    def do_del(self, idxs):

        # revisar que tire

        idxs = [int(_) for _ in idxs.split()]
        unbind_cases = []
        for idx in idxs:
            target_node = self.listed_nodes[idx-1]
            field_symb = self.parent_cli.placeholder.fields[0]
            field = ('synset' if field_symb[0] == 'y' else 'semset') + field_symb[1]
            unbind_cases.append((target_node, field))
        for unbind_case in unbind_cases:
            self.parent_cli.G.unbind(self.ls_node, unbind_case[0], unbind_case[1])

        padded_print(f"Deleted {len(idxs)} nodes.")

        self.do_ls()
    
    def do_grab(self, idxs):
        idxs = [int(_) for _ in idxs.split()]
        for idx in idxs:
            target_node = self.listed_nodes[idx-1]
            if target_node not in self.parent_cli.grabbed_nodes:
                self.parent_cli.grabbed_nodes.append(target_node)
        padded_print(f'Grabbed {len(idxs)} nodes.')

    def do_add(self, name):

        def capitalize_name(name):
            return name[0].upper() + name[1:] if name else None

        def select_node(name):
            matched_nodes = self.parent_cli.G.select(name=name)
            if matched_nodes:
                header_statement = "Did you mean..."
                tail_statement = "(Press Enter to select none)"
                formatted_nodes = [node._convert_header_to_compact_format() for node in matched_nodes]
                SelectInterface(formatted_nodes, self, header_statement, tail_statement).cmdloop()
                response = self._get_response()
                return matched_nodes[int(response)-1] if response else None
            return None

        def create_node():
            user_input = input("| Do you want to create this node? [Y/N] : ").strip().lower()
            if user_input in ['y']:
                creation_input = input("   | Enter <lang> <type> <lemma> in this format:\n   > ")
                parts = creation_input.split()
                if len(parts) >= 2:
                    return parts[0], parts[1], ' '.join(parts[2:]) or 'NA'
            return None, None, None

        def bind_node(current_node, selected_node, edge_type):
            if selected_node and not selected_node in current_node.get_neighbors(edge_type):
                self.parent_cli.G.bind(current_node, selected_node, edge_type)
                print(f"| Successfully binded '{selected_node.name}'.")
            elif selected_node:
                print('| The node was already present.')

        while name:
            name = capitalize_name(name)
            selected_node = select_node(name)

            if not selected_node:
                lang, type, lemma = create_node()
                if lang and type and len(lang) == 2 and len(type) == 1:
                    if not self.parent_cli.G.select(lang=lang, type=type, name=name, lemma=lemma):
                        self.parent_cli.G.create_node(lang, type, name, lemma)
                        selected_node = self.parent_cli.G.select(lang=lang, type=type, name=name, lemma=lemma)[0]
                        print("| Node created.")
                    else:
                        print('| The specified set of characteristics already exists.')
                elif lang or type or lemma:
                    print('Failed to validate hash attributes.')

            if selected_node:
                bind_node(self.ls_node, selected_node, self.parent_cli.placeholder.fields[0])

            name = input(">> add ")

        print('(SYS: Resumed edit-session)')

    # Q1. This function is critical, and my life depends on its behavior. I need you to refactor it intelignetly to occupy less lines, but to keep the original behavior intact. It has to continue running. Please. Refactor it elegantly. Respect all prints too. Everything, except structure, so refactor it.
    # Q2. Also, how to avoid '>>> tf' from breaking (no arguments) without adding deeper tabs. That is : how to stop the execution of a command because arguments are not as expected, to avoid the app to break.

    def do_tf(self, arg):
        
        def _parse_command(parts):
            idxs = [int(part) for part in parts if part.isdigit()]
            fields = [part for part in parts if part[0] in 'ye']
            name_index = next((i for i, part in enumerate(parts) if not part.isdigit()), len(parts))
            field_index = next((i for i, part in enumerate(parts) if part in fields), len(parts))
            return idxs, " ".join(parts[name_index:field_index]), fields

        args = arg.split()
        if not args:
            return print('Not enough arguments.')

        idxs, node_name, fields = _parse_command(args)
        fields = fields or self.parent_cli.placeholder.fields
        nodes_to_be_transferred = [self.listed_nodes[i-1] for i in idxs] if idxs else self.listed_nodes
        if idxs and max(idxs) >= len(self.listed_nodes):
            return print('Indexes exceed dimensions.')

        homologous = self.parent_cli.G.select(name=node_name)
        if not nodes_to_be_transferred:
            return

        match_node = None
        if len(homologous) == 1:
            match_node = homologous[0]
        elif homologous:
            SelectInterface([node._convert_header_to_compact_format() for node in homologous], 
                            self, f"Found {len(homologous)} homologous.",
                            "(Select the node to which to transfer the connections)", '>> ').cmdloop()
            response = self._get_response()
            match_node = homologous[int(response)-1] if response.isdigit() else None

        initialNeighborCount = len(match_node._get_raw_content())

        if match_node:
            for node in nodes_to_be_transferred:
                for field in fields:
                    self.parent_cli.G.bind(match_node, node, field)
            finalNeighborCount = len(match_node._get_raw_content())
            N = len(nodes_to_be_transferred) * len(fields)
            n = finalNeighborCount - initialNeighborCount
            diff = (finalNeighborCount-initialNeighborCount)/initialNeighborCount*100
            print(f"Transferred {n}/{N} (+{round(diff,2)}%) connections to '{node_name}' at {fields} field(s).")
        else:
            print('Transfer process aborted.')

    def do_cp(self, arg):

        args = arg.split()
        idxs = [int(i) for i in args if i.isdigit()]
        
        if not idxs:
            target_nodes = self.listed_nodes
        else:
            target_nodes = [self.listed_nodes[i-1] for i in idxs]

        target_fields = [i for i in args if i.isalnum() and not i.isdigit()]

        initialNeighborCount = len(self.ls_node._get_raw_content())

        for target_field in target_fields:
            for node in target_nodes:
                self.parent_cli.G.bind(self.ls_node, node, target_field)
        
        finalNeighborCount = len(self.ls_node._get_raw_content())

        N = len(target_nodes)
        n = finalNeighborCount - initialNeighborCount
        diff = (finalNeighborCount-initialNeighborCount)/initialNeighborCount*100 
        print(f"Copied nodes to {target_fields} fields (+{round(diff,2)}%).")

    def do_mv(self, arg):

        args = arg.split()
        idxs = [int(i) for i in args if i.isdigit()]

        if not idxs:
            target_nodes = self.listed_nodes
        else:
            target_nodes = [self.listed_nodes[i-1] for i in idxs]
            
        target_fields = [i for i in args if i.isalnum() and not i.isdigit()]

        for target_field in target_fields:
            for node in target_nodes:
                self.parent_cli.G.bind(self.ls_node, node, target_field)

                field_to_remove_from = self.parent_cli.placeholder.fields[0]
                self.parent_cli.G.unbind(self.ls_node, node, field_to_remove_from)

        print(f"Moved {len(target_nodes)} nodes to {target_fields} fields.")

    def default(self, line):
        line = line.strip()
        if line[0] in {'y', 'e'} and line[1] in {'0', '1', '2'} and len(line)==2:
            self.parent_cli.placeholder.fields = []
            self.parent_cli.placeholder.update_field('add', line)
            self.do_ls()
        else:
            padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)

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

    def cmdloop(self, intro=None):
        super().cmdloop(intro)

    def _get_response(self, reset_response=True):
        # Gets and decides wether it resets the response or not (by default, it does)
        res, self.response = self.response, None if reset_response else self.response
        return res

    def _update_listed_nodes(self):
        self.listed_nodes = list(self.ls_node.get_neighbors(self.parent_cli.placeholder.fields))
        # We update internal object self.listed_nodes to reflect changes that might have been made during the session
        self.listed_nodes = sorted(self.listed_nodes, key=lambda node: node.name)
        # We sort these nodes for readibility (by name)    
    
class NW_Interface(cmd.Cmd):

    prompt = '<Name> : '
    def __init__(self, parent_cli):
        super().__init__()
        self.parent_cli = parent_cli
        self.default_lang = 'es'
        self.default_type = 'n'
        self.response = None
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

        def is_valid_language_code(code):
            return len(code) == 2 and code.isalpha() and code.islower()

        def is_valid_type_code(code):
            return len(code) == 1 and code.isalpha() and code.islower()

        def capitalize_name(name):
            return name[0].upper() + name[1:] if name else None

        def find_homologous(name):
            return self.parent_cli.G.select(name=name, lang=self.default_lang, type=self.default_type)

        def handle_homologous_response(homologous, name):
            statement_1 = f"Found {len(homologous)} homologous."
            statement_2 = "(Enter 'lemma' to create a new meaning or press Enter to move on.)"
            formatted_nodes = [node._convert_header_to_compact_format() for node in homologous]
            SelectInterface(formatted_nodes, self, statement_1, statement_2, 'Lemma: ').cmdloop()
            response = self._get_response()
            
            if isinstance(response, str) and not response.isdigit():
                if response not in [node.lemma for node in homologous]:
                    self.parent_cli.G.create_node(lang=self.default_lang, type=self.default_type, name=name, lemma=response)
                    print(f"| Created [{self.default_lang}][{self.default_type}][{name}]@[{response}]")
                else:
                    print("Already existing. Did nothing.")

        def create_node_with_default_lemma(name):
            lemma = "NA"
            self.parent_cli.G.create_node(lang=self.default_lang, type=self.default_type, name=name, lemma=lemma)
            print(f"| OK : [{self.default_lang}][{self.default_type}][{name}]@[{lemma}]")

        self.response = None
        if is_valid_language_code(line):
            self.default_lang = line
        elif is_valid_type_code(line):
            self.default_type = line
        else:
            name = capitalize_name(line)
            homologous = find_homologous(name)
            if homologous:
                handle_homologous_response(homologous, name)
            else:
                create_node_with_default_lemma(name)
        
        self.update_prompt()

    def emptyline(self):
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True

    def _get_response(self, reset_response=True):
        # Gets and decides wether it resets the response or not (by default, it does)
        res, self.response = self.response, None if reset_response else self.response
        return res

class GB_Interface(cmd.Cmd):

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
            help_text = COMMAND_DOCSTRINGS_GB.get(arg)
            if help_text:
                print(help_text)
            else:
                print(f"No help available for '{arg}'.")
        else:
            def get_description_from_docstring(docstring): return docstring.strip().split('\n')[0][8:]
            commands = COMMAND_DOCSTRINGS_GB.keys()
            contents = [get_description_from_docstring(COMMAND_DOCSTRINGS_GB[command]) for command in commands]
            formatted_lines = get_label_aligned_lines(commands, ':', contents)
            padded_print("Available commands:", formatted_lines, tab=0)
    
    def do_rm(self, idxs):
        target_nodes = []
        idxs = [int(_) for _ in idxs.split()]
        for idx in idxs:
            if idx > 0:
                target_nodes.append(self.parent_cli.grabbed_nodes[idx-1])
        for target_node in target_nodes:
            self.parent_cli.grabbed_nodes.remove(target_node)
        print(f"Deleted {len(idxs)} nodes.")
    
    def do_clear(self, arg):
        self.parent_cli.grabbed_nodes = []
        print(f"Cleared grabbed nodes.")
    
    def do_grab(self, arg):
        self.parent_cli.do_grab(arg)

    def do_ls(self, arg):
        self.display()
    
    def emptyline(self):
        # To exit with an empty Enter key press
        print(f"(SYS: Ended edit-session at {datetime.datetime.now().strftime('%H:%M:%S')})")
        return True
    
# POPUP CLIs ----------------------
    
    # These CLIs don't require HELP of any kind.
    
class SelectInterface(cmd.Cmd):

    def __init__(self, options, parent_cli, header_statement="", tail_statement="", prompt='>> '):
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