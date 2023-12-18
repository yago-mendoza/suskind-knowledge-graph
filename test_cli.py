import cmd

class GraphCmd(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "14:32:04 ~ [es][n][concept]@[(lemma)]/: "
        self.filters = []

    def do_filter(self, args):
        """Gestiona el comando 'filter' y sus subcomandos."""
        if args == "-e":
            self.prompt = "14:32:09 ~ [es][n][concept]@[(lemma)]/: filter\n"
        elif args == "-rm":
            self.prompt = "14:32:18 ~ [en][v][Resonate]@[('')]/: filter\n"
        else:
            self.prompt = "14:32:18 ~ [en][v][Resonate]@[('')]/: filter\n"

    def do_r(self, args):
        """Gestiona el comando 'r' y sus subcomandos."""
        if args == "-favorite":
            self.prompt = "14:32:11 ~ [es][n][concept]@[(lemma)]/: r -favorite\n"
        elif args == "-f2":
            self.prompt = "14:32:11 ~ [en][n][Dinero]@[('')]/: r -f2\n"
        else:
            self.prompt = "14:32:18 ~ [en][v][Resonate]@[('')]/: r\n"

    def do_ls(self, args):
        """Gestiona el comando 'ls' y sus subcomandos."""
        if args == "-f1":
            self.prompt = "14:32:15 ~ [en][v][Resonate]@[('')]/: ls -f1\n"
        else:
            self.prompt = "14:32:18 ~ [en][v][Resonate]@[('')]/: ls\n"

    def do_cd(self, args):
        """Gestiona el comando 'cd' y sus subcomandos."""
        self.prompt = "14:32:18 ~ [es][n][Alabastro]@[('')]/: cd " + args + "\n"

    def do_summary(self, args):
        """Gestiona el comando 'summary'."""
        self.prompt = "14:32:18 ~ [en][j][Normal]@[('')]/: summary\n"

    def do_set(self, args):
        """Gestiona el comando 'set'."""
        self.prompt = "14:32:18 ~ [en][j][Normal]@[('')]/: set " + args + "\n"

    def do_unset(self, args):
        """Gestiona el comando 'unset'."""
        self.prompt = "14:32:18 ~ [en][j][Normal]@[('')]/: unset " + args + "\n"

    def do_exit(self, args):
        """Sale del programa."""
        print("Exiting...")
        return True

if __name__ == '__main__':
    GraphCmd().cmdloop()