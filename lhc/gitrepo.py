##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : gitrepo.py                                                    ##
##  Project   : License_Header_Checker                                        ##
##  Date      : Sep 25, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : Amazing Cow - 2017                                            ##
##  Description :                                                             ##
##---------------------------------------------------------------------------~##

################################################################################
## Imports                                                                    ##
################################################################################
import git;
import os;
import time;
import pdb;

################################################################################
## Public Functions                                                           ##
################################################################################
def is_valid():
    return get_root() is not None;

def get_root():
    try:
        return git.Repo(search_parent_directories=True).working_tree_dir;
    except:
        return None;

def get_url():
    if(is_valid() is None):
        return None;

    return git.Repo(search_parent_directories=True).remotes.origin.url;

def get_date_for_file(filename):
    ## COWTODO(n2omatt): Doing that way because it's very fast
    ## to develop, and I need this shit done quickly...
    ## Refactor it to a more concise and "correct" way!!!
    tmp_file = ".__get_git_date_for_file__";
    os.system(
        "git log --format=%aD {0} | tail -1 > {1}".format(filename, tmp_file)
    );

    lines = open(tmp_file).readlines();

    os.system("rm -rf {0}".format(tmp_file));

    if(len(lines) != 0):
        line = lines[0].replace("\n", "")[:-6];
        tm   = time.strptime(
            line,
            "%a, %d %b %Y %H:%M:%S"
        );
        return time.strftime("%b %d, %Y", tm);

    return None;
