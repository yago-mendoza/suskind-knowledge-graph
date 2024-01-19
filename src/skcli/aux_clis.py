import cmd 
import random
import argparse

from src.skcli.aux_funcs.visuals import *


class LS_Interface(cmd.Cmd):

    prompt = '>> '
    def __init__(self, nodes, parent_cli, ls_args):
        super().__init__()
        self.nodes = nodes
        self.parent_cli = parent_cli
        self.ls_args = ls_args
        self.cmdloop()

    # DO_DEL and DO_ADD arent working

    def do_del(self, indexs):
        indexs = [int(_) for _ in indexs.split()]
        for index in indexs:
            target_node = self.nodes[index-1]
            field_symb = self.parent_cli.placeholder.fields[0]
            field = ('synset' if field_symb[0] == 'y' else 'semset') + field_symb[1]

            # ?????????????????????????????????????????????????????
            print(target_node in
                  self.parent_cli.G.find(name=self.parent_cli.placeholder.node.name)[0].get_neighbors().set())
            # True
            self.parent_cli.G.unbind(self.parent_cli.placeholder.node,
                                     field, target_node)
            # list.remove(x) : x not in list
            
        padded_print(f"Deleted {len(indexs)} nodes.")

    def do_add(self, name):

        while True:
            if not name:  # Exit add loop if the name is empty
                break

            matched_nodes = self.parent_cli.G.find(name=name)
            selected_node = None

            if len(matched_nodes)>1:
                selection_interface = SelectNodeInterface(matched_nodes, self, "Did you mean...", "(Press Enter to select none)")
                selection_interface.cmdloop()
                selected_index = self.selection_interface_output

                if selected_index and selected_index.isdigit():
                    selected_node = matched_nodes[int(selected_index) - 1]
            
            if len(matched_nodes)==1:
                selected_node = matched_nodes[0]

            if not selected_node and input(" "*3+"| Do you want to create this node? [Y/N] : ").strip().lower() in ['Y','y']:
                creation_input = input(" "*3+"| Enter <lang> <type> <lemma> in this format:\n"+" "*3+'> ')
                lang, type_, lemma = creation_input.split()
                self.parent_cli.G.create_node(lang, type_, name, lemma)
                print(" "*3+"| Node created and binded.")
            elif selected_node:
                current_node = self.parent_cli.placeholder.node
                edge_type = self.parent_cli.placeholder.fields[0]
                self.parent_cli.G.bind(current_node, edge_type, selected_node)

            name = input("   add ")

    def default(self, line):

        if '>' in line:
            indices, target_field = line.split('>')
            try:
                indices = [int(i) for i in indices.split()]
                target_nodes = [self.nodes[i-1] for i in indices]

                # Current field is determined by the CLI's placeholder settings
                current_field = self.parent_cli.placeholder.fields

                # Validate and format the target field
                if target_field.strip().startswith('y'):
                    target_edge_type = 'synset' + target_field.strip()[1]
                elif target_field.strip().startswith('e'):
                    target_edge_type = 'semset' + target_field.strip()[1]
                else:
                    raise ValueError("Invalid target field specification")

                # Move nodes from the current field to the target field
                for node in target_nodes:
                    # Unbind from the current edge type
                    self.parent_cli.G.unbind(node, current_field, node)
                    # Bind to the new edge type
                    self.parent_cli.G.bind(node, target_edge_type, node)

                print(f"Moved {len(target_nodes)} nodes from '{current_field}' to '{target_edge_type}'.")
            except Exception as e:
                print(f"Error processing command: {e}")

        else:
            padded_print(f'Unrecognized argument(s): {" ".join(line[:10])}')


        # 15 96 22 > y0"   =   line
        # takes this nodes and moves them to the field y0, for the use case

    
    def cmdloop(self, intro=None):
        super().cmdloop(intro)

    def do_help(self, arg=None):
        print("'add <name>' to add")
        print("'del' <int> <int> ...' to unbind")
        print("'cd <int>' to enter")
        print("'ls' to refresh")
        print("'<int> <int> ... > y0' for example to transform")
        pass
    
    def default(self, line):
        pass

    def emptyline(self): #finished
        # To exit with an empty Enter key press
        padded_print("Exited.")
        return True
    
    def do_exit(self, arg):
        padded_print("Exited.")
        return True 

    def do_cd(self, index): # finisehd
        self.parent_cli._set_node(self.nodes[int(index)-1])
        return True

    def do_ls(self, arg=None):
        names = [node.name for node in self.parent_cli.G.get_neighbors().set()]
        # get_neighbors ya está establecido en fields
        padded_print(f"Refreshing...")
        strings_to_display = [f'| {i + 1}. {name}' for i, name in enumerate(names)]
        columnize(strings_to_display, ncol=self.ls_args.ncol, col_width=self.ls_args.width)


class CreateNodeInterface(cmd.Cmd):

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
        padded_print(f"(LANG/TYPE) assigned by default : ({self.default_lang}/{self.default_type})")
        padded_print(f"Type <lang>/<type> to switch default pipe.")

    def do_help(self):
        print()
    
    def default(self, line):

        self.selection_interface_output = None
        if len(line)==2 and line.isalpha() and line.islower():
            self.default_lang = line
        elif len(line)==1 and line.isalpha() and line.islower():
            self.default_type = line
        elif line.strip() == '?':
            pass
            # padded_print(f"| LANG assigned by default : '{self.default_lang}'")
            # padded_print(f"| TYPE assigned by default : '{self.default_type}'")
        else:
            name = line[0].upper() + line[1:]
            homologous = self.parent_cli.G.find(name=name,
                                   lang=self.default_lang,
                                   type=self.default_type)
            if len(homologous) > 0:
                statement_1 = f"Found {len(homologous)} homologous."
                statement_2 = "(Press Enter to move on.)"
                interface_popup = SelectNodeInterface(homologous, self, statement_1, statement_2, 'Lemma: ')
                interface_popup.cmdloop()
                if isinstance(self.selection_interface_output, str):
                    if self.selection_interface_output not in [node.lemma for node in homologous]:
                        self.parent_cli.G.create_node(lang=self.default_lang,type_=self.default_type,name=name,lemma=self.selection_interface_output)
                        print(f"OK : [{self.default_lang}][{self.default_type}][{name}]@[({self.selection_interface_output})]")
                    else:
                        padded_print("Already existing. Did nothing.")
            else:
                self.parent_cli.G.create_node(lang=self.default_lang,type_=self.default_type,name=name,lemma="NA")
                print(f"OK : [{self.default_lang}][{self.default_type}][{name}]@[({self.selection_interface_output})]")
        
        self.update_prompt()

    def emptyline(self):
        # To exit with an empty Enter key press
        padded_print("Exited.")
        return True
    
    
class SelectNodeInterface(cmd.Cmd):

    def __init__(self, nodes, parent_cli, statement_1="", statement_2="", prompt='>> '):
        # Requires :
        # - set of options (<Node>s)
        # - statement to be displayed, indicating what can be entered.
        # - reference to the parent_cli to which the resulting option will be sent.
        #   (if [int] is entered -> return the <Node> (at 'n'th position)
        #   (if [str] is entered -> return the <String>)
        #   Note. It returns it by delivering it at .selection_interface_output attr from the parent_cli.
        super().__init__()
        self.nodes = nodes
        self.statement_1 = statement_1
        self.statement_2 = statement_2
        self.parent_cli = parent_cli
        self.prompt = prompt
        self.display()
    
    def display(self):
        padded_print(self.statement_1)
        for index, node in enumerate(self.nodes, start=1):
            lang, type, name, lemma = node.identify()
            string_index = str(index).zfill(2 if len(self.nodes)>10 else 1)
            print(f"|   {string_index}) [{lang}][{type}][{name}]@[({lemma or ''})]")
        padded_print(self.statement_2)

    def deliver_result(self, selection_interface_output):
        self.parent_cli.selection_interface_output = None
        self.parent_cli.selection_interface_output = selection_interface_output

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
                if 0 <= index < len(self.nodes):
                    self.deliver_result(line)
                else:
                    print("Please enter a valid number from the list.")
        except ValueError:
            print("Please enter a number to select a node or just press Enter to exit.")
        return True # exits loops
    
    def emptyline(self):
        # To exit with an empty Enter key press
        return True
    
    def do_exit(self, arg):
        return True 