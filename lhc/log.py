
def warning(*args):
    print("[WARNING] {0}".format(" ".join(map(str, args))));

def error(*args):
    print("[ERROR] {0}".format(" ".join(map(str, args))));
    exit(1);

def help():
    pass;

def version():
    pass;
