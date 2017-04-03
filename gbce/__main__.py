from .gbce import GBCE


if __name__ == '__main__':
    shell = GBCE()
    shell.prompt = '> '
    shell.intro = 'Welcome to the << Global Beverage Corporation Exchange >>'
    shell.cmdloop()
