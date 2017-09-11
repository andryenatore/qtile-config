# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, hook, layout, widget
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
#from Xlib import display
import os
import sys
import subprocess

mod = "mod4"

if '-d' in sys.argv:
    hostname = 'xephyr'
    mod = "mod4"
    
# utk widgets
bar_defaults = dict(
    size=28,
    background=['#222222','#111111'],
)
layout_defaults = dict(
    border_width=1,
    margin=0,
    border_focus='#336699',
    border_normal='#33333',
)
widget_defaults = dict(
    font='DejaVu Sans Mono for Powerline',
    fontsize=14,
    padding=5,
    background=bar_defaults['background'],
    foreground=['#ffffff', '#ffffff', '#999999'],
    fontshadow='#000000',
)

class Widget(object):
    graph = dict(
        background='#000000',
        border_width=0,
        border_color='#000000',
        line_width=1,
        margin_x=0,
        margin_y=0,
        width=50,
    )

    groupbox = dict(
        active=widget_defaults['foreground'],
        inactive=['#444444', '#333333'],

        this_screen_border=layout_defaults['border_focus'],
        this_current_screen_border=layout_defaults['border_focus'],
        other_screen_border='#444444',

        urgent_text=widget_defaults['foreground'],
        urgent_border='#ff0000',

        highlight_method='block',
        rounded=True,

        # margin=-1,
        padding=3,
        borderwidth=2,
        disable_drag=True,
        invert_mouse_wheel=True,
    )

    sep = dict(
        foreground=layout_defaults['border_normal'],
        height_percent=100,
        padding=5,
    )

    systray = dict(
        icon_size=16,
        padding=5,
    )

    battery = dict(
       energy_now_file='charge_now',
       energy_full_file='charge_full',
       power_now_file='current_now',
    )
    battery_text = battery.copy()
    battery_text.update(
        charge_char='>',
        discharge_char='[|]',
        #format='{char} {hour:d}:{min:02d}',
    )
    weather = dict(
        update_interval=60,
        metric=False,
        format='{condition_text} {condition_temp}',
    )


class Commands(object):
    # ambil lock i3-fancy
    lock = 'lock -gpf Comic-Sans-MS -- scrot -z'
    #autostart = os.path.join(os.path.dirname(__file__), 'bin/autostart')
    vol_up = 'amixer -q set Master 10%+ unmute'
    brght_up = 'xbacklight -inc 10'
    brght_do = 'xbacklight -dec 10'
    vol_do = 'amixer -q set Master 10%- unmute'
    vol_mu = 'amixer -q set Master toggle'
    suspend = os.path.join(os.path.dirname(__file__), 'bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), 'bin/hibernate')


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("urxvt")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    #ogex
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.vol_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.vol_do)),
    Key([], 'XF86AudioMute', lazy.spawn(Commands.vol_mu)),
    Key([], 'XF86MonBrightnessUp', lazy.spawn(Commands.brght_up)),
    Key([], 'XF86MonBrightnessDown', lazy.spawn(Commands.brght_do)),

    Key([mod, "control"], "l", lazy.spawn(Commands.lock)),
]

groups = [Group(i) for i in "asdfuiop"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

border_args = dict(
    border_width=1,
)

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
#    layout.RatioTile(),
#    Layout.Matrix(),
    layout.MonadTall(ratio=0.50),
    layout.Tile(ratio=0.50, masterWindows=2),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.HDDBusyGraph(device='sda', **Widget.graph),
                widget.Prompt(),
                widget.WindowName(),
                widget.Volume(),
                widget.Backlight(
	    	    brightness_file="/sys/class/backlight/intel_backlight/actual_brightness",
		    max_brightness_file="/sys/class/backlight/intel_backlight/max_brightness",
		),
                widget.ThermalSensor(metric=True, threshold=158),
                widget.CPUGraph(graph_color='#18BAEB', fill_color='#1667EB', **Widget.graph),
                widget.MemoryGraph(graph_color='#00FE81', fill_color='00B25B', **Widget.graph),
                widget.NetGraph(graph_color='#ffff00', fill_color='#4d4d00', interface='wlp3s0', **Widget.graph),
                widget.CurrentLayout(),
                widget.BatteryIcon(**Widget.battery),
                widget.Battery(**Widget.battery_text),
                widget.Clock(format='%d-%m-%Y %a %I:%M %p'),
                widget.Systray(**Widget.systray),

            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
#hook.subscribe.startup_once
def autostart():
    home = ls.path.expanduser('/home/andry/.config/qtile/bin/autostart')
    subprocess.call([home])

auto_fullscreen = True
focus_on_window_activation = "never" #"smart"
cursor_wrap = True
follow_mouse_focus = True


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


