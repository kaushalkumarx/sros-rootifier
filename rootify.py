import sys
import os

cfg_string = ['/configure']

def rm_insignificant_lines(in_cfg):
    """
    Remove insignificant lines from input config file.
    These lines are starting with '#' or 'echo'
    :param in_cfg: cfg as a multiline string
    :return: 'cleanified' array of config lines
    """
    cfg_arr = in_cfg.splitlines()
    for line in list(cfg_arr):
        if not is_cfg_statement(line):
            cfg_arr.remove(line)
    return cfg_arr


def is_cfg_statement(line):
    if line.strip() == '' or line[0:4] != '    ':
        return False
    else:
        return True


def rootify(clean_cfg, outputCfg):
    prev_ind_level = 0
    for i, line in enumerate(clean_cfg):
        if line.strip() == 'exit':
            cfg_string.pop()
            prev_ind_level -= 4
            continue
        cur_ind_level = len(line) - len(line.lstrip())
        if cur_ind_level > prev_ind_level:
            cfg_string.append(line.strip())
        elif cur_ind_level == prev_ind_level:
            cfg_string.pop()
            cfg_string.append(line.strip())
        prev_ind_level = cur_ind_level
        if i < len(clean_cfg)-1:
            next_ind_level = len(clean_cfg[i + 1]) - len(clean_cfg[i + 1].lstrip())
            if next_ind_level > prev_ind_level:
                continue
            else:
                print(' '.join(cfg_string))
                outputCfg.write(' '.join(cfg_string) + '\n')
        else:
            print(' '.join(cfg_string))
            outputCfg.write(' '.join(cfg_string) + '\n')
    print("""
===========================
    DONE!
    Do not forget to grab your rooted file at {0}""").format(os.path.join(os.getcwd(), 'rooted_' + sys.argv[1]))
    return 0


def run():
    fInput = sys.argv[1]
    with open(fInput, 'r') as inputCfg, \
         open('rooted_'+fInput, 'w') as outputCfg:
        clean_arr = rm_insignificant_lines(inputCfg.read())
        rootify(clean_arr, outputCfg)


if __name__ == "__main__":
    print("""
                     _   _  __ _
                | | (_)/ _(_)
 _ __ ___   ___ | |_ _| |_ _  ___ _ __
| '__/ _ \ / _ \| __| |  _| |/ _ \ '__|
| | | (_) | (_) | |_| | | | |  __/ |
|_|  \___/ \___/ \__|_|_| |_|\___|_|

by Roman Dodin aka @noshut_ru
code is available at https://gitlab.com

I now will try to open input config from {0} file,
rootify it
and then will print 'em to stdout and {1} file!
""").format(sys.argv[1], 'rooted_' + sys.argv[1])
    run()
