import PySimpleGUI as sg
import sys

import Variables as var

class WindowManager:

    @staticmethod
    def getMainWindow():
        layout = [[sg.Text('Enter youtube music url:')],
                  [sg.Input(key='-INPUT-')],
                  [sg.Button('Recommend'), sg.Button('Random')]]
        return sg.Window('Music Recommender', layout)

    @staticmethod
    def getNewSongsWindow():
        layout = [[sg.Text('Not analyzed sounds found.\nDo you want to analyze them?')],
                  [sg.Button('Yes'), sg.Button('No')]]
        return sg.Window('New sounds found', layout)

    @staticmethod
    def getProgressWindow():
        layout = [[sg.Text('Progress (0%)', key='-PERCENT-')],
                  [sg.ProgressBar(1, key='-PROGRESS-')]]
        return sg.Window('Analyzing new sounds', layout)

    @staticmethod
    def updateProgressWindow(window, label: str, i: int, max: int):
        if window is None:
            return
        window['-PERCENT-'].update(value=label + ' (' + str(i / max * 100) + '%)')
        window['-PROGRESS-'].update(current_count=i, max=max)

    @staticmethod
    def getPlayerWindow():
        layout = [[sg.Text('Loading track...', key='-TITLE-')],
                  [sg.Button('Like', key='-LIKE-'),
                   sg.Button('Pause', key='-PLAY-PAUSE-'),
                   sg.Button('Dislike', key='-DISLIKE-'),
                   sg.Button('Next', key='-NEXT-')],
                  [sg.Text('Volume:'),
                   sg.Slider(range=(0, 100), default_value=var.START_VOLUME,
                             orientation='h', enable_events=True,
                             disable_number_display=True, key='-VOL-')]]
        return sg.Window('Recommender player', layout)


class WindowHandler:

    def __init__(self, window):
        self._window = window
        self._actions = {}

    def addAction(self, event: str, action):
        self._actions[event] = action

    def addCloseAction(self, action):
        self._actions['CLOSED'] = action

    def handle(self) -> bool:
        event, values = self._window.read()
        if event == sg.WIN_CLOSED:
            if 'CLOSED' in self._actions:
                self._actions['CLOSED'](self._window, values)
            self._window.close()
            sys.exit(0)
        else:
            self._actions[event](self._window, values)
        return event != sg.WIN_CLOSED
