#!/usr/bin/python3
import pdb;

################################################################################
## Constants                                                                  ##
################################################################################
slash_cmt = [
    ## C / C++
    "cpp",
    "c",
    "h",
    "hpp",
    ## ObjC
    "m",
    "mm",
    ## C#
    "cs",
    # Javascript
    "js",
    "jsx",
    ## Action Script
    "as3",
    ## PHP
    "php",
];

hash_cmt = [
    ## Shell
    "sh",
    ## SQL
    "sql",
    ## Python
    "py",
];

other_cmt = {
    "html" : ["<!-- ", "-", " -->"]
};


################################################################################
## Run Info                                                                   ##
################################################################################


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
## Comment Functions                                                          ##
################################################################################
def get_start_comment_for_ext(ext):
    ## Extension isn't in any list,
    ##    Check if it is a 'special' extension...
    if(ext in other_cmt.keys()):
        return other_cmt[ext][0];

    ## Check which list is the ext...
    if  (ext in slash_cmt): return "/";
    elif(ext in hash_cmt ): return "#";

    ## Can't find the ext...
    ##    Probally a script file without ext...
    return "#";

def get_end_comment_for_ext(ext):
    ## Extension isn't in any list,
    ##    Check if it is a 'special' extension...
    if(ext in other_cmt.keys()):
        return other_cmt[ext][2];

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
def setup_info(info_lines, info_dict):
    filled_lines = [];
    for line in info_lines:
        end_index = line.find(":");

        ## Get the tag value.
        tag = line[0 : end_index].strip().lower();

        ## Some tags has special handling...
        value = info_dict[tag];
        if(tag == "copyright"):
            value = build_copyright_years(info_dict[tag]);

        ## COWTODO(n2omatt): Comment about the code bellow...
        if(tag == "description"):
            filled_lines.append(""); ## Empty line to give separate Description:
            filled_lines.append(line);
            for desc_line in info_dict[tag]:
                desc_spaces      = " " * 5;
                filled_line = desc_spaces + desc_line;
                filled_lines.append(filled_line);
            continue;

        print(tag);
        ## Build the line...
        spaces      = " ";
        filled_line = line + spaces + value;
        filled_lines.append(filled_line);

    return filled_lines;

def build_copyright_years(years_list):
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
def fill(start, end, content, center, start_spacing, fill_char = " "):
    real_start = get_real_comment_str(start);
    real_end   = get_real_comment_str(end  );

    ## Put spaces only if needed.
    start_spc      = "" if real_start[-1] == " " or start_spacing == False else " ";
    hard_spc_count = len(real_start) + len(real_end) + len(start_spc);

    filled_content = content;
    if(center):
        content_len    = len(content);
        content_fill   = fill_char * int((((80 - hard_spc_count) - content_len) / 2));
        filled_content = "{0}{1}{0}".format(content_fill, content);

    line  = real_start + start_spc + filled_content;
    line += fill_char * (80 - len(real_end) - len(line)) + real_end;

    return line;

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

    return filled;


################################################################################
## Source File Parser Functions                                               ##
################################################################################
def clean_src_line(src_line, real_start_cmt, real_end_cmt, info_line):
    return src_line                  \
        .replace(info_line,      "") \
        .replace(real_start_cmt, "") \
        .replace(real_end_cmt,   "") \
        .replace("\n",           "") \
        .strip();

def find_description_from_src_lines(src_lines, start_cmt, end_cmt):
    real_start_cmt = get_real_comment_str(start_cmt);
    real_end_cmt   = get_real_comment_str(end_cmt  );

    desc_lines = [];
    for l in src_lines:
        clean_line = clean_src_line(l, real_start_cmt, real_end_cmt, "");
        desc_lines.append(clean_line);

    return desc_lines;

def find_value_from_src_lines(info_line, src_lines, start_cmt, end_cmt):
    real_start_cmt = get_real_comment_str(start_cmt);
    real_end_cmt   = get_real_comment_str(end_cmt  );

    for i in range(len(src_lines)):
        src_line = src_lines[i];
        key       = info_line.replace(":", "").strip();

        if(key not in src_line):
            continue;

        ## Clean key.
        key = key.lower();
        if(key == "description"):
            value = find_description_from_src_lines(
                src_lines[i+1:],
                start_cmt,
                end_cmt
            );
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

def parse_src_lines(src_file_lines, start_cmt, end_cmt):

    start_line, end_line = get_header_comment_lines_indexes(
        src_file_lines,
        start_cmt,
        end_cmt
    );
    header_lines = src_file_lines[start_line:end_line];

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
import sys;
import os;
import os.path;
import getopt;

class RunInfo:
    no_rc   = False;
    verbose = False;
    dry_run = False;

    project   = None;
    author    = None;
    date      = None;
    license   = None;
    copyright = None;
    company   = None;

    filename = None;

    rc_info_dict = {};


def parse_command_line_options():
    try:
        cmd_options = getopt.gnu_getopt(
            sys.argv[1:],
            "",
            [
                ## Help / Version
                "help",
                "version",

                ## Run Control
                "no-rc",
                "verbose",
                "dry-run",

                ## Info Flags
                "project=",
                "author=",
                "date=",
                "license=",
                "copyright=",
                "company="
            ]
        );

        for flag, value in cmd_options[0]:
            ## Help / Version
            if  ("help"    in flag): show_help   ();
            elif("version" in flag): show_version();

            ## Run Control
            elif("no-rc"   in flag): RunInfo.no_rc    = True;
            elif("verbose" in flag): RunInfo.verbose  = True;
            elif("dry-run" in flag): RunInfo.dry_run  = True;

            ## Info Flags
            elif("project"   in flag): RunInfo.project   = value;
            elif("author"    in flag): RunInfo.author    = value;
            elif("date"      in flag): RunInfo.date      = value;
            elif("license"   in flag): RunInfo.license   = value;
            elif("copyright" in flag): RunInfo.copyright = value;
            elif("company"   in flag): RunInfo.company   = value;


        if(len(cmd_options[1]) == 0):
            show_error("Missing filename.");
        else:
            RunInfo.filename = cmd_options[1][0];

    except:
        raise

def read_rc():
    root_path = os.path.abspath(".");
    if(is_git_repo()):
        root_path = get_git_repo_root();

    fullpath = os.path.join(root_path, "lhc.rc");

    if(not os.path.exists(fullpath)):
        RunInfo.rc_info_dict = None;
        show_warning("Missing lhc.rc file on project root.");
        return;

    for line in open(fullpath).readlines():
        key, value = line.split(":");

        key   = key.strip  ();
        value = value.strip();

        RunInfo.rc_info_dict[key] = value;


##COWTODO(n2omatt): pip install gitpython
import git;
def is_git_repo():
    return get_git_repo_root() is not None;

def get_git_repo_root():
    try:
        return git.Repo(search_parent_directories=True).working_tree_dir;
    except:
        return None;


def getrc_value(key, info_dict):
    if(key in RunInfo.rc_info_dict.keys()):
        return RunInfo.rc_info_dict[key];

    if(key in info_dict.keys()):
        return info_dict[key];

    return "Minha bundinha...";


def setup_run_info(info_dict):
    if(RunInfo.project   is None): RunInfo.project   = getrc_value("project",   info_dict);
    if(RunInfo.author    is None): RunInfo.author    = getrc_value("author",    info_dict);
    if(RunInfo.date      is None): RunInfo.date      = getrc_value("date",      info_dict);
    if(RunInfo.license   is None): RunInfo.license   = getrc_value("license",   info_dict);
    if(RunInfo.copyright is None): RunInfo.copyright = getrc_value("copyright", info_dict);
    if(RunInfo.company   is None): RunInfo.company   = getrc_value("company",   info_dict);

    RunInfo.rc_info_dict["project"  ] = RunInfo.project;
    RunInfo.rc_info_dict["author"   ] = RunInfo.author;
    RunInfo.rc_info_dict["date"     ] = RunInfo.date;
    RunInfo.rc_info_dict["license"  ] = RunInfo.license;
    RunInfo.rc_info_dict["copyright"] = RunInfo.copyright;
    RunInfo.rc_info_dict["company"  ] = RunInfo.company;
    RunInfo.rc_info_dict["file"     ] = RunInfo.filename;

    RunInfo.rc_info_dict["description"] = RunInfo.filename;

def main():
    parse_command_line_options();
    read_rc();

    ## Read the source file.
    src_lines = open(RunInfo.filename).readlines();

    extension = os.path.splitext(RunInfo.filename);
    start_cmt = get_start_comment_for_ext(extension);
    end_cmt   = get_end_comment_for_ext  (extension);

    start_line, end_line = get_header_comment_lines_indexes(
        src_lines,
        start_cmt,
        end_cmt
    );

    info_dict = parse_src_lines(
        src_lines[start_line:end_line],
        start_cmt,
        end_cmt
    );

    setup_run_info(info_dict);

    info_lines = setup_info(
        read_template_info(),
        RunInfo.rc_info_dict
    );

    print(info_lines);
main();


# start_cmt = get_start_comment_for_ext("m");
# end_cmt   = get_end_comment_for_ext  ("m");

# info       = parse_src_file("teste.cpp", start_cmt, end_cmt);
# info_lines =

# print(
#     fill_header_footer(
#         start_cmt,
#         end_cmt,
#         is_header=True
#     )
# );

# for l in read_template_header("n2omatt"):
#     print(
#         fill(
#             start_cmt,
#             end_cmt,
#             l,
#             center=True,
#             start_spacing=False,
#             fill_char=" "
#         )
#     );

# for l in info_lines:
#     print(
#         fill(
#             start_cmt,
#             end_cmt,
#             l,
#             center=False,
#             start_spacing=False,
#             fill_char=" "
#         )
#     );

# print(
#     fill_header_footer(
#         start_cmt,
#         end_cmt,
#         is_header=False
#     )
# );
