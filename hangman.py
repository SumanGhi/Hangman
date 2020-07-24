# hangman game
# best of luck!

import pygame
import random

# window initialisation
pygame.init()
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth, winHeight))

# initialise global variables
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
light_blue = (102, 255, 255)
buttons = []
guessed = []
limbs = 0
word = ''
btn_font = pygame.font.SysFont("arial", 20)
lost_font = pygame.font.SysFont("arial", 45)
guessed_font = pygame.font.SysFont("monospace", 24)
hangmanPics = [pygame.image.load('hangman0.png'),
               pygame.image.load('hangman1.png'),
               pygame.image.load('hangman2.png'),
               pygame.image.load('hangman3.png'),
               pygame.image.load('hangman4.png'),
               pygame.image.load('hangman5.png'),
               pygame.image.load('hangman6.png')]

input_box = pygame.Rect(250, 350, 140, 32)
hint_box = pygame.Rect(250, 400, 140, 32)
hints_box = pygame.Rect(490, 175, 140, 32)
hactive = False
text = ''
cur = ''
ast = ''
hint = ''
player1 = False
player2 = False
visible = True
go = False
p1 = btn_font.render('Single player', 1, red)
p2 = btn_font.render('Two players', 1, red)
icur = ''
hcur = ''


def cursor():
    global text
    global icur, hcur
    if active:
        if '|' not in icur:
            icur = ast + '|'
            pygame.time.delay(150)
        else:
            if icur[-1:] == '|':
                icur = icur[:-1]
                pygame.time.delay(150)
    else:
        if icur[-1:] == '|':
            icur = icur[:-1]
    if hactive:
        if '|' not in hcur:
            hcur = hint + '|'
            pygame.time.delay(150)
        else:
            if hcur[-1:] == '|':
                hcur = hcur[:-1]
                pygame.time.delay(150)

    else:
        if hcur[-1:] == '|':
            hcur = hcur[:-1]


def textHit(x, y):
    global player1, player2
    global visible
    if 200 < x < 200+p1.get_width():
        player1 = True
        visible = False
    elif 400 < x < 400+p1.get_width():
        player2 = True
        visible = False


def entry():
    win.fill(black)
    # title and logo
    entry_text = lost_font.render('!.!.Hangman.!.!', 1, light_blue)
    win.blit(entry_text, (winWidth/2 - entry_text.get_width()/2, 50))
    win.blit(hangmanPics[6], (winWidth/2 - hangmanPics[6].get_width()/2, 100))

    # blit 1player and 2player
    if visible:
        win.blit(p1, (200, 350))
        win.blit(p2, (400, 350))
    # select player
    if player1 and not player2:
        return randomWord()

    if player2:
        # guessing word
        cursor()
        pygame.draw.rect(win, light_blue, input_box)
        astrik = btn_font.render(icur, True, black)
        # Resize the box if the text is too long.
        width = max(200, astrik.get_width() + 10)
        input_box.w = width
        # Blit the text.
        win.blit(astrik, (input_box.x + 5, input_box.y + 5))

        # hint word
        pygame.draw.rect(win, light_blue, hint_box)
        hwidth = max(200, astrik.get_width() + 10)
        hint_box.w = hwidth
        hints = btn_font.render(hcur, True, black)
        win.blit(hints, (hint_box.x + 5, hint_box.y + 5))

        if not active and text == '':
            alt = btn_font.render('Enter guessing phrase', True, black)
            win.blit(alt, (input_box.x + 5, input_box.y + 5))

        if not hactive and hint == '':
            alt = btn_font.render('Enter one word hint', True, black)
            win.blit(alt, (hint_box.x + 5, hint_box.y + 5))

        pygame.draw.circle(win, light_blue, (500,380), 20)
        start = btn_font.render('Go', 1, red)
        win.blit(start, (490, 370))
        win.blit(start, (489, 369))
    name = btn_font.render('@Suman Ghimire', 1, blue)
    win.blit(name, (550, 440))
    pygame.display.update()
    return ''


def starthit(x, y):
    global word
    if 480 < x < 520 and 360 < y < 400 :
        word = text


# draw on window
def redraw_game_window():
    win.fill(red)
    spaced = spacedOut(word, guessed)
    # button
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, black, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3]-2)
            label = btn_font.render(chr(buttons[i][5]), 1, black)
            win.blit(label, (buttons[i][1] - (label.get_width()/2), (buttons[i][2] - (label.get_height()/2))))
    label1 = guessed_font.render(spaced, 1, black)
    length = label1.get_width()
    win.blit(label1, (winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))

    pygame.draw.rect(win, light_blue, hints_box)
    hint_item = 'Hint:  ' + hint.capitalize()
    hints = btn_font.render(hint_item, 1, black)
    width = max(140, hints.get_width() + 20)
    hints_box.w = width
    win.blit(hints, (500, 180))

    name = btn_font.render('@Suman Ghimire', 1, blue)
    win.blit(name, (550, 440))
    pygame.display.update()


# space for unguessed word and letter for guessed
def spacedOut(word, guessed):
    spacedWord = ''
    guessedLetters = guessed
    first = word[0]
    for x in range(len(word)):
        if word[x] == first:
            spacedWord += first.upper() + ' '
        elif word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += '  '
    buttons[ord(first) - 97][4] = False
    return spacedWord


# randomly select word from file
def randomWord():
    global hint
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f)-1)
    t = f[i][:-1].split(",")
    hint = t[1]
    return t[0]


# detect clicked alphabet
def buttonHit(x, y):
    for i in range(len(buttons)):
        if buttons[i][1] + 20 > x > buttons[i][1] - 20:
            if buttons[i][2] + 20 > y > buttons[i][2] - 20:
                if not buttons[i][4]:
                    return None
                return buttons[i][5]
    return None


# check whether to hang or not
def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


# what to do after game over
def end(winner=False):
    global limbs
    losttext = 'You are dead. Try again!!'
    wintext = 'Was that easy?....'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(green)

    if winner:
        label = lost_font.render(wintext, 1, blue)
    else:
        label = lost_font.render(losttext, 1, red)

    wordtext = lost_font.render(word.upper(), 1, black)
    wordwas = lost_font.render('The Phrase was: ', 1, black)

    win.blit(wordtext, (winWidth/2 - wordtext.get_width()/2, 295))
    win.blit(wordwas, (winWidth/2 - wordwas.get_width()/2, 245))
    win.blit(label, (winWidth/2 - label.get_width()/2, 140))
    name = btn_font.render('@Suman Ghimire', 1, blue)
    win.blit(name, (550, 440))
    pygame.display.update()
    again = True

    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


# reset every variable to initial point to restart program
def reset():
    global limbs
    global word
    global guessed
    global buttons
    global icur, hcur
    global text, hint
    global ast
    global player1, player2
    global visible, active, hactive
    for i in range(len(buttons)):
        buttons[i][4] = True
    limbs = 0
    guessed = []
    icur = ''
    hcur = ''
    text = ''
    ast = ''
    hint = ''
    word = ''  # use randomWord to generate randomly
    player1 = False
    player2 = False
    active = False
    hactive = False
    visible = True


# setup buttons.. a,b,c..... z
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        y = 85
        x = 25 + (increase * (i-13))
    buttons.append([light_blue, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

# main section where play is made and event handled
inPlay = True
active = False
while inPlay:
    if word == '':
        word = entry()  # word = randomWord()  # use randomWord to generate word randomly and entry as per your wish
    else:
        redraw_game_window()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    ast = ast[:-1]
                else:
                    a = event.unicode
                    for i in range(36):
                        if chr(i+92) is a:
                            ast += '*'
                    if chr(32) is a:
                        ast += '*'
                    text += a
            if hactive:   # capture hint
                if event.key == pygame.K_BACKSPACE:
                    hint = hint[:-1]
                else:
                    a = event.unicode
                    hint += a
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            textHit(clickPos[0], clickPos[1])
            starthit(clickPos[0], clickPos[1])
            if letter is not None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = True
            else:
                active = False
            if hint_box.collidepoint(event.pos):
                hactive = True
            else:
                hactive = False

pygame.quit()
# quit game when done
