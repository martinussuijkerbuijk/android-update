import PySimpleGUI as sg
import serial
import struct
from threading import Thread

# Arduino motor
ser_android = serial.Serial('COM3', 19200, timeout=1)


def main():
    global line_L

    # Start script to check if visitor is present
    # T1 = Thread(target=check_visitor)
    # T1.start()


    layout = [[sg.Text('STOP ALL SCRIPTS FIRST, BEFORE CLOSING WINDOW!')],
              [sg.Text('', size=(15, 1), key='-OUTPUT-')],
              [sg.Multiline(size=(60, 10), key='-ML-', autoscroll=True)],
              [sg.Text('Left-Right', size=(15, 1), key='Left-Right'), sg.Slider(orientation='horizontal', key='HSlider', range=(70, 110), default_value=90
                                                                                , enable_events = True),
               sg.Text('Up-Down', size=(15, 1), key='Up-Down'), sg.Slider(orientation='vertical', key='VSlider', range=(70, 110), default_value=90, enable_events = True)],
              [sg.Text('Face Tracker', size=(10, 1)), sg.Button('StartF'), sg.Button('StopF'), sg.Text('Start/Stop facetracker Script!', size=(30, 1))],
              [sg.Text('I2Text', size=(10, 1)), sg.Button('StartI'), sg.Button('StartI'), sg.Text('Start/Stop Image2Text Script!', size=(30, 1))],
              [sg.Button('Exit')], ]

    window = sg.Window('Android | GUI', layout, finalize=True)
    sg.cprint_set_output_destination(window, '-ML-')

    sg.cprint("Script Started! calibrate eyes with sliders.")

    while True:
        event, values = window.read(timeout=100)
        if event == 'HSlider':
            valH = int(values['HSlider'])
            sg.cprint("hslider", valH, c=('black', 'red'))
            ser_android.write(f"{str(valH)}x".encode())
        if event == 'VSlider':
            valV = int(values['VSlider'])
            sg.cprint("vslider", valV, c=('black', 'blue'))
            ser_android.write(f"{str(valV)}y".encode())


        if event in (sg.WIN_CLOSED, 'Exit'):
            break
    window.close()


if __name__ == "__main__":
    main()