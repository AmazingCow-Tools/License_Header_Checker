#!/usr/bin/python3
import pdb;
import sys;
import os;
import os.path;
import getopt;
import git;


################################################################################
## Constants                                                                  ##
################################################################################
kCmt_Slash = [
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

kCmt_Hash = [
    ## Shell
    "sh",
    ## SQL
    "sql",
    ## Python
    "py",
];

kCmt_Other = {
    "html" : ["<!-- ", "-", " -->"]
};


kInfoKeys = [
    "file",
    "author",
    "project",
    "author",
    "date",
    "license",
    "copyright",
    "description",
];


################################################################################
## Run Info                                                                   ##
################################################################################
class RunInfo:
    no_rc   = False;
    verbose = False;
    dry_run = False;

    company  = None;
    filename = None;

    rc_info_dict = dict.fromkeys(kInfoKeys);
    info_dict    = dict.fromkeys(kInfoKeys);



################################################################################
## Show Functions                                                             ##
################################################################################
def show_help():
    print("h");

def show_version():
    print("v");

def show_error(*args):
    print("[FATAL] {0}".format(" ".join(map(str, args))));
    exit(1);

def show_warning(*args):
    print("[WARNING] {0}".format(" ".join(map(str, args))));


################################################################################
## git Functions                                                              ##
################################################################################
def is_git_repo():
    return get_git_repo_root() is not None;

def get_git_repo_root():
    try:
        return git.Repo(search_parent_directories=True).working_tree_dir;
    except:
        return None;

def get_git_repo_url():
    if(is_git_repo is None):
        return none;

    return git.Repo(search_parent_directories=True).remotes.origin.url;


################################################################################
## Comment Functions                                                          ##
################################################################################
def get_start_comment_for_ext(ext):
    ## Extension isn't in any list,
    ##    Check if it is a 'special' extension...
    if(ext in kCmt_Other.keys()):
        return kCmt_Other[ext][0];

    ## Check which list is the ext...
    if  (ext in kCmt_Slash): return "/";
    elif(ext in kCmt_Hash ): return "#";

    ## Can't find the ext...
    ##    Probally a script file without ext...
    return "#";

def get_end_comment_for_ext(ext):
    ## Extension isn't in any list,
    ##    Check if it is a 'special' extension...
    if(ext in kCmt_Other.keys()):
        return kCmt_Other[ext][2];

    return get_start_comment_for_ext(ext);

def get_real_comment_str(cmt):
    return cmt if len(cmt) != 1 else cmt * 2;


################################################################################
## Read Template Functions                                                    ##
################################################################################
def read_template_header(name):
    filename    = "{0}.template".format(name);
    lines       = open(filename).readlines();
    clean_lines = [];
    max_len     = 0;

    for l in lines:
        clean_line = l.replace("\n","");
        max_len    = max(len(clean_line), max_len);

        clean_lines.append(clean_line);

    for i in range(len(clean_lines)):
        curr_line = clean_lines[i];
        curr_len  = len(curr_line);

        clean_lines[i] = curr_line + ((max_len - curr_len) * " ");

    return clean_lines;

## COWTODO(n2omatt): We need this now that we have the kInfoKeys???
def read_template_info():
    lines       = open("info.template").readlines();
    clean_lines = [];
    spaces      = " " * 2;
    for l in lines:
        clean_line = l.replace("\n","");
        clean_lines.append(spaces + clean_line);

    return clean_lines;


################################################################################
## Setup Functions                                                            ##
################################################################################
## Given a list of info lines and a dictionary with the actual info
## builds the resulting lines to be put on output file.
def setup_info(info_lines, info_dict):
    filled_lines = []; ##Output lines...

    for line in info_lines:
        end_index = line.find(":");
        if(end_index == -1):
            raise Exception("Missing ':' in line: ({0})".format(line));

        ## Get the tag value.
        tag = line[0 : end_index].strip().lower();
        if(tag not in kInfoKeys):
            raise Exception(
                "Not recognized tag: ({0}) in line: ({1})".format(tag, line)
            );

        ## Some tags has special handling...
        ##   copyright: needs to be splited in atomic years...
        value = info_dict[tag];
        if(tag == "copyright"):
            value = build_copyright_years(info_dict["copyright"]);
        ##   decription: needs to be written until the end of lines
        ##               since it may span multiple lines.
        elif(tag == "description" and info_dict["description"] is not None):
            filled_lines.append(""); ## An empty line to give separate description:
            filled_lines.append(line);

            for desc_line in info_dict["description"]:
                desc_spaces      = " " * 5; ## Indent the lines.
                filled_line = desc_spaces + desc_line;
                filled_lines.append(filled_line);

            ## Since we already cleaned the lines up
            ## we don't need further processing...
            continue;

        ## Build the line...
        spaces      = " ";
        filled_line = line + spaces + str(value);
        filled_lines.append(filled_line);

    return filled_lines;

## Builds the cleaned up version of the copyright years line.
##    Years with the diference more than one is set to
##    be ouput on a range "syntax".
def build_copyright_years(years_list):
    if(years_list is None or len(years_list) == 0):
        years_list = [2017];  ##COWTODO(n2omatt): get the date...

    years_list = set(years_list);

    yr_min = min(years_list);
    yr_max = max(years_list);

    if(len(years_list) == 1):
        return yr_max;

    if(len(years_list) == 2 and (yr_max - yr_min == 1)):
        return "{0}, {1}".format(yr_min, yr_max);

    return "{0} - {1}".format(yr_min, yr_max);


################################################################################
## Fill Functions                                                             ##
################################################################################
## Fill a line to be output as comment.
##    start         : Start comment str.
##    end           : End comment str.
##    content       : What will be placed between the comments.
##    center        : Should center the content beteween the comments?
##    start_spacing : How much gap should lead the content?
##    fill_char     : char that will be placed in gaps?
def fill(start, end, content, center, start_spacing, fill_char = " "):
    ## Get the actual comments strings.
    real_start = get_real_comment_str(start);
    real_end   = get_real_comment_str(end  );

    ## Put spaces only if needed.
    ##   Only if the start comment doesn't ends with a space itself.
    start_spc      = "" if real_start[-1] == " " or start_spacing == False else " ";
    hard_spc_count = len(real_start) + len(real_end) + len(start_spc);

    filled_content = content;
    ## If center calculate the amount of fill to put and
    ## builds the filled content.
    if(center):
        content_len    = len(content);
        content_fill   = fill_char * int((((80 - hard_spc_count) - content_len) / 2));
        filled_content = "{0}{1}{0}".format(content_fill, content);

    ## Put the content between the comments.
    line  = real_start + start_spc + filled_content;
    line += fill_char * (80 - len(real_end) - len(line)) + real_end;

    return line;

## Special case of fill
##    This is for the start and end of the license header
##    since they need to put special "markers" to indenfiy
##    the code as a license header.
def fill_header_footer(start_cmt, end_cmt, is_header):
    filled = fill(
        start_cmt,
        end_cmt,
        "",
        center=False,
        start_spacing=False,
        fill_char="-"
    );
    index  = filled.find("-") if is_header else filled.rfind("-");
    filled = filled[:index] +  "~" + filled[index+1:]

    return filled + "\n";


################################################################################
## Source File Parser Functions                                               ##
################################################################################
## Remove the comments (both start and end) and any info tag.
##  COWTODO(n2omatt): What's info line???
def clean_src_line(src_line, real_start_cmt, real_end_cmt, info_line):
    return src_line                  \
        .replace(info_line,      "") \
        .replace(real_start_cmt, "") \
        .replace(real_end_cmt,   "") \
        .replace("\n",           "") \
        .strip();

## Since description can span multiple lines, we need a way to retrieve them.
## This function will parse the lines and get the ones that represents
## a description.
## COWTODO(n2omatt): And if the description is on same line??
def find_description_from_src_lines(src_lines, start_cmt, end_cmt):
    ## Get the actual comments strings.
    real_start_cmt = get_real_comment_str(start_cmt);
    real_end_cmt   = get_real_comment_str(end_cmt  );

    desc_lines = [];
    for l in src_lines:
        clean_line = clean_src_line(l, real_start_cmt, real_end_cmt, "");
        desc_lines.append(clean_line);

    return desc_lines;

## Given a source line and a list of possible infos "prefixes" that
## might prefix that line, this function will retrive the value
## contained in that line.
def find_value_from_src_lines(info_line, src_lines, start_cmt, end_cmt):
    ## Get the actual comments strings.
    real_start_cmt = get_real_comment_str(start_cmt);
    real_end_cmt   = get_real_comment_str(end_cmt  );

    ## For each source line...
    ##   1 - Check if the given source line has the tag we want...
    ##   2 - Get the Key that line has and clean it.
    ##   3 - Get the Value that line has and clen it.
    ##   4 - Return the pair of key, value.
    for i in range(len(src_lines)):
        src_line = src_lines[i];

        ## Remove the ':' to not worry about difference spacing issues.
        key = info_line.replace(":", "").strip();
        if(key not in src_line):
            continue;

        ## Clean key.
        key = key.lower();

        ## Description is special, since it may span multiple lines
        ##   So if we find it, we read until the end lines
        ##   to get all the content.
        if(key == "description"):
            value = find_description_from_src_lines(
                src_lines[i+1:],
                start_cmt,
                end_cmt
            );
            ## Since we already cleaned the value up, and the
            ## description is treated differently we don't need
            ## further processing...
            return [key, value];

        ## Clean value.
        value = clean_src_line(
            src_line,
            real_start_cmt,
            real_end_cmt,
            info_line
        );

        return [key, value];

    return None;

## Given the source lines of a file this function returns
## the indexes of lines that delimiter a header license.
def get_header_comment_lines_indexes(src_lines, start_cmt, end_cmt):
    ## Get the real string comments.
    ##   This is because the single char comments
    ##   will be doubled at start...
    real_start_cmt = get_real_comment_str(start_cmt);
    real_end_cmt   = get_real_comment_str(end_cmt  );

    ##
    start_line = -1;
    end_line   = -1;

    ## Find the boundaries for the header comment.
    ##  The will be encapsuled into ~- and -~ chars.
    for i in range(len(src_lines)):
        line = src_lines[i];

        if  (real_start_cmt + "~-" in line): start_line = i;
        elif("-~" + real_end_cmt   in line): end_line   = i;

    return [start_line, end_line];

## Extract a dictionary with the info contained into the
## license header lines.
def parse_src_lines(src_file_lines, start_cmt, end_cmt):
    header_lines = src_file_lines;

    ## Build the dictionary of the found info.
    ##   We need parse each line, check if we found a tag
    ##   if so, we add it's value to the dict.
    info_dict  = {};
    info_lines = read_template_info();

    for info_line in info_lines:
        ## Find Value.
        key_value = find_value_from_src_lines(
            info_line,
            header_lines,
            start_cmt,
            end_cmt
        );
        if(key_value is None):
            continue;

        ## Add.
        info_dict[key_value[0]] = key_value[1];

    return info_dict;


################################################################################
## Script                                                                     ##
################################################################################
def parse_command_line_options():
    try:
        cmd_options = getopt.gnu_getopt(
            sys.argv[1:],
            "",
            [
                ## Help / Version
                "help", "version",

                ## Run Control
                "no-rc", "verbose", "dry-run",

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
            if  ("help"    in flag): show_help   ();
            elif("version" in flag): show_version();

            ## Run Control
            elif("no-rc"   in flag): RunInfo.no_rc    = True;
            elif("verbose" in flag): RunInfo.verbose  = True;
            elif("dry-run" in flag): RunInfo.dry_run  = True;

            ## Company...
            elif("company" in flag): RunInfo.company = value;

            ## Info Flags
            flag = flag.replace("=", "");
            RunInfo.info_dict[flag] = value;

        ## Parse the non flag values.
        if(len(cmd_options[1]) == 0):
            show_error("Missing filename.");
        else:
            RunInfo.filename = cmd_options[1][0];

    except:
        raise


## Read the lhcrc file.
## COWTODO(n2omatt): Comment.
def read_rc():
    root_path = os.path.abspath(".");
    if(is_git_repo()):
        root_path = get_git_repo_root();

    fullpath = os.path.join(root_path, "lhcrc"); ##COWTODO(n2omatt); Remove magic name...

    if(not os.path.exists(fullpath)):
        RunInfo.rc_info_dict = None;
        show_warning("Missing lhc.rc file on project root."); ##COWTODO(n2omatt); Remove magic name...
        return;

    for line in open(fullpath).readlines():
        key, value = line.split(":");

        key   = key.strip  ();
        value = value.strip();

        RunInfo.rc_info_dict[key] = value;


##COWTODO(n2omatt): pip install gitpython


def setup_run_info(info_dict):
    RunInfo.rc_info_dict["file"   ] = RunInfo.filename;
    RunInfo.rc_info_dict["company"] = RunInfo.company;

    for key in RunInfo.info_dict:
        ## Used passed the value by flag
        ##   It should override all other settings.
        value = RunInfo.info_dict[key];
        if(value is not None):
            continue;

        ## Check we got this information from the lhcrc file.
        ##   If so update the RunInfo.info_dict since it's
        ##   what will be used to manipulate the info.
        rcvalue = RunInfo.rc_info_dict[key];
        if(rcvalue is not None):
            RunInfo.info_dict[key] = rcvalue;
            continue;

        ## If we failed to get the info either from the
        ## command line and the lhcrc file, let's check
        ## if the actual source file provides this info for us.
        if(key in info_dict):
            src_value = info_dict[key];
            if(src_value is not None):
                RunInfo.info_dict[key] = src_value;


    ## Try to gatter info it's missing...
    ## COWTODO(n2omatt): Get from git it's available.
    ##   Get the today date...
    if(RunInfo.info_dict["date"] is None):
        RunInfo.info_dict["date"] = "DATE TO ADD.";

    ## Check if we can get the name of the project
    ## by the git url.
    if(is_git_repo()):
        repo_url  = get_git_repo_url();
        if(repo_url is not None):
            repo_name = os.path.basename(repo_url);
            repo_name = repo_name.replace(".git","");
            RunInfo.info_dict["project"] = repo_name;


def main():
    parse_command_line_options();
    read_rc();

    ## Read the source file.
    src_lines = open(RunInfo.filename).readlines();

    ## Get the comments of this type of file.
    extension = os.path.splitext(RunInfo.filename);
    start_cmt = get_start_comment_for_ext(extension);
    end_cmt   = get_end_comment_for_ext  (extension);

    ## Get the indexes that represents the license header.
    start_line, end_line = get_header_comment_lines_indexes(
        src_lines,
        start_cmt,
        end_cmt
    );

    ## Check for any information contained on the license header.
    info_dict = parse_src_lines(
        src_lines[start_line:end_line],
        start_cmt,
        end_cmt
    );

    ## Merge all the info passed by the command line, by the
    ## lhcrc file and contained in the actual source file.
    setup_run_info(info_dict);

    ## Build the lines that will be put on the source
    ## file with the update information...
    info_lines = setup_info(
        read_template_info(),
        RunInfo.info_dict
    );

    ## Start of License header...
    header = fill_header_footer(start_cmt, end_cmt, is_header=True);

    ## Company banner....
    for line in read_template_header("amazingcow"):
        header += fill(
            start_cmt,
            end_cmt,
            line,
            center=True,
            start_spacing=False,
            fill_char = " "
        );
        header += "\n";

    ## Info lines...
    for line in info_lines:
        header += fill(
            start_cmt,
            end_cmt,
            line,
            center=False,
            start_spacing=False,
            fill_char = " "
        );
        header += "\n";

    ## End of License header...
    header += fill_header_footer(start_cmt, end_cmt, is_header=False);

    header += "".join(src_lines[end_line+1:]);
    print(header);
main();

