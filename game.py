import pygame
import os
import random
from PIL import Image
import time

# Fonction pour effacer la console après chaque exécution
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


score = 0
best_score = 0
with open("score.txt", "r") as fichier:
    best_score = fichier.read()
    if best_score == "":
        best_score = 0
    else:
        best_score = int(best_score)


def diviser_gif_en_images(gif, hero):
    list_image = []
    gif = Image.open(gif)
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        list_image.append(pygame.transform.scale(pygame_image, (hero.width, hero.height)))
    return list_image


# Déclarer les variables pour des textes de couleurs
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
dark_blue = "\033[94m"
rose = "\033[95m"
light_blue = "\033[96m"
reset = "\033[0m"


def draw_score(score, best_score):
    i = 0
    if score > best_score:
        best_score = score
        i = 1
    font = pygame.font.Font('Ressources/PressStart2P-Regular.ttf', 16)
    text = font.render(f'Score: {score}', True, (255, 255, 0))
    if i == 1:
        text_best = font.render(f'NEW Best score: {best_score}', True, (255, 255, 0))
        fenetre.blit(text_best, (350, 30))
    elif i == 0:
        text_best = font.render(f'Best score: {best_score}', True, (255, 255, 0))
        fenetre.blit(text_best, (400, 30))
    fenetre.blit(text, (400, 10))


def draw_time(time_left):
    font = pygame.font.Font('Ressources/PressStart2P-Regular.ttf', 10)
    text = font.render(f'Time: {int(time_left)}', True, (255, 255, 255))
    fenetre.blit(text, (400, 60))


class Personnage:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y

        self.height = 100
        self.width = 100
        self.jump_state = False
        self.jump_count = 10
        self.static = diviser_gif_en_images('Ressources/hero.gif', self)
        self.right = diviser_gif_en_images('Ressources/Run.gif', self)
        self.left = [pygame.transform.flip(frame, True, False) for frame in self.right]

        self.attack = diviser_gif_en_images('Ressources/attack.gif', self)

        self.image = self.static
        self.image_index = 0

    def update_image(self):
        self.image_index = (self.image_index + 1) % len(self.image)
        self.current_image = self.image[self.image_index]


class Pièce:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.size = 15
        self.color = (255, 178, 102)

        self.index = 0


hero = Personnage(0, 228)

start_time = time.time()
time_limit = 60
elapsed_time_before_pause = 0


def random1():
    return random.randint(25, 550)


def random2():
    return random.randint(200, 250)


def generer_pieces(nombre_pieces):
    return [Pièce(random1(), random2()) for _ in range(nombre_pieces)]


nombre_pieces = 4
pièce = generer_pieces(nombre_pieces)


def draw(hero, score, time_left, best_score):
    fenetre.blit(image, (0, 0))
    fenetre.blit(hero.current_image, (hero.x, hero.y))
    for p in pièce:
        pygame.draw.circle(fenetre, p.color, (p.x, p.y), p.size)
    draw_score(score, best_score)
    draw_time(time_left)
    pygame.display.update()


def draw_start_menu():
    fenetre.blit(image, (0, 0))
    font = pygame.font.Font('Ressources/PressStart2P-Regular.ttf', 16)
    font_title = pygame.font.Font('Ressources/PressStart2P-Regular.ttf', 30)
    title_text = font_title.render('HERO GAME', True, (255, 255, 0))

    play_button = pygame.Rect(220, 150, 180, 50)
    quit_button = pygame.Rect(220, 290, 180, 50)
    reset_best_button = pygame.Rect(220, 220, 180, 50)

    pygame.draw.rect(fenetre, (100, 100, 100), play_button)
    pygame.draw.rect(fenetre, (100, 100, 100), quit_button)
    pygame.draw.rect(fenetre, (100, 100, 100), reset_best_button)

    play_text = font.render('Play', True, (255, 255, 255))
    quit_text = font.render('Quit', True, (255, 255, 255))
    reset_best_text = font.render('Reset Max', True, (255, 255, 255))

    fenetre.blit(title_text, (185, 100))
    fenetre.blit(play_text, (play_button.x + 50, play_button.y + 10))
    fenetre.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))
    fenetre.blit(reset_best_text, (reset_best_button.x + 10, reset_best_button.y + 10))
    pygame.display.update()

    return play_button, quit_button, reset_best_button


pygame.init()

pygame.display.set_caption("Hero Game", "Game")
logo = pygame.image.load('./Ressources/hero.gif')
pygame.display.set_icon(logo)

fenetre = pygame.display.set_mode((620, 360))
image = pygame.image.load('../Projet Jeu Vidéo/Ressources/bg.png')

clear_console()
print(f"Best score : {best_score}")

Running = True
game_state = "start_menu"  # "start_menu", "running"


while Running:
    if game_state == "start_menu":
        play_button, quit_button, reset_best_button = draw_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    score = 0
                    start_time = time.time()
                    game_state = "running"
                elif quit_button.collidepoint(mouse_pos):
                    Running = False
                elif reset_best_button.collidepoint(mouse_pos):
                    best_score = 0
                    with open("score.txt", "w") as fichier:
                        fichier.write(str(best_score))
                    print("Best score reset to 0.")
    elif game_state == "running":
        current_time = time.time()
        time_left = time_limit - (current_time - start_time)
        if time_left <= 0:
            game_state = "start_menu"
            print(f"{red}Time's up!{reset}")
            print(f"{yellow}Final score : {score}{reset}")
            if score > best_score:
                best_score = score
                with open("score.txt", "w") as fichier:
                    fichier.write(str(best_score))
            continue

        keys = pygame.key.get_pressed()

        if not (hero.jump_state):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                hero.jump_state = True
                print(f"{yellow}Space or A Key{reset}")
        else:
            if hero.jump_count >= -10:
                if hero.jump_count > 0:
                    hero.y -= hero.jump_count
                else:
                    hero.y += -hero.jump_count
                hero.jump_count -= 1
            else:
                hero.jump_state = False
                hero.jump_count = 10

        if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and hero.x >= 0:
            print(f"{green}Q or < key{reset}")
            hero.x -= 5
            hero.image = hero.left
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and hero.x <= 555:
            print(f"{light_blue}D or > key{reset}")
            hero.x += 5
            hero.image = hero.right
        elif (keys[pygame.K_f]):
            print(f"{red}F key{reset}")
            hero.image = hero.attack
        else:
            hero.image = hero.static

        hero.update_image()

        hero_rect = pygame.Rect(hero.x + 40, hero.y + 20, hero.width / 4, hero.height / 2)

        for p in pièce:
            piece_rect = pygame.Rect(p.x, p.y, p.size, p.size)
            if hero_rect.colliderect(piece_rect):
                print(f"{red}Collision détectée avec{reset}{yellow} une pièce{reset}{red} !{reset}")
                print(f"+1 score - Score {score}")
                pièce.remove(p)
                score += 1
                pièce.append(Pièce(random1(), random2()))
                break

        pygame.time.delay(70)
        draw(hero, score, time_left, best_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "start_menu"

    pygame.display.flip()

pygame.quit()
