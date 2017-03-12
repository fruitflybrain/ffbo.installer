import os,sys,subprocess
import argparse
import simplejson as json

# load default configuration
config = json.load(open("packages.json"));

def query_yes_no(msg=None):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])

    if msg is not None:
        sys.stderr.write(msg)
    sys.stderr.write("[yes/no]: ")
    choice = raw_input().lower()
    if choice in yes:
       return True
    elif choice in no:
       return False
    else:
       query_yes_no("Please respond with 'yes' or 'no'... ")

def traverse_deps(pkgList):
    idx = 0;
    while idx < len(pkgList):
        deps = config[pkgList[idx]]['deps']
        for y in deps:
            if y not in pkgList:
                pkgList.append(y)
        idx += 1

parser = argparse.ArgumentParser('download.py',description="Script for downloading FFBO applications")

parser.add_argument("--path", default="./", type=str, required=True, help="directory to store all downloaded FFBO repository")

add_nlp = parser.add_argument_group('nlp', 'arguments for downloading NeuroNLP')
add_nlp.add_argument('--no-neuronlp', dest='nlp', action='store_false', help='exclude NeuroNLP')
parser.set_defaults(nlp=True)

add_gfx = parser.add_argument_group('nlp', 'arguments for downloading NeuroGFX')
add_gfx.add_argument('--no-neurogfx', dest='gfx', action='store_false', help='exclude NeuroGFX')
parser.set_defaults(gfx=True)

args = parser.parse_args()

# check the directory for downlo
path = os.path.realpath(args.path)
if not os.path.exists(path):
    if query_yes_no('directory \033[31m%s \033[0mdoes not exist... Do you want to create it? ' % path):
        os.mkdir(path)
    else:
        exit(1)
else:
    if not os.access(path, os.W_OK):
        sys.stderr.write('directory %s exists, but is not writable' % path)
        exit(1)

# Get the list of all required repositories
packageList = []
if args.nlp:
    packageList.append('neuronlp')
if args.gfx:
    packageList.append('neurogfx')

traverse_deps(packageList)
packageFolder = {x:os.path.join(path,config[x]['url'].split('/')[-1]) for x in packageList}

sys.stdout.write("The script is downloading following repositories:\n")
for k,v in packageFolder.items():
    sys.stderr.write('\tDownload \033[34m%s \033[0mto \033[32m%s\033[0m\n' % (k,v))
if not query_yes_no('Do you want to proceed? '):
    exit(1)

# Download all required repository
for k,v in packageFolder.items():
    sys.stderr.write('Downloading \033[34m%s..\033[\0m\n' % k)
    subprocess.call(["git", "clone", config[k]['url'], v])
