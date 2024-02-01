import cmd 
import datetime

from itertools import combinations

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

        idxs = sk.parse_idxs_to_single_idxs(idxs) # accepts ranges as 5-8 (5,6,7,8)
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
        idxs = sk.parse_idxs_to_single_idxs(idxs) # accepts ranges as 5-8 (5,6,7,8)
        if not idxs:
            idxs = list(range(len(self.listed_nodes)))
        for idx in idxs:
            target_node = self.listed_nodes[idx-1]
            if target_node not in self.parent_cli.grabbed_nodes:
                self.parent_cli.grabbed_nodes.append(target_node)

        padded_print(f'Grabbed {len(idxs)} nodes.')
    
    def do_cross(self, args):
        # Divide los argumentos en índices y tipo de relación
        parts = args.split()
        idxs = ' '.join(parts[:-1])  # Todos menos el último
        relation_type = parts[-1]  # Último argumento

        # Verifica si el tipo de relación es válido
        if relation_type not in ['y', 'e']:
            print("Invalid relation type. Use 'y' or 'e'.")
            return

        # Utiliza la función existente para convertir rangos en índices individuales
        idxs = sk.parse_idxs_to_single_idxs(idxs)

        selected_nodes = [self.listed_nodes[idx - 1] for idx in idxs] if idxs else self.listed_nodes

        # Bindea los nodos seleccionados
        for node1, node2 in combinations(selected_nodes, 2):
            # Bindea cada par de nodos
            self.parent_cli.G.bind(node1, node2, relation_type + '1')

        print(f"Nodes successfully binded with {relation_type + '1'} relationship.")

    def default(self, line):

        line = line.strip()
        if line[0] in {'y', 'e'} and line[1] in {'0', '1', '2'} and len(line)==2:
            self.parent_cli.placeholder.fields = []
            self.parent_cli.placeholder.update_field('add', line)
            self.do_ls()
        
        elif len(line)>2:

            name = line       

            def capitalize_name(name):
                return name[0].upper() + name[1:] if name else None

            def select_node(name):
                
                header_statement = "Did you mean..."
                tail_statement = "(Press Enter to select none)"
                formatted_nodes = [node._convert_header_to_compact_format() for node in matched_nodes]
                SelectInterface(formatted_nodes, self, header_statement, tail_statement).cmdloop()
                response = self._get_response()
                return matched_nodes[int(response)-1] if response else None


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

            name = capitalize_name(name)

            matched_nodes = self.parent_cli.G.select(name=name)

            if matched_nodes:

                if len(matched_nodes) > 1:
                    selected_node = select_node(name)
                else:
                    selected_node = matched_nodes[0]
            
            if not matched_nodes:

                selected_node = None

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
        
        else:
            padded_print(f"Unknown '{line[:4].strip()+'...' if len(line)>5 else line}' command.", CONTEXTUAL_DISCLAIMER)

    def do_mv(self, arg):

        args = arg.split()
        fields = [arg for arg in args if arg in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']]
        idxs = [arg for arg in args if set(arg).issubset(set('0123456789-')) and arg not in fields]
        name = ' '.join([arg for arg in args if arg not in idxs and arg not in fields])
        
        numbers_set = set()
        for part in idxs:
            numbers_set.update(range(int(part.split('-')[0]), int(part.split('-')[-1]) + 1)) if '-' in part else numbers_set.add(int(part))
        idxs = sorted(numbers_set)

        target_nodes = [self.listed_nodes[i-1] for i in idxs] if idxs else self.listed_nodes

        if name:
            homologous = self.parent_cli.G.select(name=name)
            if len(homologous) == 1:
                node = homologous[0]
            else:
                SelectInterface([node._convert_header_to_compact_format() for node in homologous], 
                            self, f"Found {len(homologous)} homologous.",
                            "(Select the node to operate)", '>> ').cmdloop()
                response = self._get_response()
                node = homologous[int(response)-1] if response.isdigit() else None
            if node:
                if not fields:
                    fields = self.parent_cli.placeholder.fields

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(node, target_node, field)
                        self.parent_cli.G.unbind(self.ls_node, target_node, field)
            else:
                print('Aborted process.')
        else:
            if fields:

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(self.ls_node, target_node, field)
                        self.parent_cli.G.unbind(self.ls_node, target_node, self.parent_cli.placeholder.fields[0])
            else:
                print('Not enough arguments provided.')
    
    def do_cp(self, arg):

        args = arg.split()
        fields = [arg for arg in args if arg in ['y0', 'y1', 'y2', 'e0', 'e1', 'e2']]
        idxs = [arg for arg in args if set(arg).issubset(set('0123456789-')) and arg not in fields]
        name = ' '.join([arg for arg in args if arg not in idxs and arg not in fields])
        
        numbers_set = set()
        for part in idxs:
            numbers_set.update(range(int(part.split('-')[0]), int(part.split('-')[-1]) + 1)) if '-' in part else numbers_set.add(int(part))
        idxs = sorted(numbers_set)

        target_nodes = [self.listed_nodes[i-1] for i in idxs] if idxs else self.listed_nodes

        if name:
            homologous = self.parent_cli.G.select(name=name)
            if len(homologous) == 1:
                node = homologous[0]
            else:
                SelectInterface([node._convert_header_to_compact_format() for node in homologous], 
                            self, f"Found {len(homologous)} homologous.",
                            "(Select the node to operate)", '>> ').cmdloop()
                response = self._get_response()
                node = homologous[int(response)-1] if response.isdigit() else None
            if node:
                if not fields:
                    fields = self.parent_cli.placeholder.fields

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(node, target_node, field)

            else:
                print('Aborted process.')
        else:
            if fields:

                for field in fields:
                    for target_node in target_nodes:
                        self.parent_cli.G.bind(self.ls_node, target_node, field)
            else:
                print('Not enough arguments provided.')
        
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
                contents = [f'{content} | {"█" * round(float(content) * 35)}' for content in contents]
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
        idxs = sk.parse_idxs_to_single_idxs(idxs)
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