import PySimpleGUI as sg

class WindowManager:

    @staticmethod
    def getMainWindow():
        layout = [[sg.Text('Enter music url:')],
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
    def updateProgressWindow(label: str, i: int, max: int, window):
        window['-PERCENT-'].update(value=label+' (' + str(int(i / max * 100)) + '%)')
        window['-PROGRESS-'].update(current_count=i, max=max)

class WindowHandler:

    def __init__(self, window):
        self._window = window
        self._actions = {}

    def addAction(self, event: str, action):
        self._actions[event] = action

    def handle(self) -> bool:
        event, values = self._window.read()
        if event == sg.WIN_CLOSED:
            self._window.close()
        else:
            self._actions[event](self._window)
        return event != sg.WIN_CLOSED
