##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : srcfile.py                                                    ##
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
import os;
import os.path;
import copy;
import time;
## AmazingCow - Libs
import constants
import comment;
import log;
import gitrepo;


################################################################################
## Public Vars                                                                ##
################################################################################
info = dict.fromkeys(constants.kInfoKeys);

filename      = None;
extension     = None;
comment_start = None;
comment_end   = None;


################################################################################
## Private Vars                                                               ##
################################################################################
_header_lines = [];
_src_lines    = [];
_banner_lines = [];

_comment_real_start = None;
_comment_real_end   = None;

_license_mark_start = None;
_license_mark_end   = None;

_license_line_start = -1;
_license_line_end   = -1;

_shebang_line = None;
_coding_line  = None;


################################################################################
## Public Functions                                                           ##
################################################################################
def read_info(path):
    global filename;
    global _src_lines;

    filename = path;

    ## Check if we have a valid file to work with.
    if(not os.path.exists(filename)):
        log.error("Invalid filename: ({0}".format(filename));
        return;

    ## Read the file.
    _src_lines = open(filename).readlines();

    ## Get the extension and comments for the file.
    _build_comments_info();

    ## Check if we have shebang and coding.
    _check_shebang();
    _check_coding ();

    ## Parse the Header License.
    _parse_license();


def merge_command_line_info(info_dict):
    _merge_info(info_dict);

def merge_rc_info(info_dict):
    _merge_info(info_dict);


def set_banner():
    global _banner_lines;

    if(info["company"] is None or info["company"][0] is None):
        log.error("Missing company name.");

    company = "";
    for c in info["company"][0]:
        if(c.isalnum()): company += c.lower();

    ## COWTODO(n2omatt): Pass the correct path...
    template_filename = os.path.join(
        constants.kPath_Template,
        company + ".template"
    );

    if(not os.path.exists(template_filename)):
        log.error("Template file: ({0}) does not exists.".format(company));

    for line in open(template_filename).readlines():
        _banner_lines.append(line.replace("\n", ""));


def build():
    global  info;
    global  _banner_lines;

    _fill_missing_info();

    output_lines = [];

    ## Header start
    output_lines += _build_header_delimiter(start=True);

    ## Banner
    output_lines += map(fill_center, _banner_lines);

    ## Info
    ordered_keys = copy.deepcopy(constants.kInfoKeys);
    ordered_keys.remove("company");

    for key in ordered_keys:
        print info[key]
        values = info[key];
        lines  = map(fill, _build_info_line(key, values));
        output_lines += lines;

    ## Header End
    output_lines += _build_header_delimiter(start=False);


    ## Insert the coding and shebang if needed.
    if(_coding_line is not None):
        output_lines.insert(0, _coding_line);

    if(_shebang_line is not None):
        output_lines.insert(0, _shebang_line);

    ## The remaining of the source file.
    output_lines += _get_cleaned_source_lines();

    return output_lines;


################################################################################
## Private Functions                                                          ##
################################################################################
## Info building
def _merge_info(info_dict):
    for key in info_dict.keys():
        value = info_dict[key];
        if(value is None):
            continue;

        if(info[key] is None):
            info[key] = [];

        if(value not in info[key]):
            info[key].append(value);

def _fill_missing_info():
    if(info["file"] is None):
        info["file"] = [os.path.basename(filename)];

    if(info["project"] is None):
        info["project"] = [_get_project()];

    if(info["license"] is None):
        info["license"] = [constants.kLicense_Default];

    if(info["copyright"] is None or len(info["copyright"]) == 0):
        info["copyright"] = [_get_copyright()];

    if(info["date"] is None or len(info["date"]) == 0):
        info["date"] = [_get_date()];

def _get_date():
    if(gitrepo.is_valid()):
        return gitrepo.get_date_for_file(filename);

    return time.strftime("%b %d, %Y");

def _get_copyright():
    return "{0} - 2017".format(info["company"][0]);

def _get_project():
    if(gitrepo.is_valid()):
        return os.path.basename(gitrepo.get_url()).replace(".git", "");
    return "";


## Build output lines
def _build_info_line(key, values):
    if(values is None):
        values = [""];

    relevant_keys = copy.deepcopy(constants.kInfoKeys);
    relevant_keys.remove("company"    );
    relevant_keys.remove("description");

    spc     = " " * 2;
    big_spc = " " * 6;
    pad     = " " * (max(map(len, relevant_keys)) - len(key)) + " ";

    is_description = (key == "description");
    key            = key.capitalize();

    if(len(values) == 1 and not is_description):
        return ["{SPC}{0}{PAD}: {1}".format(key, values[0], SPC=spc, PAD=pad)];

    lines = ["{SPC}{0}{PAD}:".format(key, SPC=spc, PAD=pad)];
    for value in values:
        lines.append("{BIGSPC}{0}".format(value, BIGSPC=big_spc));

    if(is_description):
        lines.insert(0, " ");

    return lines;

def _build_header_delimiter(start):
    line = fill(constants.kMark_Start, "-");
    if(start):
        return line;

    line = line.replace("\n", "")[::-1];
    return line + "\n";

def fill_center(line):
    global _comment_real_start;
    global _comment_real_end;

    line = "{0}{1}{2}\n".format(
         _comment_real_start,
        line.center(80 - (len(_comment_real_start) + len(_comment_real_end))),
        _comment_real_end
    );
    return line;

def fill(line, fill_char=" "):
    global _comment_real_start;
    global _comment_real_end;

    spc = fill_char * ((80 - len(_comment_real_end)) - (len(_comment_real_start) + len(line)));
    line = "{0}{1}{SPC}{2}\n".format(
        _comment_real_start,
        line,
        _comment_real_end,
        SPC=spc
    );
    return line;


## Other functions
def _build_comments_info():
    global extension;
    global comment_start;
    global comment_end;

    global _comment_real_start;
    global _comment_real_end;

    global _license_mark_start;
    global _license_mark_end;

    extension = os.path.splitext(filename)[1];

    ## Get the start and end comments for this file.
    comment_start,       comment_end       = comment.get_for_ext     (extension);
    _comment_real_start, _comment_real_end = comment.get_real_for_ext(extension);

    ## Get the start and end License Header marks for this file.
    _license_mark_start = "{0}{1}".format(
        _comment_real_start, constants.kMark_Start
    );
    _license_mark_end = "{0}{1}".format(
        constants.kMark_End, _comment_real_end
    );

def _check_shebang():
    global _shebang_line;

    ## Empty file...
    if(len(_src_lines) == 0):
        return;

    if(_src_lines[0].startswith("#!")):
        _shebang_line = _src_lines[0];

def _check_coding():
    global _coding_line;

    ## Empty file...
    if(len(_src_lines) == 0):
        return;

    ## COWTODO(n2omatt): Implement...
    _coding_line = None;

def _find_header_lines_span():
    global _license_line_start;
    global _license_line_end;

    ## Get the lines that License Header spans...
    for i in range(len(_src_lines)):
        line = _src_lines[i].replace("\n", "");

        if(line.startswith(_license_mark_start)): _license_line_start = i;
        if(line.endswith  (_license_mark_end  )):  _license_line_end   = i;

        if(_license_line_start != -1 and _license_line_end != -1):
            break;

    ## Check if we have a valid span indexes..
    if(_license_line_start == -1 or _license_line_end == -1):
        if(_license_line_start != _license_line_end):
            log.error("Missing License Header markers.");

def _get_cleaned_source_lines():
    index_start = _license_line_start;
    index_end   = _license_line_end;

    ## Don't have a previous License Header.
    if(index_end == -1):
        index_start = 0;

        if(_shebang_line is not None): index_start  = 1;
        if(_coding_line  is not None): index_start += 1;

        index_end = index_start;

    ## Has a previous License Header.
    else:
        index_start = index_end + 1;

    for line in _src_lines[index_start:len(_src_lines)]:
        line = line.replace("\n", "");
        if(len(line) == 0):
            index_end += 1;
        else:
            break;

    lines = _src_lines[index_end:];
    if(lines[0] != "\n"):
        lines.insert(0, "\n");

    return lines;

## Parse License
def _parse_license():
    global info;

    global _header_lines;

    global _license_line_start;
    global _license_line_end;


    ## Empty file...
    if(len(_src_lines) == 0):
        return;

    _find_header_lines_span();

    ## There's nothing to do...
    if(_license_line_start == -1 and _license_line_end == -1):
        return

    ## Convert to zeros, just to ease the operations.
    _license_line_start += 1;
    _header_lines = _src_lines[_license_line_start:_license_line_end];

    _clean_up_header_lines();

    i = 0;
    while(i < len(_header_lines)):
        line = _header_lines[i];

        advance, extracted_info = _extract_info(line, _header_lines[i:]);
        i += advance;

        if(len(extracted_info) == 0):
            continue;

        key    = extracted_info[0];
        values = extracted_info[1];

        while(len(values) > 0 and len(values[ 0]) == 0): values.pop(0);
        while(len(values) > 0 and len(values[-1]) == 0): values.pop();

        info[key] = values;

def _clean_up_header_lines():
    global _header_lines;

    ## Clean up the header lines.
    clean_lines = [];
    for i in range(len(_header_lines)):
        line = _header_lines[i].replace("\n","");

        clean_line = line.lstrip(_comment_real_start).rstrip(_comment_real_end);
        clean_line = clean_line.strip(" ");

        if(len(line) == 0):
            continue;

        clean_lines.append(clean_line);

    _header_lines = clean_lines;

def _line_has_key(line):
    try:
        key, value = line.split(":");
        return True;
    except:
        return False;

def _extract_info(curr_line, remaining_lines):
    if(not _line_has_key(curr_line)):
        return [1, []];

    values = [];

    ## Parse the info.
    key, value = curr_line.split(":");

    ## Clean up..
    key   = key.lower().strip(" ");
    value = value.strip(" ");

    ## Key not recognized.
    ##    Just skip...
    if(not key in info.keys()):
        return [1, []];

    ## Values is on same line of the key...
    if(len(value) != 0):
        values.append(value);

    ## Keep adding values until another key is found
    ## or the lines are over.
    for i in range(1, len(remaining_lines)):
        next_line = remaining_lines[i];

        if(_line_has_key(next_line)):
            return [i, [key, values]];

        values.append(next_line);

    return [len(remaining_lines), [key, values]];




