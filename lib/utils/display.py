from tabulate import tabulate

def show_table(data, headers=None):
    print(tabulate(data, headers=headers, tablefmt="grid"))