##COWTODO(n2omatt): pip install gitpython


################################################################################
## Constants                                                                  ##
################################################################################
kComment_Slash = [
    ## C / C++
    "cpp", "c", "h", "hpp",
    ## ObjC
    "m", "mm",
    ## C#
    "cs",
    # Javascript
    "js", "jsx",
    ## Action Script
    "as3",
    ## PHP
    "php",
];

kComment_Hash = [
    ## Shell
    "sh",
    ## SQL
    "sql",
    ## Python
    "py",
];

kComment_Other = {
    "html" : ["<!-- ", "-", " -->"]
};


kInfoKeys = [
    "file",
    "project",
    "date",
    "license",
    "author",
    "copyright",
    "description",
    "company",
];

kFilename_LHCRC  = "lhcrc";
kLicense_Default = "GPLv3";


kMark_Start = "~-";
kMark_End   = "-~";


kPath_Template = "/usr/local/share/lhc_templates";
