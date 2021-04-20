#!/usr/bin/python
import os
import subprocess

SHELL = "alacritty"
SHELL_TITLE = "alacritty_popupterm"
SHELL_GEO = "700 500"
SHELL_XY = "640 360"
TMUX = "tmux new-session -A -s popupterm"
exec_cmd = SHELL
exec_cmd += " --config-file "
exec_cmd += "/home/fdlsifu/.config/alacritty_light.yml"
exec_cmd += " -t "
exec_cmd += SHELL_TITLE
exec_cmd += " -e "
exec_cmd += TMUX

NOT_RUNNING = "not_running"
UNMAPPED = "unmapped"

def exec(cmd,get_output=False):
    p = subprocess.Popen(cmd, env=os.environ, stdout=subprocess.PIPE, shell=True)
    if get_output:
        (output,_) = p.communicate()
        return output

def running():
    if exec("xdotool search --name " + SHELL_TITLE,True) == b"":
        return False
    if getwid() == NOT_RUNNING:
        return False
    return True

def toggle():
    wid = getwid()
    cmd = "xdotool "
    if wid == UNMAPPED:
        cmd += "windowmap "
        wid = getwid_unmapped()
        cmd += wid.decode()
        print("raise")
    else:
        cmd += "windowunmap "
        cmd += wid.decode()
        print("hide")
    exec(cmd)
    move(wid)
    resize(wid)


def getwid_unmapped():
    cmd = "xdotool search --name " + SHELL_TITLE
    output = exec(cmd,True)
    return output[:-1]

def getwid():
    cmd = "ps aux | grep '" + exec_cmd + "' | grep -v grep | awk '{print $2}'"
    output = exec(cmd,True)
    if output == b'':
        return NOT_RUNNING
    else:
        pid = output[:-1]
        cmd = "getwindidbypid " + pid.decode()
        output = exec(cmd,True)

        if output == b'':
            return UNMAPPED
        else:
            return output[:-1]

def move(wid):
    if wid == NOT_RUNNING or wid == UNMAPPED:
        return

    cmd = "xdotool windowmove " + wid.decode() + " " + SHELL_XY
    exec(cmd)

def resize(wid):
    if wid == NOT_RUNNING or wid == UNMAPPED:
        return
    cmd = "xdotool windowsize " + wid.decode() + " " + SHELL_GEO
    exec(cmd)

def create():
    exec(exec_cmd)
    wid = getwid()
    while (wid == UNMAPPED):
        wid = getwid()

    move(wid)
    resize(wid)
    print("create")

def main():
    if not running():
        create()
    else:
        toggle()
    
main()
