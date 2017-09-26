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

