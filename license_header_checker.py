#!/usr/bin/env python3
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        license_header_checker.py                 ##
##            █ █        █ █        License_Header_Checker                    ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2017                        ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

################################################################################
## Imports                                                                    ##
################################################################################
import getopt;
import os.path;
import os;
import pdb;
import re;
import subprocess
import sys;
import time;


################################################################################
## Global vars                                                                ##
################################################################################
g_is_to_check     = False;
g_verbose_log     = False;
g_years           = set();
g_n2omatt_license = False;


################################################################################
## Show Help / Version / Error                                                ##
################################################################################
def show_help(exit_code):
    print("I have no help for now.... sorry :x");
    exit(exit_code);

def show_version():
    print("Amazing Cow - License Header Checker v0.1.0");
    exit(0);

def show_error(*args):
    print("[FATAL] {0}".format(
        "".join(args)
    ));
    exit(1);


################################################################################
## Debug                                                                      ##
################################################################################
def debug(*args):
    # if(g_verbose_log):
    print("".join(map(str, args)));

def print_range(range, text):
    # if(g_verbose_log):
    print(repr(text[range[0]:range[1]]));
        # print(text[range[0]:range[1]]);


################################################################################
##                                                                 ##
################################################################################
def get_git_repo_name(dir_path):
    cwd = os.getcwd();
    os.chdir(dir_path);

    process = subprocess.Popen(
        ["basename $(git config --get remote.origin.url) .git", dir_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    );

    name = process.stdout.read().decode("UTF-8").replace("\n", "");
    os.chdir(cwd);
    return name;


def read_text_from_file(filename):
    f = open(filename, encoding='utf-8');

    all_lines = f.readlines();
    text      = "".join(all_lines);

    f.close();

    return text;


def write_text_to_file(filename, text):
    # debug(text);
    f = open(filename, mode="w", encoding="utf-8");
    f.write(text);
    f.close();



################################################################################
##                                                                 ##
################################################################################
def is_shebang_line(line):
    ## COWTODO(n2omatt): Use regex to check .
    return "#!" in line;

def is_coding_line(line):
    m = re.search("#\ *coding.*", line)
    return m is not None;

def is_header_delimiter_line(line, comment_char):
    ## COWTODO(n2omatt): Use regex to check .
    target_line = (comment_char * 2) + ("-" * 76) + (comment_char * 2);
    return target_line == line;

def count_chars_up_to_line(line_index, lines):
    chars_count = 0;
    for i in range(0, line_index):
        chars_count += (len(lines[i]) + 1); ## +1 for newlines
    return chars_count;

def line_for_chars_count(chars_count, lines):
    count = 0;
    for line_index in range(0, len(lines)):
        curr_line = lines[line_index];
        count    += (len(curr_line) + 1); ##+1 is for new line.

        if(count == chars_count):
            return line_index;

    return -1;


def get_comment_char_for_file(filename):
    ext = os.path.splitext(filename)[1];
    if(ext is None or len(ext) == 0):
        return "#"; ## COWTODO(n2omatt): Use file(1) to guess the type.

    if(ext in ".h"  ): return "/";
    if(ext in ".cpp"): return "/";

    if(ext in ".cs" ): return "/";

    if(ext in ".py"): return "#";
    if(ext in ".sh"): return "#";

    if(ext in ".js" ): return "/";
    if(ext in ".jsx"): return "/";



################################################################################
##                                                                 ##
################################################################################
def find_license_range(text, comment_char):
    lines = text.split("\n");

    has_shebang = is_shebang_line(lines[0]);
    has_coding  = is_coding_line (lines[0]);

    if(has_shebang):
        has_coding = is_coding_line(lines[1]);

    debug("Has shebang: ", has_shebang);
    debug("Has coding : ", has_coding );

    ## Caclulate the where the actual license starts (or should start).
    start_line = 0;
    if(has_shebang): start_line = 1;
    if(has_coding ): start_line = 2;

    debug("Starting seaching license on line: ", start_line);

    ## Check if we have already a license
    ## COWTODO(n2omatt): Is possible to have the license bellow...
    ## We must take care of this...
    found_delimiter = False;
    is_delimiter    = is_header_delimiter_line(lines[start_line], comment_char);
    if(is_delimiter):
        found_delimiter = True;

    if(not found_delimiter):
        start_index = count_chars_up_to_line(start_line, lines);
        debug("Did not found a start license delimiter");
        debug("start_index is: ", start_index);
        return [start_index, start_index];

    ## Calculate where the license ends.
    found_delimiter = False;
    end_line        = (start_line + 1);
    while(True):
        is_delimiter = is_header_delimiter_line(lines[end_line], comment_char);
        ## Found where the license ends.
        if(is_delimiter):
            found_delimiter = True;
            break;

        end_line += 1;
        if(end_line >= len(lines)):
            break;

    if(not found_delimiter):
        start_index = count_chars_up_to_line(start_line, lines);
        debug("Did not found a end license delimiter");
        debug("start_index is: ", start_index);
        return [start_index, start_index];

    debug("License spans on lines: ", start_line, " to ", end_line);

    ## Calculate the License range.
    start_range   = count_chars_up_to_line(start_line,  lines);
    end_range     = count_chars_up_to_line(end_line +1, lines);
    license_range = [start_range, end_range];

    debug("License range is: ", license_range);
    # debug("License text is:");
    # print_range(license_range, text);

    return license_range;

def find_date_range(text):
    lines = text.split("\n");

    ## Find the date line.
    date_line = -1;
    for i in range(0, len(lines)):
        line = lines[i];
        m = re.search("Date      : ", line);
        if(m is not None):
            date_line = i;
            break;

    debug("Date line is: ", date_line);
    if(date_line == -1):
        debug("Did not found Date info");
        return [-1, -1];

    ## Found...
    start_range = count_chars_up_to_line(date_line,    lines);
    end_range   = count_chars_up_to_line(date_line +1, lines);
    date_range  = [start_range, end_range];

    debug("Date range is: ", date_range);
    return date_range;


def find_date_info(text, date_range):
    if(date_range == [-1, -1]):
        return time.strftime("%B %d, %Y");

    ## First take the substring the represents the date line from text.
    date_info = text[date_range[0] : date_range[1]];

    ## Now due the format that we're using, skip the !! Date      : substr
    ## and only gets enough to be a complete date but without the last chars
    ## delimiters.
    ## COWNOTE: This is nasty... but is working for now.
    date_info = date_info[15: 65];

    debug("Date info is: ", date_info);
    return date_info.strip(" ");


def find_copyright_range(text):
    lines = text.split("\n");

    ## Find the copyright line.
    copyright_line = -1;
    for i in range(0, len(lines)):
        line = lines[i];
        m = re.search("Copyright \(c\) [0-9]{4}", line);
        if(m is not None):
            copyright_line = i;
            break;

    debug("Copyright line is: ", copyright_line);

    ## Not found...
    if(copyright_line == -1):
        debug("Did not found Copyright info");
        return [-1, -1];

    ## Found...
    start_range     = count_chars_up_to_line(copyright_line,    lines);
    end_range       = count_chars_up_to_line(copyright_line +1, lines);
    copyright_range = [start_range, end_range];

    debug("Copyright range is: ", copyright_range);
    # debug("Copyright text is:");
    # print_range(copyright_range, text);

    return copyright_range


def find_copyright_years(text, copyright_range):
    copyright_text = text[copyright_range[0] : copyright_range[1]];
    m = re.findall("[0-9]{4}", copyright_text);

    years = list(map(int, m));
    debug("Copyright years : ", years);

    return years;


################################################################################
##                                                                 ##
################################################################################
def update_license(
    file_name,
    project_name,
    curr_year,
    copyright_years,
    date_info,
    comment_char):

    license_file = "n2omatt_license_template.txt" if g_n2omatt_license else "amazingcow_license_template.txt";
    template     = read_text_from_file(
        os.path.join("/usr/local/share", license_file)
    );

    ## Filename
    template = re.sub("FILENAME", file_name, template);

    ## Project
    template = re.sub("PROJECT",  project_name, template);

    ## Date
    template = re.sub("DATE", date_info, template);

    ## Copyright years.
    ## Add the current year and make sure that the years
    ## are unique by turning the list into set.
    for year in g_years:
        copyright_years.append(int(year));

    copyright_years.append(curr_year);
    copyright_years = list(set(copyright_years));
    copyright_years.sort();


    final_copyright = "";
    if(len(copyright_years) > 2):
        final_copyright = str(copyright_years[0]) + " - " + str(copyright_years[-1]);
    elif(len(copyright_years) == 2):
        final_copyright = str(copyright_years[0]) + ", " + str(copyright_years[-1]);
    else:
        final_copyright = str(copyright_years[0]);

    template = re.sub("YEARS",  final_copyright, template);

    debug("Final copyright years: ", final_copyright);


    ## Comment chars
    template = re.sub("!!",  comment_char * 2, template);

    ## Add the last comment chars on lines
    lines = template.split("\n");
    for i in range(0, len(lines)-1):
        ## Already filled line.
        if(len(lines[i]) == 80): ## 80 is our limit
            continue;

        spaces_to_add = 78 - len(lines[i]); ## 78 because the 2 comments chars.
        lines[i] += (" " * spaces_to_add) + (comment_char * 2);

    template = "\n".join(lines);
    template = template[:-1]; ## Remove the tralling \n

    return template;


def run(file_path):
    dir_path     = os.path.dirname  (file_path);
    file_name    = os.path.basename (file_path);
    project_name = get_git_repo_name(dir_path);
    curr_year    = time.gmtime().tm_year;
    comment_char = get_comment_char_for_file(file_path);

    text            = read_text_from_file (file_path            );
    license_range   = find_license_range  (text, comment_char   );
    date_range      = find_date_range     (text                 );
    date_info       = find_date_info      (text, date_range     );
    copyright_range = find_copyright_range(text                 );
    copyright_years = find_copyright_years(text, copyright_range);

    old_license_text = text[license_range[0] : license_range[1]-1];
    new_license_text = update_license(
        file_name,
        project_name,
        curr_year,
        copyright_years,
        date_info,
        comment_char
    );

    same_license = (old_license_text == new_license_text);
    if(g_is_to_check):
        if(same_license):
            debug("Has License Header.");
            exit(0); ## Success...

        else:
            debug("Has not License Header.");
            exit(1); ## Fail...

    if(same_license):
        debug("License is the same - Skipping update.");
        return;

    debug("license_range   :", license_range  );
    debug("copyright_range :", copyright_range);

    # pdb.set_trace();
    first_part      = text[:license_range[0]];
    updated_license = new_license_text + "\n\n";
    last_part       = text[license_range[1]:].lstrip("\n");
    final_text      = first_part + updated_license + last_part;

    write_text_to_file(file_path, final_text);



################################################################################
## Entry Point                                                                ##
################################################################################
def main():
    global g_is_to_check;
    global g_verbose_log;
    global g_years;
    global g_n2omatt_license;

    ## Init the getopt.
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "",
            ["help", "version", "check", "verbose", "year=", "n2omatt"]
        );
    except Exception as e:
        raise

    ## No given filenames to check.
    if(len(args) == 0):
        show_error("Missing filename.");

    ## Default options.
    g_is_to_check     = False;
    g_verbose_log     = False;
    g_years           = set();
    g_n2omatt_license = False;

    ## Parse the given command line options.
    for option, argument in opts:
        ## Help / Version
        if "help" in option:
            show_help(0);
        elif "version" in option:
            show_version();

        ## Check
        elif "check" in option:
            g_is_to_check = True;

        ## Verbose
        elif "verbose" in option:
            g_verbose_log = True;

        ## Years
        elif "year" in option:
            g_years.add(int(argument));

        ## N2OMatt license
        elif "n2omatt" in option:
            g_n2omatt_license = True;

    ## Run.
    try:
        run(args[0]);
    except Exception as e:
        print(e);
        exit(1);

if __name__ == '__main__':
    main();
