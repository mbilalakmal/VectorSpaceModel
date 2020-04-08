# -----------------------------------------------------------
# This module defines the GUI.
#
# A GUI window asks user for:
# (1) Parameters which is to be evaluated,
# (2) range of values to test for the selected parameter,
# (3) values of remaining parameters
# (4) Trials - this is how many times each configuration is run
#
# After user describes everything, the app does heavy computing
# on the main thread (causing the GUI to hang) and draws a graph.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import PySimpleGUI as sg
import numpy as np

from vsm_indexer import generate_index_file
from query_parser import resolve_vsm_query

sg.theme('DarkAmber')

layout = [  [sg.Text('')],
            [sg.Image(r'resources\icon.png'), sg.Text('Vector Space Model', font=('Helvetica', 16))],
            [sg.Text('A Search Engine For Trump\'s Speeches.', font=('Helvetica', 9))],
            [sg.Input(key='_QUERY_'), sg.Button('SEARCH', bind_return_key=True)],
            [sg.Text('')],
            [
                sg.Text('Aplha'),
                sg.Spin(
                    [i for i in np.linspace(0.0001,0.1000, 1000)],
                    initial_value=0.0005,
                    size=(10,1),
                    key='_ALPHA_'
                    )   # spinner for alpha value
            ],
            [sg.Text('')],
            [sg.Text(size=(48,6), key='_DOCS_')],
            [sg.Text('')],
            [sg.Text(size=(4, 1), key='_SIZE_')],
            [sg.Button('Build Index')],
            [sg.Text('')]
        ]

window = sg.Window(
    title='Information Retreival - Assignment 2',
    layout=layout,
    resizable=True,
    element_padding=(4, 4),
    element_justification='center'
)

while True:
    event, values = window.read()
    if event is None:
        break

    if event == 'SEARCH':

        query = values['_QUERY_']
        alpha = values['_ALPHA_']

        if not query:
            continue

        result = resolve_vsm_query(query, alpha)
        display = ', '.join(result)
        size = len(result)

        print(f'Relevant speeches: {display}')
        print(f'Number of relevant documents: {size}')
        print()

        window['_DOCS_'].update(display)
        window['_SIZE_'].update(size)
        
    elif event == 'Build Index':
        generate_index_file()

window.close()