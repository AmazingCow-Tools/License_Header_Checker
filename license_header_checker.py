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
import os.path;
import os;
import re;
import subprocess
import time;


################################################################################
##                                                                 ##
################################################################################
def get_git_repo_name(dir_path):
    process = subprocess.Popen(
        ["git-repo-name", dir_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    );

    return process.stdout.read().decode("UTF-8").replace("\n", "");

def read_text_from_file(filename):
    f = open(filename, encoding='utf-8');

    all_lines = f.readlines();
    text      = "".join(all_lines);

    f.close();

    return text;


def write_text_to_file(filename, text):
    f = open(filename, mode="w", encoding="utf-8");

    f.write(text);

    f.close();


################################################################################
##                                                                 ##
################################################################################
def is_shebang_line(line):
    return "#!" in line;

def is_coding_line(line):
    return "# coding" in line;

def is_header_delimiter_line(line, comment_char):
    target_line = (comment_char * 2) + ("-" * 76) + (comment_char * 2);
    return target_line == line;


################################################################################
##                                                                 ##
################################################################################
def find_license_range(text):
    lines = text.split("\n");

    has_shebang = is_shebang_line(lines[0]);
    has_coding  = is_coding_line (lines[0]);

    if(has_shebang):
        has_coding = is_coding_line(lines[1]);


    ## Caclulate the where the actual license starts (or should start).
    start_line = 0;
    if(has_shebang): start_line = 1;
    if(has_coding ): start_line = 2;

    ## Check if we have already a license
    is_delimiter = is_header_delimiter_line(lines[start_line], "#"); ##COWTODO: Remove the hard cmt type
    if(not is_delimiter):
        return [start_line, -1]; ## Has not License Header.

    ## Calculate where the license ends.
    end_line = (start_line + 1);
    while(True):
        is_delimiter = is_header_delimiter_line(lines[end_line], "#"); ##COWTODO: Remove the hard cmt type
        ## Found where the license ends.
        if(is_delimiter):
            break

        end_line += 1;

    ## Calculate the License range.
    start_range = 0;
    for i in range(0, start_line):
        start_range += (len(lines[i]) + 1); ## +1 for newlines

    end_range = start_range;
    for i in range(start_line , end_line + 1):
        end_range += (len(lines[i]) + 1); ## +1 for newlines


    return [start_range, end_range -1]; ## -1 is to remove the last newline


def find_copyright_range(text):
    lines = text.split("\n");

    ## Find the copyright line.
    copyright_index = -1;
    for i in range(0, len(lines)):
        line = lines[i];
        m = re.search("Copyright \(c\) [0-9]{4}", line);
        if(m is not None):
            copyright_index = i;
            break;

    ## Calculate the range.
    start_range = 0;
    for i in range(0, copyright_index):
        start_range += (len(lines[i]) + 1); ## +1 for newlines

    end_range = start_range + len(lines[copyright_index]);

    return [start_range, end_range];


def find_copyright_years(text, copyright_range):
    copyright_text = text[copyright_range[0] : copyright_range[1]];
    m = re.findall("[0-9]{4}", copyright_text);
    return list(map(int, m));


################################################################################
##                                                                 ##
################################################################################
def update_license(
    file_name,
    project_name,
    curr_year,
    copyright_years,
    comment_char):

    template = read_text_from_file("license_template.text");

    ## Filename
    template = re.sub("FILENAME", file_name,    template);

    ## Project
    template = re.sub("PROJECT",  project_name, template);

    ## Copyright years.
    ## Add the current year and make sure that the years
    ## are unique by turning the list into set.
    copyright_years.append(curr_year)
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
    return template;


def run():
    # file_path    = "/home/n2omatt/Documents/Projects/AmazingCow/AmazingCow-Game-Framework/bootstrap_game/scripts/clone_cocos2dx.sh";
    file_path = "license_header_checker.py"
    dir_path     = os.path.dirname  (file_path);
    file_name    = os.path.basename (file_path);
    project_name = get_git_repo_name(dir_path);
    curr_year    = time.gmtime().tm_year;

    text            = read_text_from_file (file_path);
    license_range   = find_license_range  (text);
    copyright_range = find_copyright_range(text);
    copyright_years = find_copyright_years(text, copyright_range);

    updated_text = update_license(
        file_name,
        project_name,
        curr_year,
        copyright_years,
        "#"
    ) + "\n";

    if(license_range[1] == -1):
        license_range[1] = 0;

    final_text =  text[:license_range[0]];
    final_text += updated_text;
    final_text += text[license_range[1]:];


    write_text_to_file("license_header_checker.py", final_text);


    # print(text[license_range[0] : license_range[1]])
    # print(text[copyright_range[0] : copyright_range[1]])

    # print(copyright_years);

run();


# class InsertDatetimeCommand(sublime_plugin.TextCommand):
    # def run(self, edit):
        # full_file_name = self.view.file_name();
        # file_name      = os.path.basename (full_file_name);
        # dir_name       = os.path.dirname  (full_file_name);

        # curr_year      = time.gmtime().tm_year;


        # print(full_file_name);
        # print(file_name);
        # print(curr_year);
        # print(project_name);

        # ## Amazing Cow License
        # license_region = sublime.Region(0, 81 * 39);
        # license_substr = self.view.substr(license_region);


