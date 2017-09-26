##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : rcfile.py                                                     ##
##  Project   : License_Header_Checker                                        ##
##  Date      : Sep 25, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : Amazing Cow - 2017                                            ##
##  Description :                                                             ##
##---------------------------------------------------------------------------~##

import os;
import os.path;
## AmazingCow
import constants;
import gitrepo;
import log;


################################################################################
## Public Vars                                                                ##
################################################################################
info = dict.fromkeys(constants.kInfoKeys);


################################################################################
## Public Functions                                                           ##
################################################################################
def read_info():
    root_path = os.path.abspath(".");
    if(gitrepo.is_valid()):
        root_path = gitrepo.get_root();

    fullpath = os.path.join(root_path, constants.kFilename_LHCRC);

    if(not os.path.exists(fullpath)):
        log.warning(
            "Missing {0} file on project root.".format(constants.kFilename_LHCRC)
        );
        return;

    for line in open(fullpath).readlines():
        key, value = line.split(":");

        key   = key.strip  ();
        value = value.strip();

        info[key] = value;

