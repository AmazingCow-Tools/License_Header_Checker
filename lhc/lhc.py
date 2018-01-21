#!/usr/bin/python3
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : lhc.py                                                        ##
##  Project   : License_Header_Checker                                        ##
##  Date      : Sep 25, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : Amazing Cow - 2017                                            ##
##  Description :                                                             ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
## Python
import os;
import os.path;
## Amazinzg Cow - Libs
import constants;
import rcfile;
import srcfile;
import cmdline;


##----------------------------------------------------------------------------##
## Public Functions                                                           ##
##----------------------------------------------------------------------------##
def main():
    ##--------------------------------------------------------------------------
    ## Parse the command line.
    cmdline.parse_info();
    print(cmdline.info);

    ##--------------------------------------------------------------------------
    ## Read the lhcrc of the target file.
    old_cwd  = os.getcwd();
    dir_name = os.path.dirname(cmdline.filename);
    os.chdir(dir_name);

    rcfile.read_info();

    os.chdir(old_cwd);

    ##--------------------------------------------------------------------------
    ## Process the Source file.
    srcfile.read_info(cmdline.filename);

    srcfile.merge_rc_info          (rcfile.info);
    srcfile.merge_command_line_info(cmdline.info);

    if(cmdline.no_banner == False):
        srcfile.set_banner();

    lines = srcfile.build();

    ##--------------------------------------------------------------------------
    ## Write the changes.
    if(not cmdline.dry_run):
        open(cmdline.filename, "w").writelines(lines);
    else:
        print("".join(lines));


if __name__ == "__main__":
    main()
