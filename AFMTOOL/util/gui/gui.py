import PySimpleGUI as sg
import os

def launch_gui():
    vert_line = False
    # The base64 strings for the button images
    toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
    toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'

    main_layout = [
            [sg.Text('Select your files', font='bold')],
            [sg.Text('Files selected:'), sg.Input(readonly = True, key = '-FILES-'), sg.FilesBrowse()],
            [sg.Submit(key='-SUBMIT-'), sg.Button('Notes')]
    ]
    options_general_layout = [
        [sg.Text('No. of circles to detect: '),
        sg.Input(key='-NumCircles-', size = 6),
        sg.Push(),
        sg.Text('Index of circles to exclude: '),sg.Input(key='-EXCLUDE-', size = 10), sg.Push()
        ],
        [sg.Text('Min radius (μm):'), sg.Input(key='-MINR-', size = 6), sg.Push(), 
         sg.Text('Max radius (μm):'), sg.Input(key='-MAXR-', size = 6), sg.Push(),
         sg.Text('Pitch (μm):'), sg.Input(key='-PITCH-', size = 6), sg.Push(),
         ],
    ]
    
    options_roughness_layout = [
        [sg.Text('Contacts window side length: (μm):'), sg.Input(key='-CWINSIZE-', size = 6), sg.Push(), sg.Text('Polymer window side length (μm):'), sg.Input(key='-POLWINSIZE-', size = 6), sg.Push()],
    ]
    
    options_line_layout = [
        [sg.Text('Vertical line profile:'),
        sg.Button(image_data=toggle_btn_off, key='-VERTLINE-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, metadata=False),
        sg.Push(),sg.Text('Copper window width (% of radius):'), sg.Input(key='-SHCOPPER-', size = 6)],
    ]
    
    options_layout = [
        
        [sg.TabGroup([[  sg.Tab('General', options_general_layout),
                               sg.Tab('Roughness', options_roughness_layout),
                               sg.Tab('Line profile', options_line_layout),
                ]], key='-TAB GROUP OPTIONS-'),
               ],
        
        [sg.Button('Help')],
        
    ]
    
    
    layout = [
            [sg.Push(), sg.Text('AFM Data Analysis Tool', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True), sg.Push()],
            [sg.TabGroup([[  sg.Tab('Main', main_layout),
                               sg.Tab('Optional inputs', options_layout),]], key='-TAB GROUP-', expand_x=True, expand_y=True),
               ]
            ]

    window = sg.Window('AFM Tool', layout,resizable=True)
    
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            filename_list= None
            break
        elif event == '-SUBMIT-':
            break
        elif event == 'Help':
            sg.popup(
                    "No. of circles to detect: ",
                     "Choose how many Cu pads to detect for roughness and step height calculations. By default, only the best 3 circles detected will be used.", 
                     "Pitch: ",
                     "Define the minimum distance between center of contacts",
                     "Min and Max radius: ",
                     "Define the smallest and largest radius of the circular contacts in the files uploaded, respectively.",
                     "Index of circles to exclude: ",
                     "In the reference image generated in the Excel report, the green boxes inside the circles detected are numbered. If certain circles are not detected correctly, one can exclude them by specifying them in the input box with the indexes separated by commas and no spaces. For instance, if the 1st and 3rd circles are to be excluded, type in '1,3'.",
                     "Contacts/Polymer window size:",
                     "Define the side lengths of the squares within which the roughness of the contacts and polymers respectively are calculated. Default side lengths for square used for copper contacts is 1μm and that for polymer contacts is 2μm. The square on the copper contact will always be centered on the center of the circle detected, and the center of the square of the corresponding polymer will be one diameter to the right and one diameter upwards, unless all such squares are out of bound, in which case the polymer squares will be one diameter down and to the left of the copper squares.",
                     "Vertical line profile:",
                     "Calculate line profile, step height, and roll off along vertical lines.",
                     "Copper window width (% of radius):",
                     "Define the width of the window used to calculate the average height of copper contacts (blue rectangle in reference image), as a percentage of the radius of the circular contacts.",
                     keep_on_top=True, title= 'Help')
        elif event == 'Notes':
            sg.popup(
                "Please note the program assumes a minimum and maximum radius of 1μm and 2.5μm respectively, and a minimum pitch of 5μm.",
                "If your parameters are out of this range please enter them in the Optional Inputs tab."
                ,title='Notes',
            )
        elif event == '-VERTLINE-':  # if the graphical button that changes images
            window['-VERTLINE-'].metadata = not window['-VERTLINE-'].metadata
            window['-VERTLINE-'].update(image_data=toggle_btn_on if window['-VERTLINE-'].metadata else toggle_btn_off)
            vert_line = vert_line==False
    
    
    window.close()
    #Programme will error if the window is closed, since values[0]=None
    filename_list = values['-FILES-'].split(';')
    
    #Convert to floats for output, default output None to match that of legacy codes using Tkinter
    pitch = None if values['-PITCH-']=='' else float(values['-PITCH-'])
    minr = None if values['-MINR-']=='' else float(values['-MINR-'])
    num_circles = None if values['-NumCircles-']=='' else int(values['-NumCircles-'])
    maxr = None if values['-MAXR-']=='' else float(values['-MAXR-'])
    exclude = None if values['-EXCLUDE-']=='' else values['-EXCLUDE-']
    cwinsize = 1 if values['-CWINSIZE-']=='' else float(values['-CWINSIZE-'])
    polwinsize = 2 if values['-POLWINSIZE-']=='' else float(values['-POLWINSIZE-'])
    shcopper = 0.8 if values['-SHCOPPER-']=='' else float(values['-SHCOPPER-'])/100
        
    return filename_list, num_circles,pitch, minr, maxr, exclude, cwinsize, polwinsize, vert_line, shcopper

#launch_gui()



def done_gui(excel_file_path, done=True):
    title = 'Completed!' if done else 'Cancelled'
    msg = 'Processing completed successfully, Excel file has been generated.' if done else 'Process cancelled, Excel file has been generated for some data.'
    layout = [
        [sg.Text(msg)],
        [sg.Button('Open Excel file'), sg.Button('Open file location'),sg.Push(), sg.Button('Close')]
    ]
    
    window = sg.Window(title, layout)
    
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Close':
            break
        elif event == 'Open Excel file':
            os.system("start EXCEL.EXE "+excel_file_path)
        elif event == 'Open file location':
            os.startfile(os.path.abspath(os.path.join(os.getcwd(), os.pardir, "results/", "xlSheets/")) )
        
    window.close()
    
    
        
