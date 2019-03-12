#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Controls.sqlhelper import sqlhelper
from json import dumps

sql_guy = sqlhelper()


def load_status_sql():
    return sql_guy.readstatus()


def write_command_sql(**kwargs):
    for key, value in kwargs.items():
        if key == 'colors':
            sql_guy.entercommand(command=key, arg1=value[0], arg2=value[1], arg3=value[2])
        elif key == 'save':
            sql_guy.addcolortodb(name=value[1], hexcode=value[0])
        elif key == 'addmode':
            sql_guy.addmode(name=value[0], scheme=value[1])
        elif key == 'deletemode':
            sql_guy.deletemode(modekey=value)
        else:
            sql_guy.entercommand(command=key, arg1=value)


def get_colors():
    colors = sql_guy.getcolors()
    color_dict = {}
    for color in colors:
        color_dict.update({color[0]: color[1]})
    return color_dict


def get_modes():
    modes = sql_guy.getmodenames()
    return modes


def get_color_hex(color_id):
    return sql_guy.getcolorhex(color_id)


def clean_javascript_text(input_string):
    if isinstance(input_string, str):
        output_string = input_string.replace('"', "'").replace('\r\n', '\n').replace('\n', '<br>')
    else:
        output_string = ''
    return output_string


def convert_rgb_to_hex(red, green, blue):
    a = '0x{:02x}'.format(red).replace('0x', '#')
    b = '0x{:02x}'.format(green).replace('0x', '')
    c = '0x{:02x}'.format(blue).replace('0x', '')
    x = a + b + c
    return x


def make_mode_color_list_dict():
    mode_details = sql_guy.getmodes()
    mode_dict = {}
    colors = get_colors()
    for mode in mode_details:
        if int(mode[0]) > 8:
            color_list = []
            for color_id in list(eval(mode[3])):
                color_list.append(colors[color_id])
            mode_dict.update({mode[0]: {'color_list': color_list, 'name': mode[1]}})
    return mode_dict


def make_custom_color_dict():
    color_details = sql_guy.getcolors()
    color_dict = {}
    hex_list = []
    for color in color_details:
        if int(color[0]) > 8:
            color_dict.update({color[0]: {'name': color[1], 'hex': color[2]}})
            hex_list.append(color[2])
    return color_dict, dumps(hex_list)
