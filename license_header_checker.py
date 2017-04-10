import os;
import os.path;
import time;
import subprocess


def get_git_repo_name(dir_path):
    process = subprocess.Popen(
        ["git-repo-name", curr_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    );

    return process.stdout.read().decode("UTF-8").replace("\n", "");



def is_shebang_line(line):
    return "#!" in line;

def is_coding_line(line):
    return "# coding" in line;

def is_header_delimiter_line(line, comment_char):
    target_line = (comment_char * 2) + ("-" * 76) + (comment_char * 2);
    return target_line == line;


def find_license_header(text):
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
        start_range += (len(lines[i]) + 1); ##+1 for newlines

    end_range = 0;
    for i in range(start_line , end_line + 1):
        end_range += (len(lines[i]) + 1); ##+1 for newlines


    return [start_range, end_range -1]; ##-1 is to remove the last newline



def read_text_from_file(filename):
    f = open(filename, encoding='utf-8');

    all_lines = f.readlines();
    text      = "".join(all_lines);

    return text;


def run():
    path = "/home/n2omatt/Documents/Projects/AmazingCow/AmazingCow-Game-Framework/bootstrap_game/scripts/clone_cocos2dx.sh";
    text = read_text_from_file(path);

    license_range = find_license_header(text);

    print(text[range[0] : range[0] + range[1]])

run();


# class InsertDatetimeCommand(sublime_plugin.TextCommand):
    # def run(self, edit):
        # full_file_name = self.view.file_name();
        # file_name      = os.path.basename (full_file_name);
        # dir_name       = os.path.dirname  (full_file_name);
        # project_name   = get_git_repo_name(dir_name);
        # curr_year      = time.gmtime().tm_year;


        # print(full_file_name);
        # print(file_name);
        # print(curr_year);
        # print(project_name);

        # ## Amazing Cow License
        # license_region = sublime.Region(0, 81 * 39);
        # license_substr = self.view.substr(license_region);


