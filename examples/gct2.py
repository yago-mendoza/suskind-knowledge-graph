import cmd

class FilterManager:
    def __init__(self):
        # Initialize with some filters
        self.filters = {
            'f1': "type('w').lang('es')",
            'f2': "starts('clar')"
        }

    def add_filter(self, filter_name, filter_def):
        self.filters[filter_name] = filter_def

    def remove_filter(self, filter_name):
        if filter_name in self.filters:
            del self.filters[filter_name]

    def list_filters(self):
        return self.filters

class CLIEditor(cmd.Cmd):
    prompt = '>> '

    def __init__(self, filter_manager):
        super().__init__()
        self.filter_manager = filter_manager

    def do_add(self, line):
        args = line.split()
        if len(args) == 2:
            self.filter_manager.add_filter(args[0], args[1])
            print(f"Added filter: {args[0]}")
        else:
            print("Usage: add [filter_name] [filter_definition]")

    def do_rm(self, line):
        self.filter_manager.remove_filter(line)
        print(f"Removed filter: {line}")

    def do_list(self, line):
        filters = self.filter_manager.list_filters()
        for name, definition in filters.items():
            print(f"{name}/{definition}")

    def do_exit(self, line):
        return True

    def emptyline(self):
        # Exit the editor when an empty line is entered
        return True

class MainCLI(cmd.Cmd):
    prompt = '> '

    def __init__(self):
        super().__init__()
        self.filter_manager = FilterManager()

    def do_filter(self, line):
        args = line.split()
        if "-e" in args:
            editor = CLIEditor(self.filter_manager)
            editor.cmdloop("Entered editor mode on filters:")
        else:
            self.show_filters()

    def show_filters(self):
        print("| Filters:")
        for name, definition in self.filter_manager.list_filters().items():
            print(f"| {name}/{definition}")

    def do_exit(self, line):
        """Exit the application."""
        return True

    def emptyline(self):
        # Do nothing on empty input line
        pass

if __name__ == '__main__':
    MainCLI().cmdloop()