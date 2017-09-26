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

################################################################################
## Imports                                                                    ##
################################################################################
## Amazinzg Cow - Libs
import constants;
import rcfile;
import srcfile;
import cmdline;


################################################################################
## Public Functions                                                           ##
################################################################################
def main():
    rcfile.read_info  ();
    cmdline.parse_info();

    srcfile.read_info(cmdline.filename);

    srcfile.merge_rc_info          (rcfile.info);
    srcfile.merge_command_line_info(cmdline.info);

    srcfile.set_banner();

    lines = srcfile.build();

    open(cmdline.filename, "w").writelines(lines);

if __name__ == "__main__":
    main()


