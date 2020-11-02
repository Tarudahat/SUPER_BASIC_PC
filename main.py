import time
import pygame
import os
import sys
import configparser
import clipboard
pygame.init()

# set display
display_info = pygame.display.Info()
screen = pygame.display.set_mode((0, 0))
icon = pygame.image.load(os.path.normpath("./assets/graphics/icon.ico"))
pygame.display.set_icon(icon)
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("SUPER BASIC")

# set up the font
font_path = os.path.normpath(
    "./assets/fonts/UbuntuMono-Regular.ttf")
font = pygame.font.Font(font_path, 25)

# set up the block graphics
block_img1 = pygame.image.load(
    os.path.normpath("./assets/graphics/block_1.png")).convert()
block_img2 = pygame.image.load(
    os.path.normpath("./assets/graphics/block_2.png")).convert()
block_img3 = pygame.image.load(
    os.path.normpath("./assets/graphics/block_3.png")).convert()
block_img4 = pygame.image.load(
    os.path.normpath("./assets/graphics/block_4.png")).convert()

# set up some vars and lists
block = 0
code_lines = 0
block_y_list = [0]
save_file_arr = []
block_zoom = [0, 0]
b_size_x = 0
b_size_y = 0
i2 = 0
active_block = 0
language_pack_sections = []
frame_count = 0
rem_time = 0
running = True
confige_arr = []
fullscreenmode = True
clock = pygame.time.Clock()
screen_resolution = pygame.display.get_surface().get_size()
sleepmode_delay = 0
sleepmode = False
search_block_results = []
search_block_results_final = []
selected_result = 0
search_block_results_y = []


prev_selected_result = 0
searching = False
inputwindow_output = ""
mouse_pos = [0.0, 0.0]


choice_array = os.listdir(os.path.normpath(
    "./language_packs"))

choice_array_path = []
for i_ in range(len(choice_array)):
    choice_array_path.append(os.path.normpath(os.path.normpath(
        "./language_packs/a")[:-1]+choice_array[i_]))

# set block lists up
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# setup Classes and functions


class Block(pygame.sprite.Sprite):
    def __init__(self, type, in_text):
        super().__init__()
        if type == 0:
            self.image = pygame.image.load(
                os.path.normpath("./assets/graphics/cursor.bmp")).convert()
        elif type == 1:
            self.image = block_img1
        elif type == 2:
            self.image = block_img2
        elif type == 3:
            self.image = block_img3
        elif type == 4:
            self.image = block_img4
        self.type = type
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.in_text = in_text
        self.image.get_size()
        self.type = type
        self.rect.x = 100
        self.rect.y = 50
        self.deleted = False

    def draw_block_text(self, block_zoom):
        if self.rect.y > -120 and self.rect.y < screen_h():
            font = pygame.font.Font(font_path, 18+int((block_zoom[0]-340)/18))
            if len(self.in_text) <= 22:
                text = font.render(
                    self.in_text, True, (0, 0, 0))
            elif len(self.in_text) > 22:
                text = font.render(
                    self.in_text[:21-int((block_zoom[0]-340)/100)]+"…", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.topleft = (
                self.rect.x+50+int((block_zoom[0]-320)/7), self.rect.y+60+int((block_zoom[0]-320)/7))
            screen.blit(text, textRect)

    def block_render(self, block_zoom):
        self.rect.w = block_zoom[0]
        self.rect.h = block_zoom[1]
        if self.rect.y > -120 and self.rect.y < screen_h():
            scaled_block = pygame.transform.scale(
                self.image, (block_zoom[0], block_zoom[1]))
            # Display block hitbox
            # pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
            screen.blit(scaled_block, self.rect)

# input button class and more


class input_():

    def __init__(self, x, y, in_text=""):
        self.in_text = in_text
        self.image = pygame.Surface([500, 70])
        self.rect = self.image.get_rect()
        self.in_use = False
        self.type_ok = True
        self.type_timer = 0.0
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        if len(self.in_text) <= 36:
            dis_text = font.render(
                self.in_text, True, (0, 0, 0))
        elif len(self.in_text) > 36:
            dis_text = font.render(
                self.in_text[len(self.in_text)-36:], True, (0, 0, 0))

        textRect = dis_text.get_rect()
        textRect.topleft = (self.rect.x+17, self.rect.y+25)

        screen.blit(dis_text, textRect)

    def work(self, event, mouse_pos):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.in_use = False
        if (pygame.mouse.get_pressed() == (1, 0, 0) and mouse_pos[0] > self.rect.x and mouse_pos[0] < self.rect.x+501 and mouse_pos[1] > self.rect.y and mouse_pos[1] < self.rect.y+71):
            self.in_use = True

        if self.in_use == True:
            if event.type == pygame.KEYDOWN and self.type_ok == True:
                if event.key == pygame.K_BACKSPACE:
                    self.in_text = self.in_text[:-1]
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.in_text += clipboard.paste()
                    time.sleep(.05)
                else:
                    self.in_text += event.unicode
                self.type_timer = time.time()
                self.type_ok = False
        if time.time() >= self.type_timer+0.12:
            self.type_ok = True

# buttons class


class button():
    def __init__(self, in_text, x_, y_):
        self.image = pygame.Surface([12*len(in_text)+40, 60])
        self.rect = self.image.get_rect()
        self.button_label = in_text
        self.rect.x = x_
        self.rect.y = y_

    def work(self, event, mouse_pos):
        button_output = False
        if (pygame.mouse.get_pressed() == (1, 0, 0) and mouse_pos[0] > self.rect.x and mouse_pos[0] < self.rect.x+12*len(self.button_label)+40 and mouse_pos[1] > self.rect.y and mouse_pos[1] < self.rect.y+61):
            button_output = True
        return(button_output)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        dis_text = font.render(self.button_label, True, (10, 10, 10))

        textRect = dis_text.get_rect()
        textRect.topleft = (self.rect.x+18, self.rect.y+18)

        screen.blit(dis_text, textRect)


# choice class
class choice_object():
    def __init__(self, x_, y_, choice_array_, choice_array_path):
        self.image = pygame.Surface([500, 60])
        self.rect = self.image.get_rect()
        self.rect.x = x_
        self.rect.y = y_
        self.selected_choice = 0
        self.choice_array_ = choice_array_
        self.choice_array_path = choice_array_path

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        dis_text = font.render(
            self.choice_array_[self.selected_choice], True, (10, 10, 10))

        textRect = dis_text.get_rect()
        textRect.topleft = (self.rect.x+18, self.rect.y+18)

        screen.blit(dis_text, textRect)

    def work(self, event, mouse_pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                if self.selected_choice >= 1:
                    self.selected_choice -= 1
                elif self.selected_choice == 0:
                    self.selected_choice = len(self.choice_array_)-1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                if self.selected_choice <= len(self.choice_array_)-2:
                    self.selected_choice += 1
                elif self.selected_choice == len(self.choice_array_)-1:
                    self.selected_choice = 0
            time.sleep(0.2)


class LanguagePack():
    def __init__(self, langpath):
        # get values from language pack
        language_pack = configparser.ConfigParser()
        language_pack_sections = language_pack.sections()
        language_pack.read(langpath, encoding="utf-8")

        self.commentsign = language_pack["Misc"]["CommentSign"]
        self.commentsignend = language_pack["Misc"]["CommentSignEnd"]

        self.OutputFileExtension = language_pack["Misc"]["OutputFileExtension"]

        if "Loop" in language_pack_sections:
            self.LoopStart = language_pack["Loop"]["LoopStart"]
            self.LoopEnd = language_pack["Loop"]["LoopEnd"]
            self.ForLoopStart = language_pack["Loop"]["ForLoopStart"]
            self.ForLoopEnd = language_pack["Loop"]["ForLoopEnd"]
            # set the loop stuff up

        if "If" in language_pack_sections:
            self.IfStart = language_pack["If"]["IfStart"]
            self.IfEnd = language_pack["If"]["IfEnd"]
            self.ElseIfStart = language_pack["If"]["IfEnd"]
            self.ElseIfEnd = language_pack["If"]["ElseIfEnd"]
            # set the if stuff up


def draw_emptywindow(text):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(font_path, 25)
    emptywindow_image = pygame.Surface([850, 450])
    screen_part = int(screen_w()/2-425)
    emptywindow_rect = emptywindow_image.get_rect()
    emptywindow_rect.x = 0+screen_part
    emptywindow_rect.y = 70
    pygame.draw.rect(screen, (0, 0, 0), emptywindow_rect, 5)
    dis_text = font.render(text, True, (10, 10, 10))

    textRect = dis_text.get_rect()
    textRect.topleft = (emptywindow_rect.x+21, emptywindow_rect.y+17)
    emptywindow_image.fill((255, 255, 255))
    screen.blit(dis_text, textRect)
    font = pygame.font.Font(font_path, 20)


def save_file_func(text):
    save_file = open(text+langpack.OutputFileExtension, "a")
    try:
        i2 = 0
        for block in block_list_arr:
            block_y_list.append(block.rect.y)
            i2 += 1
        block_y_list.sort()
        i2 = 0
        while i2 < len(block_list_arr)+1:
            for block in block_list_arr:
                if block_y_list[i2] == block.rect.y:
                    if block.deleted == False:
                        save_file_arr.append(block.in_text)
            i2 += 1

        for line in save_file_arr:
            save_file.write("".join(line) + "\n")
        print("successfully saved")
    except:
        print("saving failed")


def zoom(text_):
    if text_ == "in" and block_zoom[0] < 502 and block_zoom[1] < 172:
        block_zoom[0] += 16
        block_zoom[1] += 6
    elif text_ == "out" and block_zoom[0] > 275 and block_zoom[1] > 112:
        block_zoom[0] -= 16
        block_zoom[1] -= 6


def scroll(text_):
    try:
        if text_ == "up":
            for block in block_list_arr:
                block.rect.y += 15
        elif text_ == "down":
            for block in block_list_arr:
                block.rect.y -= 15
    except:
        pass


def search(text_):
    search_block_results.clear()
    search_block_results_final.clear()
    search_block_results_y.clear()
    for block in block_list_arr:
        if text_ in block.in_text and block.deleted == False:
            search_block_results.append(block)

    i2 = 0
    for block in search_block_results:
        search_block_results_y.append(block.rect.y)
        i2 += 1
    search_block_results_y.sort()
    i2 = 0
    while i2 < len(search_block_results):
        for block in search_block_results:
            if search_block_results_y[i2] == block.rect.y:
                if block.deleted == False:
                    search_block_results_final.append(block)
        i2 += 1

    print(len(search_block_results_final))

    if len(search_block_results_final) > 0:
        searching = True
    else:
        searching = False

    global prev_selected_result
    prev_selected_result = -5

    return searching


def setblock(type, text):
    if text[0:len(langpack.commentsign)] == langpack.commentsign:
        print(text[len(text)-len(langpack.commentsignend):len(text)])
        print(langpack.commentsignend)
        if text[len(text)-len(langpack.commentsignend):len(text)] == langpack.commentsignend:
            type = 2
        elif langpack.commentsignend == "¤":
            type = 2
    block = Block(type, text)
    block_list.add(block)
    all_sprites_list.add(block)


def deleteblock(block_):
    block_.deleted = True


def inputwindow(event, mouse_pos, text):
    done = False
    screen_part = int(screen_w()/2-425)
    in_win = input_(175+screen_part, 250)
    confirm_button = button("Done", 685+screen_part, 420)
    cancel_button = button("Cancel", 70+screen_part, 420)
    while not done:
        draw_emptywindow(text)
        mouse_pos = pygame.mouse.get_pos()
        in_win.work(event, mouse_pos)
        in_win.draw()
        confirm_button.draw()
        cancel_button.draw()

        if confirm_button.work(event, mouse_pos) == True:
            done = True
        elif cancel_button.work(event, mouse_pos) == True:
            done = True
            in_win.in_text = "¤cancelled"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True

        pygame.display.flip()
    return in_win.in_text


def choice_window(event, mouse_pos, text, choice_array_, choice_array_path_):
    done = False
    screen_part = int(screen_w()/2-425)
    ch_win = choice_object(175+screen_part, 250,
                           choice_array_, choice_array_path_)
    confirm_button = button("Done", 685+screen_part, 420)
    cancel_button = button("Cancel", 70+screen_part, 420)
    while not done:
        draw_emptywindow(text)
        mouse_pos = pygame.mouse.get_pos()
        ch_win.work(event, mouse_pos)
        ch_win.draw()
        confirm_button.draw()
        cancel_button.draw()

        if confirm_button.work(event, mouse_pos) == True:
            done = True
        elif cancel_button.work(event, mouse_pos) == True:
            done = True
            return "¤cancelled"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True

        pygame.display.flip()
    return_text = ch_win.choice_array_path[ch_win.selected_choice]
    time.sleep(0.25)
    return return_text


def screen_w():
    screenw, screenh = pygame.display.get_surface().get_size()
    return screenw


def screen_h():
    screenw, screenh = pygame.display.get_surface().get_size()
    return screenh


# set up cursor
cursor = Block(0, "¤")
all_sprites_list.add(cursor)

# set up GUI
add_block_button = button("add block", 10, 10)
save_button = button("save", 170, 10)
search_button = button("search", 170, 80)
language_button = button("language ", 10, 80)

langpack = LanguagePack(os.path.normpath("./language_packs/python"))


while running:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # -=-Get input-=-

    for event in pygame.event.get():
        sleepmode_delay = 0
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if fullscreenmode == True:
                    pygame.display.set_mode((screen_w()-150, screen_h()-100))
                    fullscreenmode = False
                elif fullscreenmode == False:
                    pygame.display.set_mode(
                        screen_resolution, pygame.FULLSCREEN)
                    fullscreenmode = True
                    time.sleep(0.25)
            elif (event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS) and pygame.key.get_mods() & pygame.KMOD_CTRL:
                zoom("in")
                time.sleep(0.25)
            elif (event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS) and pygame.key.get_mods() & pygame.KMOD_CTRL:
                zoom("out")
                time.sleep(0.25)
            if searching == True:
                if event.key == pygame.K_UP and selected_result > 0:
                    selected_result -= 1
                elif event.key == pygame.K_DOWN and selected_result < len(search_block_results_final)-1:
                    selected_result += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scroll("up")
            elif event.button == 5:
                scroll("down")
    # -=-=-=-=-=-=-=-

    if searching == True:

        if selected_result != prev_selected_result:

            while search_block_results_final[selected_result].rect.y > 35 or search_block_results_final[selected_result].rect.y < 20:
                if search_block_results_final[selected_result].rect.y > 30:
                    scroll("down")
                elif search_block_results_final[selected_result].rect.y < 40:
                    scroll("up")

        prev_selected_result = selected_result

        if pygame.mouse.get_pressed() == (1, 0, 0):
            selected_result = 0
            search_block_results_final.clear()
            search_block_results.clear()
            searching = False

    mouse_pos = pygame.mouse.get_pos()
    cursor.rect.x = int(mouse_pos[0])
    cursor.rect.y = int(mouse_pos[1])

    blocks_hit_list = pygame.sprite.spritecollide(cursor, block_list, False)

    for block in blocks_hit_list:
        if block.deleted == False:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                if block == active_block:
                    block.rect.x = int(mouse_pos[0]-150)
                    block.rect.y = int(mouse_pos[1]-70)
                active_block = block
            if pygame.key.get_pressed()[pygame.K_DELETE]:
                deleteblock(block)
                time.sleep(0.1)

    try:
        for block in block_list_arr:
            # block rendering
            if block_zoom[0] == 0:
                b_size_x, b_size_y = block.image.get_size()
                block_zoom = [b_size_x, b_size_y]
            if block.deleted == False:
                block.block_render(block_zoom)
            # text rendering
            if block.deleted == False:
                block.draw_block_text(block_zoom)
            # connect blocks
            if block.deleted == False:
                if (pygame.mouse.get_pressed() == (1, 0, 0)) and active_block.type != 2 and block.type != 2:
                    if active_block.rect.x > block.rect.x-20 and active_block.rect.y > block.rect.y-30+block_zoom[1] and active_block.rect.x < block.rect.x+block_zoom[0]-15 and active_block.rect.y < block.rect.y+block_zoom[1]+20:
                        active_block.rect.x = block.rect.x
                        active_block.rect.y = block.rect.y + \
                            block_zoom[1]-128+115
                    elif active_block.rect.x > block.rect.x-20 and active_block.rect.y > block.rect.y-150 and active_block.rect.x < block.rect.x+block_zoom[0]-15 and active_block.rect.y < block.rect.y-30:
                        active_block.rect.x = block.rect.x
                        active_block.rect.y = block.rect.y-block_zoom[1]+13
    except:
        pass

    add_block_button.draw()
    save_button.draw()
    search_button.draw()
    language_button.draw()

    if add_block_button.work(event, mouse_pos) == True:
        inputwindow_output = inputwindow(
            event, mouse_pos, "Please enter code:")
        print(inputwindow_output)
        if inputwindow_output != "¤cancelled":
            setblock(1, inputwindow_output)
            time.sleep(0.25)
            block_list_arr = pygame.sprite.Group.sprites(block_list)

    if save_button.work(event, mouse_pos) == True:
        inputwindow_output = inputwindow(
            event, mouse_pos, "Please enter a name to save the file with:")
        print(inputwindow_output)
        if inputwindow_output != "¤cancelled":
            save_file_func(inputwindow_output)
            time.sleep(0.25)

    if search_button.work(event, mouse_pos) == True:
        inputwindow_output = inputwindow(
            event, mouse_pos, "What should be searched for?:")
        print(inputwindow_output)

        if inputwindow_output != "¤cancelled":
            searching = search(inputwindow_output)
            time.sleep(0.25)

    if language_button.work(event, mouse_pos) == True:
        inputwindow_output = choice_window(
            event, mouse_pos, "Please choose a language pack:", choice_array, choice_array_path)
        print(inputwindow_output)

        if inputwindow_output != "¤cancelled":
            rusure = choice_window(
                event, mouse_pos, "Warning:", ["Unsaved progres will be lost"], [""])
            print(rusure)
            if rusure != "¤cancelled":
                langpack = LanguagePack(inputwindow_output)

    # fps counter
    if int(time.time()) > int(rem_time):
        print("Fps:", frame_count)
        frame_count = 0
    frame_count += 1
    rem_time = time.time()

    pygame.display.flip()

    # sleep mode
    sleepmode_delay += 1
    if sleepmode_delay >= 300:  # 300 -> 5s
        sleepmode = True

    while sleepmode:
        clock.tick(5)
        for event in pygame.event.get():
            sleepmode = False
            sleepmode_delay = 0

sys.exit(0)
