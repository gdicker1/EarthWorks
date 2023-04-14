#!/usr/bin/env python3

# -- Constants --
LOG_FILE_NAME='update_ext.log'

# -- Imports --
import os
import logging
from pathlib import Path
import argparse
import textwrap
import manic
from manic.utils import execute_subprocess, fatal_error
from manic.externals_description import read_externals_description_file
from manic.externals_description import create_externals_description

def parse_args(args=None):
    '''Setup command-line arguments and parse them'''
    parser = argparse.ArgumentParser()

    parser.add_argument("--cesm-url", "-cu",
            nargs="?",
            default="https://github.com/ESCOMP/CESM",
            help="URL to use for the ESCOMP/CESM repo")
    parser.add_argument("--cesm-tag", "-ct",
            nargs="?",
            required=True,
            help="Tag from ESCOMP/CESM to use to update EarthWorks externals")
    parser.add_argument("--externals",
            nargs="*",
            help="Only do this for specified externals")

    opts = parser.parse_args(args)
    return opts

def exe_stat(cmd):
    return execute_subprocess(cmd, status_to_caller=True)

def exe_ret(cmd):
    return execute_subprocess(cmd, status_to_caller=True, output_to_caller=True)

def get_cesm_extcfg(tag,fpath):
    if fpath.exists():
        return 0
    url = f"https://raw.githubusercontent.com/ESCOMP/CESM/{tag}/Externals.cfg"
    cmd = ['curl', url, '-o', str(fpath)]
    stat = exe_stat(cmd)
    if stat != 0:
        msg = f"Failed to get Externals.cfg file from {url}"
        fatal_error(msg)

    return stat

def get_update_dict(root_dir, ew_file, cesm_file, cesm_tag):
    stat = get_cesm_extcfg(cesm_tag ,cesm_file)

    ew_data = read_externals_description_file(root_dir, ew_ext)
    cesm_data = read_externals_description_file(root_dir, cesm_ext)
    ew_extdesc = create_externals_description(ew_data,
                    components=args.externals, exclude=None)
    cesm_extdesc = create_externals_description(cesm_data,
                     components=args.externals, exclude=None)
    ret = {}
    for k in ew_extdesc.keys():
        e_repo = ew_extdesc[k]['repo']
        if ('EarthWorksOrg' in e_repo['repo_url']
          and k in cesm_extdesc.keys()):
            c_repo = cesm_extdesc[k]['repo']
            url = e_repo['repo_url']
            e_name = url.replace('https://github.com/','').replace('.git','')
            url = c_repo['repo_url']
            c_name = url.replace('https://github.com/','').replace('.git','')
            ret[k] = {
              'local_path':ew_extdesc[k]['local_path'],      
              'repo':{
                     'branch':'ew-develop',
                     'repo_url':e_repo['repo_url'],
                     'name':e_name},
              'upstream':{
                     'repo_url':c_repo['repo_url'],
                     'name':c_name,
                     'tag':c_repo['tag']}
            }
    return ret

def setup_remotes(root_dir, update):
    for k,ext in update.items():
        epath = root_dir / ext['local_path']
        os.chdir(epath)
        
        # Add the remote
        uname = ext['upstream']['name']
        url = ext['upstream']['repo_url']
        cmd = ['git', 'remote', 'add', uname, url]
        stat,oput = exe_ret(cmd)
        ext['fetch'] = {'remote':stat} 
        if stat != 0:
            msg = f"- Failed to add remote {uname} {url} to external {k} in {str(epath)}"
            print(msg)
            print(f'cmd={cmd}\ncmdOut={oput}\n')

        # Fetch the tag from upstream and develop from origin
        utag = ext['upstream']['tag']
        cmd = ['git', 'fetch', uname, 'tag', utag, '--no-tags']
        stat,oput = exe_ret(cmd)
        ext['fetch']['tag'] = stat
        if stat != 0:
            msg = f"- Failed to fetch '{uname}/{utag}'"
            print(msg)
            print(f'cmd={cmd}\ncmdOut={oput}\n')
        cmd = ['git', 'fetch', 'origin', 'ew-develop']
        stat,oput = exe_ret(cmd)
        ext['fetch']['branch'] = stat
        if stat != 0:
            msg = f"- Failed to fetch 'origin/ew-develop'"
            print(msg)
            print(f'cmd={cmd}\ncmdOut={oput}\n')

        os.chdir(root_dir)

def merge_branches(root_dir, update, cesm_tag):
    stat = -1
    for k, ext in update.items():
        if ext['fetch'].get('tag') != 0 or ext['fetch'].get('branch') != 0:
            continue
        epath = root_dir / ext['local_path']
        os.chdir(epath)
        
        # Create branch for the merge
        m_branch = f"update/{cesm_tag}/{k}"
        cmd = ['git', 'checkout', '-b', m_branch, 'origin/ew-develop']
        stat,oput = exe_ret(cmd)
        ext['merge'] = {'branch':m_branch}
        if stat != 0:
            msg = '- Failed to create new branch for merge'
            print(msg)
            print(f'cmd={cmd}\ncmdOut={oput}\n')
            os.chdir(root_dir)

        # Perform the merge
        uname = ext['upstream']['name']
        utag = ext['upstream']['tag']
        name = ext['repo']['name']
        branch = ext['repo']['branch']
        s_msg = f"Merge tag '{utag}' from {uname} into '{branch}'"
        b_msg = f"Update {name} with upstream work from 'ESCOMP/CESM/{cesm_tag}' version."
        cmd = ['git', 'merge', '--no-ff', utag, '-m', s_msg, '-m', b_msg]
        stat,oput = exe_ret(cmd)
        ext['merge']['stat'] = stat
        if stat != 0:
            msg = '- Merge failed'
            print(msg)
            print(f'cmd={cmd}\ncmdOut={oput}\n')
        
        os.chdir(root_dir)
    return

def push_success(rootdir, update):
    for k, ext in update.items():
        if ext['merge']['stat'] == 0:
            os.chdir(root_dir / ext['local_path'])
            branch = ext['merge']['branch']
            cmd = ['git', 'push', 'origin', str(branch)]
            print('cmd={cmd}')
            stat, oput = exe_ret(cmd)
            ext['merge']['push'] = stat
            if stat != 0:
                msg = '- Push failed'
                print(msg)
                print(f'cmd={cmd}\ncmdOut={oput}\n')

            os.chdir(root_dir)   

def git_wrap(summ, body, col=79):
    '''Insert newline every col characters to wrap a body message
    '''
    wrapbod = '\n'.join(textwrap.wrap(body,width=79,break_long_words=False))
    return summ+"\n\n"+wrapbod 

def summarize_update(update):
    print(f'\n\nExternal   | fetch:remote/tag/branch | merge stat | merge branch | pushed')
    print(f'           | (status 0 is success)    |            |')
    print('----------------------------------------------------')
    for k, ext in update.items():
        f_remote = f_tag = f_branch = m_stat = m_branch = m_push = None
        fetch = ext.get('fetch')
        if fetch:
            f_remote = str(fetch.get('remote'))
            f_tag =    str(fetch.get('tag'))
            f_branch = str(fetch.get('branch'))
        merge = ext.get('merge')
        if merge:
            m_stat =   str(merge.get('stat'))
            m_branch = str(merge.get('branch'))
            m_push =   str(merge.get('push'))

        print(f"{k:10} | {f_remote}/{f_tag}/{f_branch} | {m_stat} | {m_branch} | {m_push}")
    print('')

if __name__ == "__main__":
    args = parse_args()
    print(args)
    logging.basicConfig(filename=LOG_FILE_NAME,
                        format='%(levelname)s : %(asctime)s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    root_dir = Path.cwd()
    ew_ext = root_dir / "Externals.cfg"
    cesm_ext = root_dir / f"Externals.{args.cesm_tag}.cfg"
    data_dict = get_update_dict(root_dir, ew_ext, cesm_ext, args.cesm_tag)

    setup_remotes(root_dir, data_dict)
    merge_branches(root_dir, data_dict, args.cesm_tag)
    push_success(root_dir, data_dict)
    summarize_update(data_dict)
    print(f'update:\n{data_dict}')
