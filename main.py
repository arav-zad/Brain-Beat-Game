import pygame  # Import the pygame module
import sys  # Import the sys module for system functions
from settings import *  # Import all settings
from sprites import *  # Import all sprite classes
import random  # Import the random module
import webbrowser  # Import the webbrowser module
from pygame import mixer  # Import the mixer from pygame
pygame.init()  # Initialize pygame
mixer.init()  # Initialize the mixer

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION  # Import specific events from pygame.locals

DEFAULT_VOLUME = 0.5  # Set the default volume to 0.5
pygame.mixer.music.set_volume(DEFAULT_VOLUME)  # Set the mixer music volume to default

SCREEN = pygame.display.set_mode((1280, 720))  # Set the screen size to 1280x720
BG = pygame.image.load("assets/Background.png")  # Load the background image
OPBG = pygame.image.load("assets/OptionsBG.jpg")  # Load the options background image
current_volume = 0.5  # Initialize current volume to 0.5
mixer.music.set_volume(current_volume)  # Set the mixer music volume to current volume



def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)  # Load a font of a specific size

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image  # Set button image
		self.x_pos = pos[0]  # X position
		self.y_pos = pos[1]  # Y position
		self.font = font  # Font for text
		self.base_color, self.hovering_color = base_color, hovering_color  # Colors
		self.text_input = text_input  # Text on button
		self.text = self.font.render(self.text_input, True, self.base_color)  # Render text
		if self.image is None:
			self.image = self.text  # Use text as image if no image
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Button rect
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Text rect

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)  # Draw button image
		screen.blit(self.text, self.text_rect)  # Draw button text

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True  # Check if clicked
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)  # Change color on hover
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)  # Change back on leave

class EventHandler:
    def __init__(self):
        EventHandler.events = pygame.event.get()  # Initialize events

    def run():
        EventHandler.events = pygame.event.get()  # Update events

    def clicked() -> bool:
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return True  # Check if mouse clicked
        return False


UNSELECTED = "red"
SELECTED = "white"
BUTTONSTATES = {
    True: SELECTED,
    False: UNSELECTED
}

class UI:
    def init(app):
        UI.font = get_font(20)  # Set small font
        UI.sfont = get_font(20)  # Set medium font
        UI.lfont = get_font(40)  # Set large font
        UI.xlfont = get_font(50)  # Set extra-large font
        UI.center = (app.screen.get_size()[0]//2, app.screen.get_size()[1]//2)  # Center of the screen
        UI.half_width = app.screen.get_size()[0]//2  # Half width of the screen
        UI.half_height = app.screen.get_size()[1]//2  # Half height of the screen

        UI.fonts = {
            'sm': UI.sfont,
            'm': UI.font,
            'l': UI.lfont,
            'xl': UI.xlfont
        }  # Font dictionary for easy access

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos  # Position of the slider
        self.size = size  # Size of the slider
        self.hovered = False  # Hover state
        self.grabbed = False  # Grab state

        self.slider_left_pos = self.pos[0] - (size[0]//2)  # Left position of the slider
        self.slider_right_pos = self.pos[0] + (size[0]//2)  # Right position of the slider
        self.slider_top_pos = self.pos[1] - (size[1]//2)  # Top position of the slider

        self.min = min  # Minimum value
        self.max = max  # Maximum value
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val  # Initial value as percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])  # Container rectangle
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])  # Button rectangle

        # Label
        self.text = UI.fonts['m'].render(str(int(self.get_value())), True, "white", None)  # Render text
        self.label_rect = self.text.get_rect(center = (self.pos[0], self.slider_top_pos - 15))  # Label rectangle

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]  # Get mouse position
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos  # Ensure within left bound
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos  # Ensure within right bound
        self.button_rect.centerx = pos  # Update button position

    def hover(self):
        self.hovered = True  # Set hover state to true

    def render(self, app):
        pygame.draw.rect(app.screen, "darkgray", self.container_rect)  # Draw container
        pygame.draw.rect(app.screen, BUTTONSTATES[self.hovered], self.button_rect)  # Draw button

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1  # Calculate value range
        button_val = self.button_rect.centerx - self.slider_left_pos  # Calculate button value

        return (button_val/val_range)*(self.max-self.min)+self.min  # Return scaled value

    def display_value(self, app):
        self.text = UI.fonts['m'].render(str(int(self.get_value())), True, "white", None)  # Render value text
        app.screen.blit(self.text, self.label_rect)  # Blit text onto screen

class NormButton:
    def __init__(self, x, y, colour):
        self.x = x  # X position
        self.y = y  # Y position
        self.colour = colour  # Button color
        self.rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)  # Button rectangle
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)  # Draw button

    def clicked(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)  # Check if clicked

class EduButton:
    def __init__(self, x, y, image_file, width, height, flash_image_file, first_audio, second_audio):
        self.x = x  # X position
        self.y = y  # Y position
        self.width = width  # Width of button
        self.height = height  # Height of button
        self.image = pygame.image.load(image_file)  # Load image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale image
        self.flash_image = pygame.image.load(flash_image_file)  # Load flash image
        self.flash_image = pygame.transform.scale(self.flash_image, (275, 275))  # Scale flash image
        self.first_audio = pygame.mixer.Sound(first_audio)  # Load first audio
        self.second_audio = pygame.mixer.Sound(second_audio)  # Load second audio
        self.hovered = False  # Hover state
        self.hover_sound_played = False  # Hover sound state

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Draw button

    def draw_flash_image(self, screen):
        screen.blit(self.flash_image, (self.x - 12, self.y - 12))  # Draw flash image centered

    def draw_hover_image(self, screen):
        screen.blit(self.flash_image, (self.x - 12, self.y - 12))  # Draw hover image centered

    def clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height  # Check if clicked

    def handle_hover(self, mouse_x, mouse_y):
        if self.clicked(mouse_x, mouse_y):  # Check hover
            if not self.hover_sound_played:
                self.second_audio.play()  # Play hover sound
                self.hover_sound_played = True  # Mark sound as played
            self.hovered = True  # Set hover state
        else:
            self.hovered = False  # Reset hover state
            self.hover_sound_played = False  # Reset sound state

class ChallButton:
    def __init__(self, x, y, image, width, height, sound_file):
        self.x = x  # X position
        self.y = y  # Y position
        self.image = pygame.image.load(image).convert_alpha()  # Load and convert image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale image
        self.rect = self.image.get_rect(topleft=(x, y))  # Image rectangle
        self.sound = pygame.mixer.Sound(sound_file)  # Load sound

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Draw button

    def clicked(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)  # Check if clicked

class UIElement:
    def __init__(self, x, y, text, font_size):
        self.x = x  # X position
        self.y = y  # Y position
        self.text = text  # Text to display
        self.font_size = font_size  # Font size

    def draw(self, screen):
        font = get_font(self.font_size)  # Get font
        text_surface = font.render(self.text, True, WHITE)  # Render text
        screen.blit(text_surface, (self.x, self.y))  # Draw text

class EduAudio:
    def __init__(self, sound_file: str):
        self.sound = pygame.mixer.Sound(sound_file)  # Load sound file
        self.current_channel = None  # Initialize audio channel

    def play(self):
        self.current_channel = pygame.mixer.find_channel(True)  # Find available audio channel
        self.current_channel.play(self.sound)  # Play sound

def confirm_exit(screen, return_to_function):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # Set transparency
    overlay.fill((0, 0, 0))  # Fill with black color

    font = get_font(30)  # Get font
    message = '''
Some progress may not be saved. 
Are you okay with this?'''  # Confirmation message
    lines = message.split('\n')  # Split message into lines
    
    yes_button = Button(image=None, pos=(800, 475), text_input="STAY", font=get_font(30), base_color="White", hovering_color=GREEN)  # Stay button
    no_button = Button(image=None, pos=(400, 475), text_input="QUIT", font=get_font(30), base_color="White", hovering_color="#800000")  # Quit button

    while True:
        screen.blit(overlay, (0, 0))  # Draw overlay

        y_offset = 200  # Initial Y offset for text
        for line in lines:
            text_surface = font.render(line, True, WHITE)  # Render text line
            screen.blit(text_surface, (150, y_offset))  # Draw text line
            y_offset += 40  # Update Y offset

        yes_button.update(screen)  # Update stay button
        no_button.update(screen)  # Update quit button
        pygame.display.update()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit program
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
                if yes_button.checkForInput((mouse_x, mouse_y)):
                    return_to_function()  # Call return function
                if no_button.checkForInput((mouse_x, mouse_y)):
                    return True  # Confirm exit
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
                yes_button.changeColor((mouse_x, mouse_y))  # Change stay button color
                no_button.changeColor((mouse_x, mouse_y))  # Change quit button color

def confirm_clear_high_scores(screen):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # Set transparency
    overlay.fill((0, 0, 0))  # Fill with black color

    font = get_font(30)  # Get font
    message = '''
Are you sure you want to clear 
ALL High Scores?'''  # Confirmation message
    lines = message.split('\n')  # Split message into lines
    
    clear_button = Button(image=None, pos=(400, 475), text_input="CLEAR", font=get_font(30), base_color="White", hovering_color="#800000")  # Clear button
    back_button = Button(image=None, pos=(800, 475), text_input="BACK", font=get_font(30), base_color="White", hovering_color=GREEN)  # Back button

    while True:
        screen.blit(overlay, (0, 0))  # Draw overlay

        y_offset = 200  # Initial Y offset for text
        for line in lines:
            text_surface = font.render(line, True, WHITE)  # Render text line
            screen.blit(text_surface, (150, y_offset))  # Draw text line
            y_offset += 40  # Update Y offset

        clear_button.update(screen)  # Update clear button
        back_button.update(screen)  # Update back button
        pygame.display.update()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit program
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
                if clear_button.checkForInput((mouse_x, mouse_y)):
                    reset_file_norm = open("high_score.txt", "w")  # Open normal mode high score file
                    reset_file_norm.write("0")  # Reset high score
                    reset_file_norm.close()  # Close file

                    reset_file_edu = open("edu_high_score.txt", "w")  # Open education mode high score file
                    reset_file_edu.write("0")  # Reset high score
                    reset_file_edu.close()  # Close file

                    reset_file_chall = open("chall_high_score.txt", "w")  # Open challenge mode high score file
                    reset_file_chall.write("0")  # Reset high score
                    reset_file_chall.close()  # Close file

                    options()  # Return to options after clearing high scores
                    return
                if back_button.checkForInput((mouse_x, mouse_y)):
                    options()  # Return to options without clearing high scores
                    return
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
                clear_button.changeColor((mouse_x, mouse_y))  # Change clear button color
                back_button.changeColor((mouse_x, mouse_y))  # Change back button color

def game_over_audio():
    beeps = [Audio(BEEP1), Audio(BEEP2), Audio(BEEP3), Audio(BEEP4)] 
    for beep in beeps:
        beep.play() # Play all beats synched to get the "BEEP!" - Game over sound





def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()  # Get current mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()  # Get current mouse position
        SCREEN.blit(OPBG, (0, 0))  # Draw background image

        PLAY_TEXT = get_font(50).render("SELECT GAME MODE", True, "#b68f40")  # Render game mode selection text
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 50))  # Center the text
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)  # Draw the text on the screen

        PLAY_BACK = Button(image=None, pos=(120, 50), 
                            text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")  # Create back button

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)  # Change color on hover
        PLAY_BACK.update(SCREEN)  # Update button display

        PLAY_EDUMODE = Button(image=None, pos=(220, 600),
                              text_input="EDUCATION", font=get_font(20), base_color=WHITE, hovering_color=GREEN)  # Create education mode button
        PLAY_EDUMODE.changeColor(PLAY_MOUSE_POS)  # Change color on hover
        PLAY_EDUMODE.update(SCREEN)  # Update button display

        PLAY_NORMMODE = Button(image=None, pos=(640, 600),
                                    text_input="NORMAL", font=get_font(20), base_color=WHITE, hovering_color=GREEN)  # Create normal mode button
        PLAY_NORMMODE.changeColor(PLAY_MOUSE_POS)  # Change color on hover
        PLAY_NORMMODE.update(SCREEN)  # Update button display

        PLAY_CHALLMMODE = Button(image=None, pos=(1060, 600),
                              text_input="CHALLENGE", font=get_font(20), base_color=WHITE, hovering_color=GREEN)  # Create challenge mode button
        PLAY_CHALLMMODE.changeColor(PLAY_MOUSE_POS)  # Change color on hover
        PLAY_CHALLMMODE.update(SCREEN)  # Update button display

        eduplayimg = pygame.image.load("assets/PlayEdu.png")  # Load education mode image
        eduplayimgscaled = pygame.transform.scale(eduplayimg, (180, 430))  # Scale image
        SCREEN.blit(eduplayimgscaled, (130, 130))  # Draw image on screen

        normplayimg = pygame.image.load("assets/PlayNorm.png")  # Load normal mode image
        normplayimgscaled = pygame.transform.scale(normplayimg, (200, 430))  # Scale image
        SCREEN.blit(normplayimgscaled, (532, 130))  # Draw image on screen

        challplayimg = pygame.image.load("assets/PlayChall.png")  # Load challenge mode image
        challplayimgscaled = pygame.transform.scale(challplayimg, (200, 430))  # Scale image
        SCREEN.blit(challplayimgscaled, (970, 130))  # Draw image on screen

        for button in [PLAY_EDUMODE, PLAY_NORMMODE, PLAY_CHALLMMODE]:
            button.changeColor(MENU_MOUSE_POS)  # Change button color on hover
            button.update(SCREEN)  # Update button display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_EDUMODE.checkForInput(MENU_MOUSE_POS):
                    edumode()  # Start education mode
                if PLAY_NORMMODE.checkForInput(MENU_MOUSE_POS):
                    normmode()  # Start normal mode
                if PLAY_CHALLMMODE.checkForInput(MENU_MOUSE_POS):
                    challmode()  # Start challenge mode
                if PLAY_BACK.checkForInput(MENU_MOUSE_POS):
                    main_menu()  # Return to main menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()  # Return to main menu

        pygame.display.update()  # Update display





def main_menu():
    while True:

        pygame.display.set_caption(TITLE)  # Set the window title
        SCREEN.blit(BG, (0, 0))  # Draw the background image
        MENU_MOUSE_POS = pygame.mouse.get_pos()  # Get the current mouse position

        # Render the text onto a surface
        SCIENTIFIC_BANNER_TEXT = get_font(20).render("Scientifically Proven!", True, "#ff9535")

        # Rotate the surface by 10 degrees
        rotated_banner_text = pygame.transform.rotate(SCIENTIFIC_BANNER_TEXT, 10)

        # Get the rectangle of the rotated surface
        SCIENTIFIC_BANNER_RECT = rotated_banner_text.get_rect(center=(300, 290))

        # Blit the rotated surface onto the screen
        SCREEN.blit(rotated_banner_text, SCIENTIFIC_BANNER_RECT)

        MENU_TEXT = get_font(100).render("BRAIN BEAT", True, "#b68f40")  # Render the main menu text
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))  # Center the main menu text

        PLAY_BUTTON = Button(image=None, pos=(215, 450), 
                            text_input="PLAY", font=get_font(40), base_color="White", hovering_color="#d6b4fc")  # Create the Play button
        OPTIONS_BUTTON = Button(image=None, pos=(215, 550), 
                            text_input="OPTIONS", font=get_font(40), base_color="White", hovering_color="#08787f")  # Create the Options button
        QUIT_BUTTON = Button(image=None, pos=(215, 650), 
                            text_input="QUIT", font=get_font(40), base_color="White", hovering_color="#800000")  # Create the Quit button
        
        logoimg = pygame.image.load("assets/BrainBeatNewTransparent.png")  # Load the logo image
        logoimgscaled = pygame.transform.scale(logoimg, (445, 445))  # Scale the logo image
        SCREEN.blit(logoimgscaled, (575, 220))  # Draw the scaled logo image on the screen

        SCREEN.blit(MENU_TEXT, MENU_RECT)  # Draw the main menu text on the screen

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)  # Change button color on hover
            button.update(SCREEN)  # Update button display
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Start play mode
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()  # Go to options menu
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()  # Quit pygame
                    sys.exit()  # Exit program

        pygame.display.update()  # Update the display





def options():
    app = type('', (), {})()  # Create an empty object to simulate the app
    app.screen = SCREEN  # Assign the main screen to the app
    UI.init(app)  # Initialize the UI with the app

    slider = Slider((900, 200), (600, 40), 0.5, 0, 100)  # Create a slider object

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()  # Get the current mouse position
        MOUSE_CLICKED = pygame.mouse.get_pressed()  # Get the current mouse button state

        SCREEN.blit(OPBG, (0, 0))  # Draw the options background

        OPTIONS_TEXT = get_font(50).render("OPTIONS", True, "#b68f40")  # Render the options text
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))  # Center the options text
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)  # Draw the options text on the screen

        OPTIONS_BACK = Button(image=None, pos=(120, 50), 
                              text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")  # Create the back button

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)  # Change the back button color on hover
        OPTIONS_BACK.update(SCREEN)  # Update the back button display

        VOLUME_TEXT = get_font(35).render("Volume:", True, "#08787f")  # Render the volume text
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(325, 200))  # Center the volume text
        SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)  # Draw the volume text on the screen

        CLEARHS_TEXT = get_font(35).render("High Scores:", True, "#08787f")  # Render the high scores text
        CLEARHS_RECT = CLEARHS_TEXT.get_rect(center=(325, 350))  # Center the high scores text
        SCREEN.blit(CLEARHS_TEXT, CLEARHS_RECT)  # Draw the high scores text on the screen

        HTP_TEXT = get_font(35).render("How to Play:", True, "#08787f")  # Render the how to play text
        HTP_RECT = HTP_TEXT.get_rect(center=(325, 500))  # Center the how to play text
        SCREEN.blit(HTP_TEXT, HTP_RECT)  # Draw the how to play text on the screen

        HTP_DETAIL_TEXT = get_font(20).render("To get the most fun out of the", True, "White")  # Render the how to play detail text
        HTP_DETAIL_RECT = HTP_DETAIL_TEXT.get_rect(center=(900, 500))  # Center the how to play detail text
        SCREEN.blit(HTP_DETAIL_TEXT, HTP_DETAIL_RECT)  # Draw the how to play detail text on the screen

        HTP_DETAIL_TEXT2 = get_font(20).render("Brain Beat experience, click", True, "White")  # Render the how to play detail text 2
        HTP_DETAIL_RECT2 = HTP_DETAIL_TEXT2.get_rect(center=(885, 550))  # Center the how to play detail text 2
        SCREEN.blit(HTP_DETAIL_TEXT2, HTP_DETAIL_RECT2)  # Draw the how to play detail text 2 on the screen

        HTP_DETAIL_TEXT3 = get_font(20).render("(Redirection to web page)", True, "White")  # Render the how to play detail text 3
        HTP_DETAIL_RECT3 = HTP_DETAIL_TEXT3.get_rect(center=(890, 670))  # Center the how to play detail text 3
        SCREEN.blit(HTP_DETAIL_TEXT3, HTP_DETAIL_RECT3)  # Draw the how to play detail text 3 on the screen

        # Create the How to Play Button
        HTP_BUTTON = Button(image=None, pos=(900, 610), 
                            text_input="HERE", font=get_font(40), base_color="White", hovering_color="#fc4665")

        HTP_BUTTON.changeColor(OPTIONS_MOUSE_POS)  # Change the How to Play button color on hover
        HTP_BUTTON.update(SCREEN)  # Update the How to Play button display

        CLEARHS_BUTTON = Button(image=None, pos=(880, 350), 
                                text_input="CLEAR ALL", font=get_font(30), base_color="White", hovering_color="#fc4665")

        CLEARHS_BUTTON.changeColor(OPTIONS_MOUSE_POS)  # Change the Clear High Scores button color on hover
        CLEARHS_BUTTON.update(SCREEN)  # Update the Clear High Scores button display

        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        mouse = pygame.mouse.get_pressed()  # Get the current mouse button state

        # Handle the slider
        if slider.container_rect.collidepoint(mouse_pos):
            if mouse[0]:
                slider.grabbed = True  # Check if the slider is grabbed
        if not mouse[0]:
            slider.grabbed = False  # Release the slider if the mouse button is not pressed
        if slider.button_rect.collidepoint(mouse_pos):
            slider.hover()  # Change the slider state to hovered
        if slider.grabbed:
            slider.move_slider(mouse_pos)  # Move the slider
            slider.hover()  # Change the slider state to hovered
        else:
            slider.hovered = False  # Change the slider state to not hovered
        slider.render(app)  # Render the slider
        slider.display_value(app)  # Display the slider value

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit the program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()  # Go back to the main menu
                if HTP_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open("https://online.publuu.com/554222/1249336")  # Open the How to Play link

        if CLEARHS_BUTTON.checkForInput(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  
                confirm_clear_high_scores(SCREEN)  # Confirm clearing high scores

        pygame.display.update()  # Update the display





def edumode():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize pygame screen with specified dimensions
    pygame.display.set_caption(TITLE)  # Set the window title of the game
    clock = pygame.time.Clock()  # Initialize pygame clock for managing frame rate

    # Load animal images and corresponding sounds
    ANIMAL_IMAGES = ["EduMode/Pig.png", "EduMode/Snake.png", "EduMode/Cow.png", "EduMode/Lion.png"]
    FIRST_ANIMAL_SOUNDS = ["EduMode/PigAudio.mp3", "EduMode/SnakeAudio.mp3", "EduMode/CowAudio.mp3", "EduMode/LionAudio.mp3"]
    SECOND_ANIMAL_SOUNDS = ["EduMode/FinalPigOink.mp3", "EduMode/FinalSnakeHiss.mp3", "EduMode/FinalCowMoo.mp3", "EduMode/FinalLionRoar.mp3"]
    FLASH_IMAGES = ["EduMode/PigFlash.png", "EduMode/SnakeFlash.png", "EduMode/CowFlash.png", "EduMode/LionFlash.png"]

    # Create instances of EduButton with adjusted coordinates, sizes, and associated files
    animals = [EduButton(250, 100, ANIMAL_IMAGES[0], width=250, height=250, flash_image_file=FLASH_IMAGES[0], first_audio=FIRST_ANIMAL_SOUNDS[0], second_audio=SECOND_ANIMAL_SOUNDS[0]), 
               EduButton(600, 100, ANIMAL_IMAGES[1], width=250, height=250, flash_image_file=FLASH_IMAGES[1], first_audio=FIRST_ANIMAL_SOUNDS[1], second_audio=SECOND_ANIMAL_SOUNDS[1]),
               EduButton(250, 400, ANIMAL_IMAGES[2], width=250, height=250, flash_image_file=FLASH_IMAGES[2], first_audio=FIRST_ANIMAL_SOUNDS[2], second_audio=SECOND_ANIMAL_SOUNDS[2]), 
               EduButton(600, 400, ANIMAL_IMAGES[3], width=250, height=250, flash_image_file=FLASH_IMAGES[3], first_audio=FIRST_ANIMAL_SOUNDS[3], second_audio=SECOND_ANIMAL_SOUNDS[3])]

    back_button = Button(image=None, pos=(120, 50), text_input="BACK", font=get_font(40), base_color="White", hovering_color="#b68f40")

    OPTIONS_TEXT = get_font(50).render("EDUCATION", True, "#b68f40")  # Render the text for the game mode title
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))  # Get the rectangle of the rendered text for positioning

    # Function to retrieve the highest score from the file
    def get_high_score():
        with open("edu_high_score.txt", "r") as file:
            score = file.read()
        return int(score)

    # Function to save the score to the file if it's higher than the existing high score
    def save_score(score, high_score):
        with open("edu_high_score.txt", "w") as file:
            if score > high_score:
                file.write(str(score))
            else:
                file.write(str(high_score))

    # Function to initialize a new game session by resetting variables
    def new_game():
        nonlocal waiting_input, pattern, current_step, score, high_score
        waiting_input = False
        pattern = []
        current_step = 0
        score = 0
        high_score = get_high_score()

    # Function to run the main game loop
    def run_game():
        nonlocal playing, clicked_button
        playing = True
        while playing:
            clock.tick(FPS)
            clicked_button = None
            events()
            draw()
            update()

    # Function to update the game state based on user input and game logic
    def update():
        nonlocal waiting_input, current_step, playing, score
        if not waiting_input:
            pygame.time.wait(1000)
            pattern.append(random.choice(animals))
            for button in pattern:
                button_animation(button)
                pygame.time.wait(3200)  # Adjusted delay to accommodate audio length
            waiting_input = True
        else:
            if clicked_button and clicked_button == pattern[current_step]:
                # Delay to ensure clear feedback for correct click
                pygame.time.wait(500)
                clicked_button.second_audio.play()  # Play the second audio when user clicks correctly
                user_clicked_button_animation(clicked_button)
                current_step += 1
                if current_step == len(pattern):
                    score += 1
                    waiting_input = False
                    current_step = 0
            elif clicked_button and clicked_button != pattern[current_step]:
                game_over_animation()
                save_score(score, high_score)
                playing = False

    # Function to animate button flash effect during pattern presentation
    def button_animation(button):
        sound = button.first_audio
        original_surface = screen.copy()
        flash_surface = pygame.Surface((250, 250))  # Adjusted flash surface size
        flash_surface = flash_surface.convert_alpha()
        r, g, b, a = (255, 255, 255, 0)  # Using white for flash
        sound.play()
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, ANIMATION_SPEED * step):
                screen.blit(original_surface, (0, 0))
                flash_surface.fill((r, g, b, alpha))
                screen.blit(flash_surface, (button.x, button.y))  # Adjusted position to match button location
                pygame.display.update()
                clock.tick(FPS)
        screen.blit(original_surface, (0, 0))

    # Function to animate the flash effect when the user clicks on a button
    def user_clicked_button_animation(button):
        button.draw_flash_image(screen)

    # Function to animate game over effect when the user makes a mistake
    def game_over_animation():
        original_surface = screen.copy()
        flash_surface = pygame.Surface((screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        game_over_audio()
        r, g, b = WHITE
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    clock.tick(FPS)

    # Function to draw elements onto the screen during the game
    def draw():
        screen.fill(BGCOLOUR)
        UIElement(900, 300, f"Score: {str(score)}", 25).draw(screen)
        UIElement(900, 380, f"High score: {str(high_score)}", 25).draw(screen)
        for button in animals:
            if button.hovered:
                button.draw_hover_image(screen)
            else:
                button.draw(screen)
        back_button.update(screen)
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        pygame.display.update()

    # Function to handle various events during the game, such as mouse clicks and movements
    def events():
        nonlocal clicked_button, playing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in animals:
                    if button.clicked(mouse_x, mouse_y):
                        clicked_button = button
                        user_clicked_button_animation(clicked_button)
                if back_button.checkForInput((mouse_x, mouse_y)):
                    confirm_exit(screen, edumode)
                    play()
                    return
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in animals:
                    button.handle_hover(mouse_x, mouse_y)
                back_button.changeColor((mouse_x, mouse_y))

    # Initialize game variables and start the main game loop
    waiting_input = False
    pattern = []
    current_step = 0
    score = 0
    high_score = get_high_score()
    playing = True
    clicked_button = None

    while True:
        new_game()
        run_game()





def normmode():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize pygame screen with specified dimensions
    pygame.display.set_caption(TITLE)  # Set the window title of the game
    clock = pygame.time.Clock()  # Initialize pygame clock for managing frame rate

    beeps = [Audio(BEEP1), Audio(BEEP2), Audio(BEEP3), Audio(BEEP4)]
    flash_colours = [YELLOW, BLUE, RED, GREEN]
    colours = [DARKYELLOW, DARKBLUE, DARKRED, DARKGREEN]
    buttons = [
        NormButton(410, 150, DARKYELLOW),  # Create a button with dark yellow color at specified position
        NormButton(630, 150, DARKBLUE),   # Create a button with dark blue color at specified position
        NormButton(410, 370, DARKRED),    # Create a button with dark red color at specified position
        NormButton(630, 370, DARKGREEN),  # Create a button with dark green color at specified position
    ]

    back_button = Button(image=None, pos=(120, 50), text_input="BACK", font=get_font(40), base_color="White", hovering_color="#b68f40")

    OPTIONS_TEXT = get_font(50).render("NORMAL", True, "#b68f40")  # Render the text for the game mode title
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))  # Get the rectangle of the rendered text for positioning

    # Function to retrieve the highest score from the file
    def get_high_score():
        with open("high_score.txt", "r") as file:
            score = file.read()
        return int(score)

    # Function to save the score to the file if it's higher than the existing high score
    def save_score(score, high_score):
        with open("high_score.txt", "w") as file:
            if score > high_score:
                file.write(str(score))
            else:
                file.write(str(high_score))

    # Function to initialize a new game session by resetting variables
    def new_game():
        nonlocal waiting_input, pattern, current_step, score, high_score
        waiting_input = False
        pattern = []
        current_step = 0
        score = 0
        high_score = get_high_score()

    # Function to run the main game loop
    def run_game():
        nonlocal playing, clicked_button
        playing = True
        while playing:
            clock.tick(FPS)
            clicked_button = None
            events()
            draw()
            update()

    # Function to update the game state based on user input and game logic
    def update():
        nonlocal waiting_input, current_step, playing, score
        if not waiting_input:
            pygame.time.wait(1000)
            pattern.append(random.choice(colours))
            for button in pattern:
                button_animation(button)
                pygame.time.wait(200)
            waiting_input = True
        else:
            if clicked_button and clicked_button == pattern[current_step]:
                button_animation(clicked_button)
                current_step += 1
                if current_step == len(pattern):
                    score += 1
                    waiting_input = False
                    current_step = 0
            elif clicked_button and clicked_button != pattern[current_step]:
                game_over_animation()
                save_score(score, high_score)
                playing = False

    # Function to animate button flash effect during pattern presentation
    def button_animation(colour):
        for i in range(len(colours)):
            if colours[i] == colour:
                sound = beeps[i]
                flash_colour = flash_colours[i]
                button = buttons[i]
        original_surface = screen.copy()
        flash_surface = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = flash_colour
        sound.play()
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, ANIMATION_SPEED * step):
                screen.blit(original_surface, (0, 0))
                flash_surface.fill((r, g, b, alpha))
                screen.blit(flash_surface, (button.x, button.y))  # Adjusted position to match button location
                pygame.display.update()
                clock.tick(FPS)
        screen.blit(original_surface, (0, 0))

    # Function to animate game over effect when the user makes a mistake
    def game_over_animation():
        original_surface = screen.copy()
        flash_surface = pygame.Surface((screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        game_over_audio()
        r, g, b = WHITE
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    clock.tick(FPS)

    # Function to draw elements onto the screen during the game
    def draw():
        screen.fill(BGCOLOUR)
        UIElement(900, 300, f"Score: {str(score)}", 25).draw(screen)
        UIElement(900, 380, f"High score: {str(high_score)}", 25).draw(screen)
        for button in buttons:
            button.draw(screen)
        # Draw the BACK button
        back_button.update(screen)
        # Draw the OPTIONS text
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        pygame.display.update()

    # Function to handle various events during the game, such as mouse clicks and movements
    def events():
        nonlocal clicked_button, playing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in buttons:
                    if button.clicked(mouse_x, mouse_y):
                        clicked_button = button.colour
                # Check if the BACK button is clicked
                if back_button.checkForInput((mouse_x, mouse_y)):
                    confirm_exit(screen, normmode)
                    play()  # Call the play() function
                    return  # Exit the current normmode function

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                back_button.changeColor((mouse_x, mouse_y))

    # Initialize game variables and start the main game loop
    waiting_input = False
    pattern = []
    current_step = 0
    score = 0
    high_score = get_high_score()
    playing = True
    clicked_button = None

    while True:
        new_game()
        run_game()





def challmode():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize pygame screen with specified dimensions
    pygame.display.set_caption(TITLE)  # Set the window title of the game
    clock = pygame.time.Clock()  # Initialize pygame clock for managing frame rate

    # Load images and sounds for challenge mode
    HARD_IMAGES = ["ChallMode/Fire.png", "ChallMode/Joker.png", "ChallMode/PurpSkull.png", "ChallMode/Skull.png"]
    HARD_SOUNDS = ["ChallMode/FireAudio.mp3", "ChallMode/JokerAudio.mp3", "ChallMode/PurpSkullAudio.mp3", "ChallMode/SkullAudio.mp3"]

    challimg = [ChallButton(250, 150, HARD_IMAGES[0], width=260, height=260, sound_file=HARD_SOUNDS[0]),  # Create challenge buttons with specified parameters
                ChallButton(560, 160, HARD_IMAGES[1], width=250, height=250, sound_file=HARD_SOUNDS[1]),
                ChallButton(250, 450, HARD_IMAGES[2], width=250, height=200, sound_file=HARD_SOUNDS[2]),
                ChallButton(590, 460, HARD_IMAGES[3], width=200, height=200, sound_file=HARD_SOUNDS[3])]

    back_button = Button(image=None, pos=(120, 50), text_input="BACK", font=get_font(40), base_color="White", hovering_color="#b68f40")

    OPTIONS_TEXT = get_font(50).render("CHALLENGE", True, "#b68f40")  # Render the text for the challenge mode title
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))  # Get the rectangle of the rendered text for positioning

    # Function to retrieve the highest score from the file, handling potential file absence
    def get_high_score():
        try:
            with open("chall_high_score.txt", "r") as file:
                score = int(file.read())
        except FileNotFoundError:
            score = 0
        return score

    # Function to save the score to the file if it's higher than the existing high score
    def save_score(score, high_score):
        with open("chall_high_score.txt", "w") as file:
            file.write(str(max(score, high_score)))

    # Function to initialize a new game session by resetting variables
    def new_game():
        nonlocal waiting_input, pattern, current_step, score, high_score, start_ticks
        waiting_input = False
        pattern = []
        current_step = 0
        score = 0
        high_score = get_high_score()
        start_ticks = pygame.time.get_ticks()

    # Function to run the main game loop
    def run_game():
        nonlocal playing
        playing = True
        while playing:
            clock.tick(FPS)
            events()
            draw()
            update()

    # Function to update the game state based on user input and game logic
    def update():
        nonlocal waiting_input, current_step, playing, score, start_ticks
        if not waiting_input:
            pygame.time.wait(1000)
            pattern.append(random.choice(challimg))
            for button in pattern:
                button_animation(button, play_sound=True)
                pygame.time.wait(1500)  # Adjusted delay to 1.5 seconds between each button
            waiting_input = True
            start_ticks = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - start_ticks >= 3000:
                game_over_animation()
                save_score(score, high_score)
                playing = False

    # Function to animate button flash effect during pattern presentation
    def button_animation(button, play_sound=False):
        original_surface = screen.copy()
        button_rect = button.image.get_rect(topleft=(button.x, button.y))  # Get the rect of the button's image
        flash_surface = pygame.Surface((button_rect.width, button_rect.height))  # Use image dimensions
        flash_surface = flash_surface.convert_alpha()
        r, g, b, a = (255, 255, 255, 0)  # Using white for flash
        if play_sound:
            button.sound.play()
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, ANIMATION_SPEED * step):
                screen.blit(original_surface, (0, 0))
                flash_surface.fill((r, g, b, alpha))
                screen.blit(flash_surface, button_rect.topleft)  # Position adjusted to button's top-left corner
                pygame.display.update()
                clock.tick(FPS)
        screen.blit(original_surface, (0, 0))

    # Function to animate game over effect when the user makes a mistake
    def game_over_animation():
        original_surface = screen.copy()
        flash_surface = pygame.Surface((screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        game_over_audio()
        r, g, b = WHITE
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    clock.tick(FPS)

    # Function to draw elements onto the screen during the game
    def draw():
        screen.fill(BGCOLOUR)
        UIElement(900, 300, f"Score: {str(score)}", 25).draw(screen)
        UIElement(900, 380, f"High score: {str(high_score)}", 25).draw(screen)
        for button in challimg:
            button.draw(screen)
        # Draw the BACK button
        back_button.update(screen)
        # Draw the OPTIONS text
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        pygame.display.update()

    # Function to handle various events during the game, such as mouse clicks and movements
    def events():
        nonlocal playing, current_step, waiting_input, start_ticks, score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in challimg:
                    if button.clicked(mouse_x, mouse_y):
                        if button == pattern[current_step]:
                            button_animation(button)  # Call button_animation without sound
                            current_step += 1
                            start_ticks = pygame.time.get_ticks()  # Reset the timer
                            if current_step == len(pattern):
                                score += 1
                                waiting_input = False
                                current_step = 0
                                return
                        else:
                            game_over_animation()
                            save_score(score, high_score)
                            playing = False
                            return
                if back_button.checkForInput((mouse_x, mouse_y)):
                    confirm_exit(screen, challmode)
                    play()  # Call the play() function
                    return
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                back_button.changeColor((mouse_x, mouse_y))

    waiting_input = False
    pattern = []
    current_step = 0
    score = 0
    high_score = get_high_score()
    playing = True

    start_ticks = pygame.time.get_ticks()

    while True:
        new_game()
        run_game()





main_menu() #DO NOT CHANGE