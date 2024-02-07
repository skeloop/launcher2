import pygame
import config
import version_checker
import sys
# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 800, 450
WIDTH_MIDDLE, HEIGHT_MIDDLE = WIDTH / 2, HEIGHT / 2
CENTER = WIDTH_MIDDLE, HEIGHT_MIDDLE

print("Breite: "+str(WIDTH))
print("Höhe: "+str(HEIGHT))
print("Mitte: "+str(CENTER))

# Erstellen Sie ein Fenster
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textur auf zweitem Sprite")

# Definition der Sprite-Klasse
class MySprite(pygame.sprite.Sprite):
    def __init__(self, sprite_id, p_x, p_y, s_x, s_y, image_path=None, event=None):
        super().__init__()
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image = pygame.Surface((s_x, s_y))
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (p_x, p_y)
        self.sprite_id = sprite_id
        self.tags = []
        self.hs_x, self.hs_y = s_x / 2, s_y / 2
        self.click_event = event

# Gruppe für Sprites erstellen
all_sprites = pygame.sprite.Group()
def add_tag_to_sprite(sprite, tag):
    for t in sprite.tags:
        if t == tag:
            remove_tag_from_sprite(sprite=sprite, tag=tag)
            return
    sprite.tags.append(tag)
def remove_tag_from_sprite(sprite, tag):
    if tag in sprite.tags:
        sprite.tags.remove(tag)

# Funktion zur Erstellung eines Sprites
def create_sprite(sprite_id, p_x, p_y, s_x, s_y, image_path=None):
    sprite = MySprite(sprite_id, p_x, p_y, s_x, s_y, image_path)
    sprite.rect.x = p_x
    sprite.rect.y = p_y
    all_sprites.add(sprite)
def square_click():
    print("CLICK")
# Hier werden alle Sprites erstellt.
create_sprite(1, 100, 100, 30, 30)
create_sprite(2, 300, 200, 30, 350, config.program_path+ str("//Images//left_bar.png"))  # Textur für das zweite Sprite


def remove_tag_from_any_sprite(tag):
    for sprite in all_sprites:
        if tag in sprite.tags:
            sprite.tags.remove(tag)
# Spiel-Schleife
running = True
object_selected = False
while running:
    for event in pygame.event.get():
        for sprite in all_sprites:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if sprite.rect.collidepoint(event.pos):
                        if object_selected:
                            remove_tag_from_any_sprite("selected")
                            object_selected = False
                            continue
                        else:
                            add_tag_to_sprite(sprite=sprite, tag="selected")
                            object_selected = True
                            continue
            if "selected" in sprite.tags:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                sprite.rect.y = mouse_y - sprite.hs_y
                sprite.rect.x = mouse_x - sprite.hs_x
                print(sprite.hs_y)
        if event.type == pygame.QUIT:
            running = False

    # Aktualisieren
    all_sprites.update()

    # Zeichnen
    screen.fill((0, 0, 0))  # Hintergrundfarbe
    all_sprites.draw(screen)

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()