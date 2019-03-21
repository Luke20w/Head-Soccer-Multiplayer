import pygame
from network import Network
from player import Player
from ball import Ball

# Initialization
screenwidth = 900
screenheight = 630
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Client")
pygame.init()

# Classes
ball = Ball(screenwidth / 2, screenwidth, screenheight)

# Fonts
chatFont = pygame.font.SysFont('', 18)


def update(screen, player, player2):
    # Background
    background = pygame.image.load('background.png')
    background = pygame.transform.scale(background, (screenwidth, screenheight))
    screen.blit(background, (0, 0))

    # Players
    player.draw(screen)
    player2.draw(screen)

    update_ball(screen, player, player2)

    chat(screen, player, player2)

    pygame.display.update()


def chat(screen, player, player2):
    # Background
    back = pygame.Surface((300, 200))
    back.set_alpha(100)
    back.fill((100, 100, 100))
    screen.blit(back, (8, 8))
    yloc = 190
    # Messages
    msgs = []
    for i in player.pastMsgs:
        msgs.append([i, 0])
    for i in player2.pastMsgs:
        msgs.append([i, 1])
    msgs.sort(key=lambda x: x[0][1])  # Arranges the chats by recent
    for i in range(len(msgs) - 1, -1, -1):
        val = msgs[i]
        if val[1] == 0:
            text = chatFont.render(val[0][0], True, (255, 255, 255))
        else:
            text = chatFont.render(val[0][0], True, (0, 255, 0))
        pos = text.get_rect()
        pos.topleft = (10, yloc)
        screen.blit(text, pos)
        yloc -= 20
    if player.chatActive:
        text = chatFont.render(player.msg, True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(8, 206, 300, 20))
        pos = text.get_rect()
        pos.topleft = (10, 208)
        screen.blit(text, pos)


def update_ball(screen, player, player2):
    ball.update()
    ball.collide_player(player.x, player.y, player.radius)
    ball.collide_player(player2.x, player.y, player2.radius)
    ball.draw(screen)


def main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            # X Button Quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Add to or remove from the chat string
            if p.chatActive:
                if event.type == pygame.KEYDOWN:
                    if event.key != 13:
                        if event.key == 8:  # Backspace
                            p.msg = p.msg[0:-1]
                        else:
                            p.msg = p.msg + chr(event.key)

        p.move()
        update(screen, p, p2)

main()