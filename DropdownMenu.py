import pygame
class DropdownMenu:
    def __init__(self, width, height, options, default_option, font):
        self.width = width
        self.height = height
        self.options = options
        self.default_option = default_option
        self.font = font
        self.selected_option = default_option
        self.menu_open = False
        self.color = (62,78,86)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        # Draw the dropdown box
         # Draw the dropdown box
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height),1)

        # Render the selected option
        text = self.font.render(self.selected_option, 1, self.color)
        screen.blit(text, (self.x + 10, self.y ))

        # If the menu is open, draw the options
        if self.menu_open:
            y = self.y + self.height
            for option in self.options:
                # Render the option
                text = self.font.render(option, 1, self.color)
                screen.blit(text, (self.x + 10, y ))
                # Increment the y position for the next option
                y += self.height
    
    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def is_mouse_selection(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False

    def set_menu_selection(self, pos):
        if self.menu_open:
            y = self.y + self.height
            for option in self.options:
                if pos[1] > y and pos[1] < y + self.height:
                    self.selected_option = option
                    self.menu_open = False
                y += self.height