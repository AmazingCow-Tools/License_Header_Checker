##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : install.sh                                                    ##
##  Project   : License_Header_Checker                                        ##
##  Date      : May 23, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : Amazing Cow - 2017                                            ##
##  Description :                                                             ##
##---------------------------------------------------------------------------~##


################################################################################
## Vars                                                                       ##
################################################################################
SHARE_DIR="/usr/local/share";


echo "Installing...";

################################################################################
## lhc                                                                        ##
################################################################################
sudo python setup.py install --force;


################################################################################
## Templates                                                                  ##
################################################################################
## In cygwin we might not have all the directories
##   So create it if needed.
sudo mkdir -pv $SHARE_DIR;

## Just copy the files to destination folders.
sudo rm -rf $SHARE_DIR/lhc_templates;
sudo cp -r templates $SHARE_DIR/lhc_templates;


echo "Done...";
