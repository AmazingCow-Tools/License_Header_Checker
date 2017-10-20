##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : cmdline.py                                                    ##
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
import getopt;
import sys;
## Amazing Cow - Libs
import constants;
import log;


################################################################################
## Public Vars                                                                ##
################################################################################
info     = dict.fromkeys(constants.kInfoKeys);

no_rc     = False;
verbose   = False;
dry_run   = False;
filename  = None;
no_banner = False;


################################################################################
## Public Functions                                                           ##
################################################################################
def parse_info():
    global info;
    global no_rc;
    global verbose;
    global dry_run;
    global filename;
    global no_banner;

    try:
        cmd_options = getopt.gnu_getopt(
            sys.argv[1:],
            "",
            [
                ## Help / Version
                "help", "version",

                ## Run Control
                "no-rc", "verbose", "dry-run", "no-banner",

                ## Info Flags
                "project=",
                "author=",
                "date=",
                "license=",
                "copyright=",
                "company="
            ]
        );

        ## Parse the flag values.
        for flag, value in cmd_options[0]:
            ## Help / Version
            if  ("help"    in flag): log.help   ();
            elif("version" in flag): log.version();

            ## Run Control
            elif("no-rc"     in flag): no_rc     = True; continue;
            elif("verbose"   in flag): verbose   = True; continue;
            elif("dry-run"   in flag): dry_run   = True; continue;
            elif("no-banner" in flag): no_banner = True; continue;

            ## Info Flags
            flag = flag.replace("=", "").replace("--", "");
            info[flag] = value;

        ## Parse the non flag values.
        if(len(cmd_options[1]) == 0):
            log.error("Missing filename.");

        filename = cmd_options[1][0];

    except:
        raise
