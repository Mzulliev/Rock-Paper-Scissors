import random

import PySimpleGUI as sg
import cv2 as cv
import torch


def main():
    # creating a GUI layout
    sg.theme('Black')

    user_column = [
        [sg.Text('You: 0', justification='left', size=(40, 1), font='Helvetica 16', key='user_score')],
        [sg.Image(filename='', key='user_image')]
    ]
    computer_column = [
        [sg.Text('Computer: 0', justification='left', size=(40, 1), font='Helvetica 16', key='computer_score')],
        [sg.Text('', justification='left', key='computer_text', font='Helvetica 16')],
        [
            sg.Text('', justification='left', key='result_user', font='Helvetica 16'),
            sg.Image(filename='', key='result_img_user')
        ],
        [
            sg.Text('', justification='left', key='result_computer', font='Helvetica 16'),
            sg.Image(filename='', key='result_img_computer')
        ]
    ]

    layout = [
        [sg.Text('ROCK PAPER SCISSORS', size=(40, 1), justification='center', font='Helvetica 20')],
        [sg.Column(user_column)],
        [sg.VSeparator()],
        [sg.Column(computer_column)],
        [sg.Button('PLAY', size=(10, 1), font='Helvetica 14'),
         sg.Button('STOP', size=(10, 1), font='Helvetica 14'),
         sg.Button('RESET SCORE', size=(20, 1), font='Helvetica 14')]
    ]

    # create the window and show it without the plot
    window = sg.Window('Game - "Rock Paper Scissors"',
                       layout)

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv.VideoCapture(0)
    play = False
    user_score = 0
    computer_score = 0
    while True:

        event, values = window.read(timeout=20)

        ret, frame = cap.read()

        # resizing the displayed image
        scale_percent = 50
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame = cv.resize(frame, dsize)

        # displaying an image on the screen
        imgbytes = cv.imencode('.png', frame)[1].tobytes()
        window['user_image'].update(data=imgbytes)

        # interface algorithm
        if event == sg.WIN_CLOSED or event == 'STOP':
            break

        elif event == 'PLAY':
            play = True
            if play:
                ret, frame = cap.read()
                cv.imwrite('camera.jpg', frame)

                model = torch.hub.load('D:\ProjectPortfolio\yolov5', 'custom',
                                       path="D:\ProjectPortfolio\yolov5\\runs\\train\exp\weights\\best.pt",
                                       source='local')
                img = 'D:\ProjectPortfolio\camera.jpg'
                results = model(img)
                result = str(results).strip().split()[4]

                list_data = ['rock', 'paper', 'scissors']
                random_index = random.randint(0, len(list_data) - 1)
                result_computer = list_data[random_index]

                if result in list_data:

                    if result == result_computer:
                        window['computer_text'].update('Draw!')
                    elif (result == "rock" and result_computer == "paper") \
                            or (result == "paper" and result_computer == "scissors"):
                        window['computer_text'].update('Computer win!!!')
                        computer_score += 1
                        window['computer_score'].update(f'Computer: {computer_score}')
                    else:
                        window['computer_text'].update("You win!!! Congratulations!!!")
                        user_score += 1
                        window['user_score'].update(f'You: {user_score}')

                    window['result_user'].update(f'You: {result}')
                    window['result_img_user'].update(f'D:\ProjectPortfolio\{result}.png')
                    window['result_computer'].update(f'Computer: {result_computer}')
                    window['result_img_computer'].update(f'D:\ProjectPortfolio\{result_computer}.png')
                else:
                    window['computer_text'].update('TRY AGAIN.')
                    window['result_user'].update('')
                    window['result_img_user'].update('')
                    window['result_computer'].update('')
                    window['result_img_computer'].update('')

                play = False

        elif event == 'RESET SCORE':
            window['computer_text'].update('')
            window['user_score'].update('You: 0')
            window['computer_score'].update('Computer: 0')
            window['result_user'].update('')
            window['result_img_user'].update('')
            window['result_computer'].update('')
            window['result_img_computer'].update('')

    window.close()


main()
