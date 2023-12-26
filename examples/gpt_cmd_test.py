import cmd
import argparse

class MyShell(cmd.Cmd):
    intro = 'Bienvenido a mi CLI. Escribe help o ? para listar los comandos.\n'
    prompt = '(miCLI) '

    # Comando simple sin argumentos.
    def do_saludar(self, arg):
        print("¡Hola Mundo!")

    def do_set(self, arg):
        # ademas habilita set --help (triggered automaitcally if just 'set')
        parser = argparse.ArgumentParser(prog='set', description='Establece una variable a un valor.')
        parser.add_argument('variable', help='La variable a establecer.')
        parser.add_argument('valor', help='El valor a establecer.')
        parser.add_argument('-f', '--full-price', action='store_true', help='Establecer el precio completo')
        parser.add_argument('--force', action='store_true', help='Forzar la operación')

        try:
            args = parser.parse_args(arg.split())
            print(f"Estableciendo {args.variable} a {args.valor}")
            if args.full_price:
                print("Estableciendo al precio completo.")
            if args.force:
                print("Operación forzada.")
        except SystemExit:
            # Evitar que cierre el shell cuando el comando falla
            pass

if __name__ == '__main__':
    MyShell().cmdloop()