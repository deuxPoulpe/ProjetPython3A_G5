import pygame

class Menu:

        
    def main_menu(self):

        pygame.init()
        screen = pygame.display.set_mode((800, 700))
        pygame.display.set_caption("Button Example")

        single_button = Button((800 - 230) // 2, 200, 230, 50, "Single Simulation", (200, 200, 200),screen)
        multi_button = Button((800 - 215) // 2, 300, 215, 50, "Multi Simulation", (200, 200, 200),screen)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                single_button.handle_event(event)
                multi_button.handle_event(event)

            screen.fill((255,255,255))

            single_button.draw()
            multi_button.draw()

            pygame.display.flip()

            if single_button.clicked:
                return False
            elif multi_button.clicked:
                return True 

class Button:
    def __init__(self, x, y, width, height, text, color,screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.clicked = False
        self.screen = screen

    def draw_text(self,text, x, y, color=(0,0,0)):
        text_surface = pygame.font.Font(None, 36).render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.draw_text(self.text, self.rect.x + 10, self.rect.y + 10, (255,255,255) if self.clicked else (0,0,0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False



