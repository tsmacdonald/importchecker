import sys
from glob import glob

verbose, all, pretty, extra = False, False, True, True

def get_files():
    return glob("*.java")

def is_import(line):
    return "import" in line

def is_end_of_imports(line):
    return "public" in line and "class" in line

def check(file):
    with open(file) as f:
        classes = {}
        lines = f.readlines()
        for line in lines:
            if is_import(line):
                if verbose: print "\nParsing this import line:", line.strip()
                classes = read_import_line(line, classes)
            if is_end_of_imports(line):
                if verbose: print "\nNo more imports after this line:", line
                break
        for line in lines:
            if not is_import(line):
                for key in classes:
                    if key in line:
                        if verbose:
                            print "This line uses the %s class: %s"%(key, line)
                        classes[key] = True

        if pretty:
            filename_msg = "|     %s"%f.name
            print "+" + ("-" * 78) + "+"
            print "|" + (" " * 78) + "|"
            print filename_msg + (" " * (79 - len(filename_msg))) + "|"
            print "|" + (" " * 78) + "|"
            print "+" + ("-" * 78) + "+\n"
        else:
            print "\n%s"%f.name
        for key in classes:
            if not classes[key] and extra:
                print "\t- %s class is not used"%key
            elif all:
                print "\t+ %s class is used"%key
        print "\n"
        
                

def read_import_line(line, classes):
    parts = line.split(".")
    tail = last(parts)
    if "//" in tail: #Check for comments. This will break with /* */ comments,
                     #but those aren't usually on the same line as an import.
        tail = tail[:tail.rfind("//")]
    jclass = tail.strip().replace(";", "")
    if verbose: print "Found this class being imported:", jclass
    classes[jclass] = False
    return classes
            
def last(sequence):
    return sequence[len(sequence) - 1]

def print_help():
    print "\nChecks all java files in the current working directory to see if they have extraneous import statements.\n" + "\nOptions:\n" + "\t-a (--all):\n\t\tPrint results for all imports--not just the unnecessary ones.\n" + "\t-h (--help):\n\t\tPrint this help and exit (without parsing files).\n" + "\t-u (--ugly):\n\t\tPrint only the necessary information, with no pretty (and space-\n" + "\t\tconsuming) effects.\n" + "\t-v (--verbose):\n\t\tPrint extra information.\n" + "\nCopyright 2011 Tim Macdonald <tmacdonald@carleytech.com>."
 
def main():
    args = sys.argv
    global verbose, all, pretty
    if "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)
    if "-v" in args or "--verbose" in args:
        verbose = True
    if "-a" in args or "--all" in args:
        all = True
    if "-u" in args or "--ugly" in args:
        pretty = False
    files = get_files()[::-1] #The reverse ([::-1]) puts things in alphabetical order
    for file in files:
        check(file)

if __name__ == "__main__":
    main()
