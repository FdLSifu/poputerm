#!/usr/bin/python
import os
from Xlib.display import Display

shell = "/home/fdlsifu/Documents/tools/st/st -g 90x24+700+315 -e tmux new-session -A -s popterm"
shell_wmclass = "st-256color"
shell_window = None
shell_name = "st"

def close_term():
    try:
        f = open('/tmp/popupterm_pid','r')
        pid = int(f.read())
        f.close()
        os.system('kill -9 '+str(pid))
    except:
        pass

def launch_term():
    popupterm_pid = os.spawnvpe(os.P_NOWAIT, shell.split(' ')[0] , shell.split(' '),os.environ)
    f = open('/tmp/popupterm_pid','w')
    f.write(str(popupterm_pid))
    f.close()

def findWindowHierrarchy(window,wmclass):
    global shell_window
    children = window.query_tree().children
    for w in children:
        if shell_window:
            break
        current_class = w.get_wm_class()
        if current_class and wmclass == current_class[0]:
            shell_window = w
        findWindowHierrarchy(w,wmclass)

def is_launched():
    global shell_window

    display = Display()
    root = display.screen().root
    findWindowHierrarchy(root,shell_wmclass)
    if shell_window:
        return True
    else:
        return False


if not is_launched():
    launch_term()
else:
    close_term()