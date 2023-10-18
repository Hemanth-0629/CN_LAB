import time
import pygame
import random
import socket
import re
import threading
import pickle
import re
import uuid
import time

pygame.init()
# Create the screen

x = 0.8
y = 0.8
counter = 10
timeinterval = 0.05
screen = pygame.display.set_mode((900*x, 620*y))


player1set = ''
roomid = ''
amount_pay = 0


def player2set(client, SIZE, FORMAT):
    msg = client.recv(SIZE)
    msg = pickle.loads(msg)
    print(f"Msg:{msg}")
    return msg

# wait ui


def wait(client, FORMAT, SIZE):
    icon = pygame.image.load("paper.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Stone Paper Scissors")

    fonts3 = pygame.font.SysFont('Georgia', int(40*x), bold=True)
    message = fonts3.render("Wait...", True, 'white')

    # Button positions
    button_positions = {
        "Quit": (450*x, 500*y),
    }

    def gradientRects(screen, left_colour, right_colour, target_rect):
        gradient_surface = pygame.Surface(
            (target_rect.width, target_rect.height))
        left_color_stop = left_colour
        right_color_stop = right_colour
        for x in range(target_rect.width):
            factor = x / (target_rect.width - 1)
            r = int(left_color_stop[0] + factor *
                    (right_color_stop[0] - left_color_stop[0]))
            g = int(left_color_stop[1] + factor *
                    (right_color_stop[1] - left_color_stop[1]))
            b = int(left_color_stop[2] + factor *
                    (right_color_stop[2] - left_color_stop[2]))
            pygame.draw.line(gradient_surface, (r, g, b),
                             (x, 0), (x, target_rect.height))
        screen.blit(gradient_surface, target_rect)

    target_rects = pygame.Rect(0, 0, 900*x, 620*y)
    Start_button = pygame.Rect(370*x, 310*y, 125*x, 60*y)
    id = pygame.font.SysFont('Georgia', int(40*x), bold=True)

    running = True

    while running:
        gradientRects(screen, (150, 100, 40), (0, 100, 200), target_rects)
        screen.blit(message, (300, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if Start_button.collidepoint(event.pos):
                    running = False
        pygame.draw.rect(screen, (0, 0, 100),
                         Start_button, border_radius=3)
        quit = fonts3.render('Quit', True, 'white')
        screen.blit(quit, (308, 255))

        pygame.display.update()


# starting ui
def ui(client, FORMAT, SIZE):
    icon = pygame.image.load("paper.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Stone Paper Scissors")

    fonts3 = pygame.font.SysFont('Georgia', int(40*x), bold=True)
    message = fonts3.render("Enter the room id: ", True, 'white')
    message1 = fonts3.render("Enter the amount(min:100): ", True, 'white')
    start = fonts3.render('Start', True, 'white')

    # Button positions
    button_positions = {
        "Start": (450*x, 500*y),
    }

    def gradientRects(screen, left_colour, right_colour, target_rect):
        gradient_surface = pygame.Surface(
            (target_rect.width, target_rect.height))
        left_color_stop = left_colour
        right_color_stop = right_colour
        for x in range(target_rect.width):
            factor = x / (target_rect.width - 1)
            r = int(left_color_stop[0] + factor *
                    (right_color_stop[0] - left_color_stop[0]))
            g = int(left_color_stop[1] + factor *
                    (right_color_stop[1] - left_color_stop[1]))
            b = int(left_color_stop[2] + factor *
                    (right_color_stop[2] - left_color_stop[2]))
            pygame.draw.line(gradient_surface, (r, g, b),
                             (x, 0), (x, target_rect.height))
        screen.blit(gradient_surface, target_rect)

    target_rects = pygame.Rect(0, 0, 900*x, 620*y)
    Start_button = pygame.Rect(390*x, 430*y, 125*x, 60*y)
    id = pygame.font.SysFont('Georgia', int(40*x), bold=True)
    amounts = pygame.font.SysFont('Georgia', int(40*x), bold=True)

    # Load background image
    global roomid
    global amount_pay
    ids = ''
    amount = ''
    id_input_active = True
    running = True

    while running:
        gradientRects(screen, (150, 100, 40), (0, 100, 200), target_rects)
        screen.blit(message, (200, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if id_input_active:
                    if event.key == pygame.K_RETURN:  # User pressed Enter to switch to entering amount
                        id_input_active = False
                    else:
                        ids += event.unicode
                else:  # Entering amount
                    if event.key == pygame.K_RETURN:  # User pressed Enter to start
                        if int(amount) >= 100:
                            roomid = ids
                            running = False
                    else:
                        amount += event.unicode

            if event.type == pygame.MOUSEBUTTONUP:
                if Start_button.collidepoint(event.pos):
                    if amount and int(amount) >= 100:
                        amount_pay = amount
                        roomid = ids
                        running = False

        show_id = id.render(ids, True, (0, 0, 0))
        screen.blit(show_id, (350, 200))

        if id_input_active:
            if ids != '':
                screen.blit(message1, (150, 250))
        else:  # Entering amount
            screen.blit(message1, (150, 250))
            amount_paid = amounts.render(amount, True, (0, 0, 0))
            screen.blit(amount_paid, (320, 300))
            if amount and int(amount) >= 100:
                pygame.draw.rect(screen, (200, 200, 100),
                                 Start_button, border_radius=3)
                screen.blit(start, (320, 350))

        pygame.display.update()


# time over
def timeover(client, FORMAT, SIZE, mac):
    icon = pygame.image.load("paper.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Stone Paper Scissors")

    fonts3 = pygame.font.SysFont('Georgia', int(40*x), bold=True)
    message = fonts3.render("Time Over", True, 'white')
    message1 = fonts3.render("Thank You", True, 'white')
    finish = fonts3.render('Finish', True, 'white')

    # Button positions
    button_positions = {
        "Finish": (450*x, 500*y),
    }
    Finish_button = pygame.Rect(370*x, 430*y, 150*x, 60*y)

    def gradientRects(screen, left_colour, right_colour, target_rect):
        gradient_surface = pygame.Surface(
            (target_rect.width, target_rect.height))
        left_color_stop = left_colour
        right_color_stop = right_colour
        for x in range(target_rect.width):
            factor = x / (target_rect.width - 1)
            r = int(left_color_stop[0] + factor *
                    (right_color_stop[0] - left_color_stop[0]))
            g = int(left_color_stop[1] + factor *
                    (right_color_stop[1] - left_color_stop[1]))
            b = int(left_color_stop[2] + factor *
                    (right_color_stop[2] - left_color_stop[2]))
            pygame.draw.line(gradient_surface, (r, g, b),
                             (x, 0), (x, target_rect.height))
        screen.blit(gradient_surface, target_rect)

    target_rects = pygame.Rect(0, 0, 900*x, 620*y)

    running = True

    while running:
        gradientRects(screen, (150, 100, 40), (0, 100, 200), target_rects)

        screen.blit(message, (250, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if Finish_button.collidepoint(event.pos):
                    info = {
                        "Timeleft": counter,
                        "Mac": mac
                    }
                    Time_left = pickle.dumps(info)
                    client.send(Time_left)
                    bye = pickle.dumps("BYE")
                    client.send(bye)
                    running = False

        screen.blit(message1, (250, 200))
        pygame.draw.rect(screen, (200, 200, 100),
                         Finish_button, border_radius=3)
        screen.blit(finish, (300, 350))
        pygame.display.update()

    pygame.display.quit()


# actual game ui
def game(client, FORMAT, SIZE, mac, totaltime):
    # Title and Icon
    pygame.display.set_caption("Stone Paper Scissors")
    icon = pygame.image.load("paper.png")
    pygame.display.set_icon(icon)
    # Load background image
    background = pygame.image.load("bg.png")
    background = pygame.transform.scale(background, (900*x, 620*y))

    # player
    playerImg = pygame.image.load("hand1.png")
    playerImg1 = pygame.image.load("hand2.png")
    playerImg2 = pygame.image.load("hand3.png")
    # Image will came from left
    playerImg = pygame.transform.rotate(playerImg, 270)
    playerImg1 = pygame.transform.rotate(playerImg1, 270)
    playerImg2 = pygame.transform.rotate(playerImg2, 270)
    # Image will came from right
    playerImg3 = pygame.transform.rotate(playerImg, 180)
    playerImg4 = pygame.transform.rotate(playerImg1, 180)
    playerImg5 = pygame.transform.rotate(playerImg2, 180)

    # Two player
    # Left
    Left_move_X = 50*x
    Left_move_y = 200*y  # not changed

    # right
    Right_move_x = 750*x
    Right_move_y = 200*y  # not changed

    start = 0  # when two player
    start1 = 0  # when three player

    # leader board for 2 player

    def player_score2(score1, score2):
        pygame.draw.rect(screen, (250, 150, 150), (650*x, 60*y, 220*x, 40*y))
        player1_score_text = fonts2.render(
            f"Player1 Score: {score1}", True, 'white')
        screen.blit(player1_score_text, (665*x, 65*y))
        pygame.draw.rect(screen, (250, 150, 150), (650*x, 100*y, 220*x, 40*y))
        player2_score_text = fonts2.render(
            f"Player2 Score: {score2}", True, 'white')
        screen.blit(player2_score_text, (665*x, 105*y))

    # It is among two player decider

    def decider(user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif user_choice == "Rock":
            return "You win!" if computer_choice == "Scissors" else "Player2 win!"
        elif user_choice == "Paper":
            return "You win!" if computer_choice == "Rock" else "Player2 win!"
        elif user_choice == "Scissors":
            return "You win!" if computer_choice == "Paper" else "Player2 win!"

    fonts = pygame.font.SysFont('Georgia', int(40*x), bold=True)
    fonts1 = pygame.font.SysFont('Georgia', int(40*x), bold=True)
    fonts2 = pygame.font.SysFont('Georgia', int(20*x))

    message = fonts2.render("Number of player:2", True, 'white')
    surf = fonts.render('Quit', True, 'white')
    surf1 = fonts1.render('Start', True, 'white')
    back = fonts2.render("Back", True, 'white')
    times = fonts2.render("TimeLeft:", True, 'white')

    # Button positions
    button_positions = {
        "Paper": (200*x, 500*y),
        "Scissors": (400*x, 500*y),
        "Rock": (600*x, 500*y),
    }

    button = pygame.Rect(600*x, 550*y, 105*x, 60*y)
    Start_button = pygame.Rect(200*x, 550*y, 115*x, 60*y)
    button5 = pygame.Rect(370*x, 100*y, 150*x, 40*y)
    back_button = pygame.Rect(820*x, 5*y, 60*x, 25*y)

    animation_speed = 0.3
    animation_speed1 = -0.3

    Player1_Score = 0
    Player2_Score = 0

    count_player = pygame.font.SysFont('Georgia', int(20*x), bold=True)
    time_counter = pygame.font.SysFont('Georgia', int(20*x), bold=True)

    player_count = ''
    on = 0
    option = 1

    # Result show after match

    def show_winner(winner):
        result = fonts2.render("Result: ", True, "white")
        screen.blit(result, (200*x, 50*y))
        result_text = fonts2.render(winner, True, "white")
        screen.blit(result_text, (300*x, 50*y))

    # Rock paper scissor button

    def buttonlaga(a, b):
        for choice, position in button_positions.items():
            if position[0] <= a <= position[0]+110 and position[1] <= b <= position[1]+60:
                pygame.draw.rect(screen, (0, 0, 100),
                                 (position[0]+5, position[1], 100*x, 45*y), border_radius=3)
                button_text = fonts2.render(choice, True, "white")
                screen.blit(button_text, (position[0] + 26, position[1] + 11))
            else:
                pygame.draw.rect(screen, (0, 100, 100),
                                 (position[0]+5, position[1], 100*x, 40*y), border_radius=3)
                button_text = fonts2.render(choice, True, "white")
                screen.blit(button_text, (position[0] + 25, position[1] + 10))

    def player(playerImg, posX, posY):
        screen.blit(playerImg, (posX, posY))

    # Choices
    choices = ["Rock", "Paper", "Scissors"]
    player1_choice = None
    player2_choice = None
    target_rect = pygame.Rect(0, 0, 900*x, 620*y)

    score_displayed = False
    global timeinterval
    global counter
    counter = 60*totaltime

    options = []
    # Game Loop
    running = True

    while running:
        # set background picture
        screen.blit(background, (0, 0))
        screen.blit(message, (0, 0))
        if option == 1:
            pass
        if option == 0:
            if back_button.x <= a <= back_button.x + 110 and back_button.y <= b <= back_button.y + 60:
                pygame.draw.rect(screen, (200, 100, 0),
                                 back_button, border_radius=3)
                screen.blit(back, (back_button.x+8, back_button.y+1))
            else:
                pygame.draw.rect(screen, (0, 0, 0),
                                 back_button, border_radius=3)
                screen.blit(back, (back_button.x+7, back_button.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                player_count = 0
                player_count = event.unicode
                on = 1

            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.collidepoint(event.pos):
                    player_count = 0
                    option = 1  # showing option How many player will play
                    on = 0  # off

            if event.type == pygame.MOUSEBUTTONUP:
                if button.collidepoint(event.pos):
                    info = {
                        "Timeleft": counter,
                        "Mac": mac
                    }
                    Time_left = pickle.dumps(info)
                    client.send(Time_left)
                    bye = pickle.dumps("BYE")
                    client.send(bye)
                    running = False
                if Start_button.collidepoint(event.pos):
                    start = 1
                    start1 = 0
                    animation_speed = 1
                    animation_speed1 = -1
                    Left_move_X = 50*x
                    Right_move_x = 750*x
                    player1_choice = None
                    player2_choice = None

                if start:  # Check if the "Start" button is clicked
                    if player1_choice is None:
                        for choice, position in button_positions.items():
                            if event.type == pygame.MOUSEBUTTONDOWN+1 and position[0] <= event.pos[0] <= position[0] + 100 and position[1] <= event.pos[1] <= position[1] + 50:
                                player1_choice = choice
                                player1set = player1_choice
                                info = pickle.dumps(player1set)
                                client.send(info)
                                # client.send(player1set.encode(FORMAT))

                    elif player2_choice is None:
                        player2_choice = player2set(client, SIZE, FORMAT)

        if on == 1 or on == 0:
            a, b = pygame.mouse.get_pos()
            option = 0

            if button.x <= a <= button.x + 110 and button.y <= b <= button.y + 60:
                pygame.draw.rect(screen, (200, 50, 0), button, border_radius=3)
                screen.blit(surf, (button.x + 7.5, button.y + 7.5))
            else:
                pygame.draw.rect(screen, (0, 0, 0), button, border_radius=3)
                screen.blit(surf, (button.x + 5, button.y + 5))

            if Start_button.x <= a <= Start_button.x + 110 and Start_button.y <= b <= Start_button.y + 60:
                pygame.draw.rect(screen, (100, 200, 50),
                                 Start_button, border_radius=3)
                screen.blit(surf1, (Start_button.x +
                            7.5, Start_button.y + 7.5))
            else:
                pygame.draw.rect(screen, (0, 0, 0),
                                 Start_button, border_radius=3)
                screen.blit(surf1, (Start_button.x + 5, Start_button.y + 5))

            if start:
                if player1_choice == None:
                    buttonlaga(a, b)

                if player1_choice is None:
                    prompt = fonts2.render(
                        "Player 1: Choose your move", True, "white")
                    screen.blit(prompt, (50*x, 50*y))
                    player_score2(Player1_Score, Player2_Score)
                    score_displayed = True
                elif player2_choice is None:
                    pass
                else:
                    if (player2_choice != None):
                        if player1_choice == "Paper":
                            Left_move_X += animation_speed
                            if Left_move_X >= 250*x:
                                animation_speed = 0
                            player(playerImg, Left_move_X, 200*y)

                        elif player1_choice == "Scissors":
                            Left_move_X += animation_speed
                            if Left_move_X >= 250*x:
                                animation_speed = 0
                            player(playerImg1, Left_move_X, 200*y)

                        elif player1_choice == "Rock":
                            Left_move_X += animation_speed
                            if Left_move_X >= 250*x:
                                animation_speed = 0
                            player(playerImg2, Left_move_X, 200*y)

                        if player2_choice == "Paper":
                            Right_move_x += animation_speed1
                            if Right_move_x <= 550*x:
                                animation_speed1 = 0
                            player(playerImg3, Right_move_x, 200*y)

                        elif player2_choice == "Scissors":
                            Right_move_x += animation_speed1
                            if Right_move_x <= 550*x:
                                animation_speed1 = 0
                            player(playerImg4, Right_move_x, 200*y)

                        elif player2_choice == "Rock":
                            Right_move_x += animation_speed1
                            if Right_move_x <= 550*x:
                                animation_speed1 = 0
                            player(playerImg5, Right_move_x, 200*y)

                        winner = decider(player1_choice, player2_choice)
                        if winner == "You win!" and score_displayed:
                            Player1_Score += 1
                            score_displayed = False
                        elif winner == "Player2 win!" and score_displayed:
                            Player2_Score += 1
                            score_displayed = False
                        show_winner(winner)
                    player_score2(Player1_Score, Player2_Score)

        screen.blit(times, (400, 0))

        counter = counter - timeinterval
        time.sleep(timeinterval)
        minutes, seconds = divmod(int(counter), 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        time_left = time_counter.render(f"{time_str}", True, (255, 255, 255))
        screen.blit(time_left, (475, 0))
        if (counter <= 0):
            timeover(client, FORMAT, SIZE, mac)
            break
        pygame.display.update()


def main():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 8000
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = "utf-8"
    DISCONNECT_MSG = "BYE"

    client = socket.socket()
    client.connect(ADDR)
    print(f"[Connected] Client connected to server at {IP}:{PORT}")
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    macdata = pickle.dumps(mac)
    client.send(macdata)
    lefttime = client.recv(SIZE)
    lefttime = pickle.loads(lefttime)
    print(lefttime)
    if lefttime <= 0:
        if lefttime != -1:
            ui(client, FORMAT, SIZE)
            info = {
                "id": roomid,
                "amount": amount_pay,
                "mac": mac
            }
            info = pickle.dumps(info)
            client.send(info)
            msg = client.recv(SIZE)
            msg = pickle.loads(msg)
            print(f"Msg:{msg}")
        elif lefttime == -1:
            msg = client.recv(SIZE)
            msg = pickle.loads(msg)
            print(msg)
            if msg["flag"] == 1:
                wait(client, FORMAT, SIZE)
        if msg["time"] <= 0:
            timeover(client, FORMAT, SIZE, mac)
        else:
            game(client, FORMAT, SIZE, mac, msg["time"])
    else:
        macData = pickle.dumps(mac)
        client.send(macData)
        game(client, FORMAT, SIZE, mac, (lefttime)/60)


if __name__ == '__main__':
    main()


# problem is I have to fix three player and make room
