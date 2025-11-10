import pygame
import math
from math import gcd

# My slider class I made for pygame a few years ago - I do not think this has ever been used, 
# it was just made to be obselete for around 5 years... ( kinda sad)
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, color):
        self.rect = pygame.Rect(x, y, width, height)
        
        self.color = color
        self.minval = min_val
        self.maxval = max_val
        self.value = initial_val
        self.handle_rect = pygame.Rect(x, y, 10, height)
        self.handle_rect.centerx = self.get_handle_pos()
        self.is_dragging = False
        
    def get_handle_pos(self):
        return (self.rect.x + (self.rect.width * (self.value - self.minval) / (self.maxval - self.minval)))
    
    def draw(self, screen):
        pygame.draw.rect(screen,(200, 200, 200), self.rect, border_radius=5)
        pygame.draw.rect(screen, self.color, self.handle_rect, border_radius=5)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.is_dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

        elif event.type == pygame.MOUSEMOTION and self.is_dragging: # some good old clamping so we don't get infinity (sorry)
            mouse_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.handle_rect.centerx = mouse_x
            self.value = self.minval + (self.handle_rect.centerx - self.rect.x) / self.rect.width * (self.maxval - self.minval)





class Spirograph:
    def __init__(self, R, r, d):
        self.R = R
        self.r = r
        self.d = d
        self.points = []


        self.calculate_points()

    def calculate_points(self):
        self.points = []

        try:
            nRot = self.r // gcd(int(self.R), int(self.r))

        except ZeroDivisionError:
            nRot = 1
        
        steps = 1000 * nRot
        angle_step = (2 * math.pi) / 1000
        
        for i in range(int(steps) + 1):
            t_angle = angle_step * i
            x = (self.R - self.r) * math.cos(t_angle) + self.d * math.cos(((self.R - self.r) / self.r) * t_angle)
            y = (self.R - self.r) * math.sin(t_angle) - self.d * math.sin(((self.R - self.r) / self.r) * t_angle)
            
            screen_x = x + 400
            screen_y = y + 300
            self.points.append((screen_x, screen_y))
            
    def draw(self, screen, color):
        if len(self.points) > 1:
            # Use the dynamic color parameter
            pygame.draw.lines(screen, color, False, self.points, 2)


def main():
    pygame.init()
    
    # Screen settings
    screen_width, screen_height = 800, 700 
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Interactive Spirograph")
    black = (0, 0, 0)
    white = (255, 255, 255)
    largefont = pygame.font.Font(None, 48)
    smallfont = pygame.font.Font(None, 24)

    startR = 100
    startr = 50
    startd = 40

    spiro = Spirograph(100, 50, 40)

    slider_R = Slider(50, 80, 200, 20, 10, 200, startR, (255, 0, 0))
    slider_r = Slider(50, 130, 200, 20, 10, 100,startr, (0, 255, 0))
    slider_d = Slider(50, 180, 200, 20, 1, 100, startd, (0, 0, 255))
    
    sliderR = Slider(500, 80, 200, 20, 0, 255, 255, (255, 0, 0))
    sliderG = Slider(500, 130, 200, 20, 0, 255, 255, (0, 255, 0))
    sliderB = Slider(500, 180, 200, 20, 0, 255, 255, (0, 0, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            

            # next time i am switching away from python because this is just boring
            slider_R.handle_event(event)
            slider_r.handle_event(event)
            slider_d.handle_event(event)
            sliderR.handle_event(event)
            sliderG.handle_event(event)
            sliderB.handle_event(event)


        screen.fill(black)
        
        # updating the values from the slider so the program actually does stuff and is not a glorified png
        if spiro.R != slider_R.value or spiro.r != slider_r.value or spiro.d != slider_d.value:
            spiro.R =slider_R.value
            spiro.r =slider_r.value
            spiro.d =slider_d.value
            spiro.calculate_points()
        
        # dynamically grab the slider values for the colour so we can have colour (I over explained that I am very tired)
        current_color = (int(sliderR.value), int(sliderG.value), int(sliderB.value))

        # I think this is where we draw the thing? Who can tell atp
        spiro.draw(screen, current_color)
        
        slider_R.draw(screen)
        slider_r.draw(screen)
        slider_d.draw(screen)
        sliderR.draw(screen)
        sliderG.draw(screen)
        sliderB.draw(screen)

        # Just in case people forget what this is and that it is me
        title_text = largefont.render("Spirograph Sim by Toby Tragen", True, white)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 10))

        label_R = smallfont.render(f"R: {slider_R.value:.1f}", True, white) # cool python f string magic
        label_r = smallfont.render(f"r: {slider_r.value:.1f}", True, white) # so we don't get number like
        label_d = smallfont.render(f"d: {slider_d.value:.1f}", True, white) # 1.67676767676767676767676767


        screen.blit(label_R, (270, 80))
        screen.blit(label_r, (270, 130))
        screen.blit(label_d, (270, 180))
        
        colorR = smallfont.render(f"Red: {sliderR.value:.0f}", True, white)
        colorG = smallfont.render(f"Green: {sliderG.value:.0f}", True, white)
        colorB = smallfont.render(f"Blue: {sliderB.value:.0f}", True, white)


        screen.blit(colorR, (720, 80))
        screen.blit(colorG, (720, 130))
        screen.blit(colorB, (720, 180))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
