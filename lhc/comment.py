##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : comment.py                                                    ##
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
## Python
import pdb;
## Amazing Cow
import constants;


################################################################################
## Comment Functions                                                          ##
################################################################################
def get_for_ext(ext):
    if(ext.startswith(".")):
        ext = ext[1:];

    return [
        get_start_for_ext(ext),
        get_end_for_ext  (ext)
    ];

def get_real_for_ext(ext):
    if(ext.startswith(".")):
        ext = ext[1:];

    return [
        get_real_str(get_start_for_ext(ext)),
        get_real_str(get_end_for_ext  (ext))
    ];


def get_start_for_ext(ext):
    ## Extension isn't in any list,
    ##    Check if it is a 'special' extension...
    if(ext in constants.kComment_Other.keys()):
        return constants.kComment_Other[ext][0];

    ## Check which list is the ext...
    if  (ext in constants.kComment_Slash): return "/";
    elif(ext in constants.kComment_Hash ): return "#";

    ## Can't find the ext...
    ##    Probally a script file without ext...
    return "#";

def get_end_for_ext(ext):
    ## Extension isn't in any list,
    ##    Check if it is a 'special' extension...
    if(ext in constants.kComment_Other.keys()):
        return constants.kComment_Other[ext][2];

    return get_start_for_ext(ext);


def get_real_str(cmt):
    return cmt if len(cmt) != 1 else cmt * 2;
