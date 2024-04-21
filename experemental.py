import json
import pygame
import sys
import os
import survey
from random import randint
pygame.init()

current_sprite = 0
answer_rects = []


floor = 1
infoObject = pygame.display.Info()
xx = infoObject.current_w
yy = infoObject.current_h
fps = 100
fps_tick = 1000/fps
fps_tick0 = 0
screen = pygame.display.set_mode((xx, yy), pygame.FULLSCREEN)
file = open('data.json', 'r')
data = json.loads(file.read())
file.close()
shift = 20 

backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
backdround_image_rect = backdround_image.get_rect()

arrow_up = pygame.image.load("images/arrow_up.png")
arrow_up = pygame.transform.scale(arrow_up, (arrow_up.get_size()[0]//6, arrow_up.get_size()[1]//6))
arrow_rect = arrow_up.get_rect()

arrow_down = pygame.image.load("images/arrow_down.png")
arrow_down = pygame.transform.scale(arrow_down, (arrow_down.get_size()[0]//6, arrow_down.get_size()[1]//6))

coke = pygame.image.load("images/coke.png")
coke = pygame.transform.scale(coke, (coke.get_size()[0]//4.5, coke.get_size()[1]//4.5))
coke_rect = coke.get_rect()

heart = pygame.image.load("images/heart.png")
heart = pygame.transform.scale(heart, (heart.get_size()[0]//12, heart.get_size()[1]//12))
heart_rect = heart.get_rect()

bag = pygame.image.load("images/bag.png")
bag = pygame.transform.scale(bag, (bag.get_size()[0]//1, bag.get_size()[1]//1))
bag_rect = bag.get_rect(topleft = (-150 + shift, -270 + shift//2))

character_size = 2
npc_list0 = os.listdir("images/npc")
npc_list = []
player_animation = [1, 1, 0, 1000]
for i in npc_list0:
    if i[0].isdigit():
        npc_list.append(i)
npc_images = []
for i in npc_list:
    list0 = []
    for j in range(1, 5):
        list1 = []
        for k in range(1, 5):
            image0 = pygame.image.load("images/npc/" + str(i) + "/" + str(j) + "/" + str(k) + ".PNG")
            image0 = pygame.transform.scale(image0, (image0.get_size()[0]//character_size, image0.get_size()[1]//character_size))
            list1.append(image0)
        list0.append(list1)
    npc_images.append(list0)

for i in range(len(data[str(floor) + "-floor"]["npc"])):
    data[str(floor) + "-floor"]["npc"][i][2] = randint(1, len(npc_images))

for i in range(1, 5):
    blocks_j = 0
    blocks_num = len(data[str(i) + "-floor"]["blocks"])
    while blocks_j < blocks_num:
        if data[str(i) + "-floor"]["blocks"][ blocks_j][2] < 1 or data[str(i) + "-floor"]["blocks"][ blocks_j][3] < 1:
            del data[str(i) + "-floor"]["blocks"][ blocks_j]
            blocks_num-=1
        else:
            blocks_j+=1


level = 1
lifes = 3
level_1_timer = 120000
level_2_timer = 100000
level_3_timer = 80000
level_4_timer = 60000
target_room = data[str(level) + "-floor"]["rooms"][randint(0, len(data[str(level) + "-floor"]["rooms"])-1)][0]
timer = level_1_timer
darken_surface = pygame.Surface((xx, yy))
darken = True
darken_time = 500
darken_coef = 255//(darken_time//10)
darken_num = 255
font_36 = pygame.font.Font("PIXY.ttf", 36)
font = pygame.font.Font("PIXY.ttf", 20)
x_map = backdround_image.get_size()[0]
y_map = backdround_image.get_size()[1]
x = 6004.592527820984 
y = 9488.892630683886
x_plus_move = False
x_minus_move = False
y_plus_move = False
y_minus_move = False
x_ac = 0
y_ac = 0
ac_slow = 0.7
ac_speed = 0.5
speed0 = 6
speed = speed0
player_size = 30
mode = 0
x_mode_1 = int()
y_mode_1 = int()
x_mode_2 = int()
y_mode_2 = int()
mouse_hold = False
coke_time = 0
win_sound = pygame.mixer.Sound("sounds/win.mp3")
loss_sound = pygame.mixer.Sound("sounds/loss.mp3")
main_game_sound = pygame.mixer.Sound("sounds/main_game.mp3")
ough_sound = pygame.mixer.Sound("sounds/ough.mp3")
coke_sound = pygame.mixer.Sound("sounds/coke.mp3")
speak_sound = pygame.mixer.Sound("sounds/speak.mp3")


def pause(data, xx, yy, pause_mode):
    pause_sound = pygame.mixer.Sound("sounds/pause.mp3")
    pause_sound.play(-1)
    font = pygame.font.Font("PIXY.ttf", 120)
    backdround = pygame.image.load("images/menu_background.jpg")
    backdround = pygame.transform.scale(backdround, (backdround.get_size()[0]*yy//backdround.get_size()[1], yy))
    backdround_rect = backdround.get_rect(center = (xx//2, yy//2))
    darken_surface = pygame.Surface((xx, yy))
    darken = True
    darken_time = 500
    darken_coef = 255//(darken_time//10)
    darken_num = 255
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for j in range(1, 5):
                    for i in range(len(data[str(j) + "-floor"]["cokes"])):
                        data[str(j) + "-floor"]["cokes"][i][2] = True
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                text = font.render("Quit", True, (255, 255, 255))
                if event.button == 1:
                    if xx//2 + text.get_size()[0]//2 >= pygame.mouse.get_pos()[0] >= xx//2 - text.get_size()[0]//2 and yy//4*3 + text.get_size()[1]//2 >= pygame.mouse.get_pos()[1] >= yy//4*3 - text.get_size()[1]//2:
                        for j in range(1, 5):
                            for i in range(len(data[str(j) + "-floor"]["cokes"])):
                                data[str(j) + "-floor"]["cokes"][i][2] = True
                            with open("data.json", "w") as file:
                                json.dump(data, file, indent=4)
                        exit()
                    if pause_mode == 1:
                        text = font.render("Resume", True, (255, 255, 255))
                    elif pause_mode == 2:
                        text = font.render("Next level", True, (255, 255, 255))
                    elif pause_mode == 3:
                        text = font.render("Restart level", True, (255, 255, 255))
                    elif pause_mode == 4:
                        text = font.render("New game", True, (255, 255, 255))
                    if xx//2 + text.get_size()[0]//2 >= pygame.mouse.get_pos()[0] >= xx//2 - text.get_size()[0]//2 and yy//4*2 + text.get_size()[1]//2 >= pygame.mouse.get_pos()[1] >= yy//4*2 - text.get_size()[1]//2:
                        pygame.mixer.stop()
                        return

        if darken:
            if darken_num-darken_coef >= 0:
                darken_num-=darken_coef
            else:
                darken_num = 255
                darken = False

        darken_surface.set_alpha(darken_num)
        darken_surface.fill((0, 0, 0))

        screen.fill((0, 0, 0))
        screen.blit(backdround, backdround_rect)
        text = font.render("Don't be late!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(xx//2, yy//4))
        pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
        screen.blit(text, text_rect)
        if pause_mode == 1:
            text = font.render("Resume", True, (255, 255, 255))
        elif pause_mode == 2:
            text = font.render("Next level", True, (255, 255, 255))
        elif pause_mode == 3:
            text = font.render("Restart level", True, (255, 255, 255))
        elif pause_mode == 4:
            text = font.render("New game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(xx//2, yy//4*2))
        pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
        screen.blit(text, text_rect)
        text = font.render("Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(xx//2, yy//4*3))
        pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
        screen.blit(text, text_rect)
        if darken:
            screen.blit(darken_surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(10)

def transition(xx, yy, position, room, time):
    transition_time = 3000
    if position == 1:
        transition_time = 1500
    transition_time_tick = 0
    font = pygame.font.Font("PIXY.ttf", 60)
    backdround = pygame.image.load("images/kbtu_room.jpg")
    backdround = pygame.transform.scale(backdround, (backdround.get_size()[0]*yy//backdround.get_size()[1], yy))
    backdround_rect = backdround.get_rect(center = (xx//2, yy//2))
    teacher = pygame.image.load("images/teacher.png")
    teacher = pygame.transform.scale(teacher, (teacher.get_size()[0]*1.5, teacher.get_size()[1]*1.5))
    teacher_rect = teacher.get_rect(center = (xx//2, yy - teacher.get_size()[1]//2))
    darken_surface = pygame.Surface((xx, yy))
    darken = True
    darken_time = 500
    darken_coef = 255//(darken_time//10)
    darken_num = 255
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for j in range(1, 5):
                    for i in range(len(data[str(j) + "-floor"]["cokes"])):
                        data[str(j) + "-floor"]["cokes"][i][2] = True
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                exit()
        if darken:
            if darken_num-darken_coef >= 0:
                darken_num-=darken_coef
            else:
                darken_num = 255
                darken = False

        darken_surface.set_alpha(darken_num)
        darken_surface.fill((0, 0, 0))

        screen.fill((0, 0, 0))
        screen.blit(backdround, backdround_rect)
        if position == 1:
            text = font.render("Don't be late!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(xx//2, 200))
            pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
            screen.blit(text, text_rect)
            text = font.render("The lesson will be in room " + str(room) + " in " + str(round(time/1000)) + " seconds", True, (255, 255, 255))
            text_rect = text.get_rect(center=(xx//2, 100))
            pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
        elif position == 2:
            text = font.render("Don't be late anymore!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(xx//2, 200))
            pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
            screen.blit(text, text_rect)
        elif position == 3:
            text = font.render("Good job!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(xx//2, 200))
            pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
            screen.blit(text, text_rect)
        elif position == 4:
            text = font.render("Go for a retake!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(xx//2, 200))
            pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
            screen.blit(text, text_rect)
        elif position == 5:
            text = font.render("Your GPA is 4.0!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(xx//2, 200))
            pygame.draw.rect(screen, (40, 40, 40), text_rect, border_radius = 40)
            screen.blit(text, text_rect)
        screen.blit(text, text_rect)
        screen.blit(teacher, teacher_rect)

        if transition_time_tick < transition_time:
            transition_time_tick+=10
        else:
            return

        if darken:
            screen.blit(darken_surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(10)

pause(data, xx, yy, 4)
speak_sound.play()
transition(xx, yy, 1, target_room, timer)
main_game_sound.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for j in range(1, 5):
                for i in range(len(data[str(j) + "-floor"]["cokes"])):
                    data[str(j) + "-floor"]["cokes"][i][2] = True
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                x_plus_move = True
            elif event.key == pygame.K_a:
                x_minus_move = True
            elif event.key == pygame.K_w:
                y_minus_move = True
            elif event.key == pygame.K_s:
                y_plus_move = True
            elif event.key == pygame.K_e:
                if mode == 0:
                    mode = 1
                    speed = 30
                else:
                    mode = 0
                    speed = speed0
            elif event.key == pygame.K_q:
                if mode == 1:
                    for i in range(len(data[str(floor) + "-floor"]["blocks"])):
                        block = data[str(floor) + "-floor"]["blocks"][i]
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if block[0] <= mouse_x + x - xx//2 <= block[0] + block[2] and block[1] <= mouse_y + y - yy//2 <= block[1] + block[3]:
                            del data[str(floor) + "-floor"]["blocks"][i]
                            break
                    for i in range(len(data[str(floor) + "-floor"]["npc"])):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if (((data[str(floor) + "-floor"]["npc"][i][0]) - mouse_x - x + xx//2)**2 + ((data[str(floor) + "-floor"]["npc"][i][1]) - mouse_y - y +yy//2)**2)**(1/2) <= 40:
                            del data[str(floor) + "-floor"]["npc"][i]
                            break
                    for i in range(len(data[str(floor) + "-floor"]["rooms"])):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if (((data[str(floor) + "-floor"]["rooms"][i][1]) - mouse_x - x + xx//2)**2 + ((data[str(floor) + "-floor"]["rooms"][i][2]) - mouse_y - y +yy//2)**2)**(1/2) <= 50:
                            del data[str(floor) + "-floor"]["rooms"][i]
                            break
                    for i in range(len(data[str(floor) + "-floor"]["stairs"])):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if (((data[str(floor) + "-floor"]["stairs"][i][0]) - mouse_x - x + xx//2)**2 + ((data[str(floor) + "-floor"]["stairs"][i][1]) - mouse_y - y +yy//2)**2)**(1/2) <= 50:
                            del data[str(floor) + "-floor"]["stairs"][i]
                            break
                    for i in range(len(data[str(floor) + "-floor"]["cokes"])):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if (((data[str(floor) + "-floor"]["cokes"][i][0]) - mouse_x - x + xx//2)**2 + ((data[str(floor) + "-floor"]["cokes"][i][1]) - mouse_y - y +yy//2)**2)**(1/2) <= 40:
                            del data[str(floor) + "-floor"]["cokes"][i]
                            break
            elif event.key == pygame.K_p:
                if mode == 1:
                    #data["1-floor"]["npc"].clear()
                    None
            elif event.key == pygame.K_r or event.key == pygame.K_t or event.key == pygame.K_y or event.key == pygame.K_u:
                if mode == 1:
                    direction = 1
                    if event.key == pygame.K_t:
                        direction = 2
                    elif event.key == pygame.K_y:
                        direction = 3
                    elif event.key == pygame.K_u:
                        direction = 4
                    data[str(floor) + "-floor"]["npc"].append([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, randint(1, len(npc_images)), direction, 1, randint(0, 1000), 1000, False, 0, 2000])
                    #print([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, randint(1, len(npc_images)), 1, 1])
            elif event.key == pygame.K_c:
                if mode == 1:
                    print("Write number: ")
                    room = int(input())
                    data[str(floor) + "-floor"]["rooms"].append([room, pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2])
            elif event.key == pygame.K_v:
                if mode == 1:
                    data[str(floor) + "-floor"]["stairs"].append([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, 0, 0, 1])
            elif event.key == pygame.K_b:
                if mode == 1:
                    data[str(floor) + "-floor"]["cokes"].append([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, True])
            elif event.key == pygame.K_x:
                if mode == 1:
                    print(pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2)
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.stop()
                pause(data, xx, yy, 1)
                main_game_sound.play(-1)
                darken = True
                x_plus_move = False
                x_minus_move = False
                y_plus_move = False
                y_minus_move = False 
            elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4:
                if mode == 1:
                    floor_num = 1
                    if event.key == pygame.K_2:
                        floor_num = 2
                    elif event.key == pygame.K_3:
                        floor_num = 3
                    elif event.key == pygame.K_4:
                        floor_num = 4
                    floor = floor_num
                    backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
                    backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
                    backdround_image_rect = backdround_image.get_rect() 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                x_plus_move = False
            elif event.key == pygame.K_a:
                x_minus_move = False
            elif event.key == pygame.K_w:
                y_minus_move = False
            elif event.key == pygame.K_s:
                y_plus_move = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mode == 1:
                    x_mode_1, y_mode_1 = pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2
                    mouse_hold = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if mode == 1:
                    data[str(floor) + "-floor"]["blocks"].append([min(x_mode_1, x_mode_2), min(y_mode_1, y_mode_2), abs(x_mode_1 - x_mode_2), abs(y_mode_1 - y_mode_2)])
                    mouse_hold = False
    x_mode_2, y_mode_2 = pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2


    if x_plus_move:
        if x_ac <= speed:
            x_ac+=ac_speed
        else:
            x_ac = speed
    elif x_minus_move:
        if x_ac >= -speed:
            x_ac-=ac_speed
        else:
            x_ac = -speed
    else:
        if x_ac*ac_slow >= 0.1:
            x_ac*=ac_slow
        else:
            x_ac = 0
    if y_plus_move:
        if y_ac <= speed:
            y_ac+=ac_speed
        else:
            y_ac = speed
    elif y_minus_move:
        if y_ac >= -speed:
            y_ac-=ac_speed
        else:
            y_ac = -speed
    else:
        if y_ac*ac_slow >= 0.1:
            y_ac*=ac_slow
        else:
            y_ac = 0

    x_plus = True
    y_plus = True

    if mode != 1:
        if timer > 0:
            timer-=13
        else:
            pygame.mixer.stop()
            loss_sound.play()
            if lifes-1 != 0:
                transition(xx, yy, 2, target_room, timer)
                pause(data, xx, yy, 3)
                lifes-=1
            else:
                transition(xx, yy, 4, target_room, timer)
                pause(data, xx, yy, 4)
                level = 1
                lifes = 3
            darken = True
            floor = 1
            speed = speed0
            backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
            backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
            backdround_image_rect = backdround_image.get_rect()
            coke_time = 0
            for j in range(1, 5):
                for i in range(len(data[str(j) + "-floor"]["cokes"])):
                    data[str(j) + "-floor"]["cokes"][i][2] = True
            target_room = data[str(level) + "-floor"]["rooms"][randint(0, len(data[str(level) + "-floor"]["rooms"])-1)][0]
            timer = level_1_timer
            if level == 2:
                timer = level_2_timer
            elif level == 3:
                timer = level_3_timer
            elif level == 4:
                timer = level_4_timer
            speak_sound.play()
            transition(xx, yy, 1, target_room, timer)
            main_game_sound.play(-1)
            x = 6004.592527820984 
            y = 9488.892630683886
            x_plus_move = False
            x_minus_move = False
            y_plus_move = False
            y_minus_move = False 


    if player_animation[2] >= player_animation[3]:
        if y_ac < 0:
            if player_animation[0] != 2:
                player_animation[0] = 2
                player_animation[1] = 2
            else:
                if player_animation[1] != 2:
                    player_animation[1] = 2
                else:
                    player_animation[1] = 3
        elif y_ac > 0:
            if player_animation[0] != 1:
                player_animation[0] = 1
                player_animation[1] = 2
            else:
                if player_animation[1] != 2:
                    player_animation[1] = 2
                else:
                    player_animation[1] = 3
        elif x_ac < 0: 
            if player_animation[0] != 3:
                player_animation[0] = 3
                player_animation[1] = 1
            else:
                if player_animation[1] != 3 and player_animation[1]+1 <= 3:
                    player_animation[1] +=1
                else:
                    player_animation[1] = 1
        elif x_ac > 0: 
            if player_animation[0] != 4:
                player_animation[0] = 4
                player_animation[1] = 1
            else:
                if player_animation[1] != 3 and player_animation[1]+1 <= 3:
                    player_animation[1] +=1
                else:
                    player_animation[1] = 1
        elif player_animation[1] != 4:
            player_animation[1] = 4
        else:
            player_animation[1] = 1 
        player_animation[2] = 0        
    elif x_ac or y_ac:
        player_animation[2] += 80
    else:
        if player_animation[1] != 4:
            player_animation[2] += 6
        else:
            player_animation[2] +=160
    
    if coke_time:
            if coke_time-10 > 0:
                coke_time-=13
            else:
                coke_time = 0
                speed = speed0

    if mode != 1:
        for i in data[str(floor) + "-floor"]["blocks"]:
            x_prev = x
            y_prev = y + y_ac
            if y_prev + player_size > i[1] and y_prev - player_size < i[1] + i[3] and x_prev + player_size > i[0] and x_prev - player_size < i[0] + i[2]:
                y_plus = False
            x_prev = x + x_ac
            y_prev = y
            if y_prev + player_size > i[1] and y_prev - player_size < i[1] + i[3] and x_prev + player_size > i[0] and x_prev - player_size < i[0] + i[2]:
                x_plus = False
    
        for i in range(len(data[str(floor) + "-floor"]["npc"])):
            if ((x - (data[str(floor) + "-floor"]["npc"][i][0]))**2 + (y - (data[str(floor) + "-floor"]["npc"][i][1]))**2)**(1/2) <= 40:
                x_ac*=-1
                y_ac*=-1
                ough_sound.play()
                data[str(floor) + "-floor"]["npc"][i][7] = True
                data[str(floor) + "-floor"]["npc"][i][8] = 0

        for i in data[str(floor) + "-floor"]["stairs"]:
            if ((i[0] - x)**2 + (i[1] - y)**2)**(1/2) <= 50:
                darken = True
                floor+=i[4]
                backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
                backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
                backdround_image_rect = backdround_image.get_rect() 
                x = i[2]
                y = i[3]

        for i in range(len(data[str(floor) + "-floor"]["cokes"])):
            if ((x - (data[str(floor) + "-floor"]["cokes"][i][0]))**2 + (y - (data[str(floor) + "-floor"]["cokes"][i][1]))**2)**(1/2) <= 40 and data[str(floor) + "-floor"]["cokes"][i][2]:
                speed = 11
                coke_time += 10000
                data[str(floor) + "-floor"]["cokes"][i][2] = False
                coke_sound.play()
        
        for i in data[str(floor) + "-floor"]["rooms"]:
            if ((i[1] - x)**2 + (i[2] - y)**2)**(1/2) <= 50 and i[0] == target_room:
                pygame.mixer.stop()
                win_sound.play()
                if level+1 == 3:
                    survey.survey_game(screen)
                if level+1 <= 4:
                    transition(xx, yy, 3, target_room, timer)
                    pause(data, xx, yy, 2)
                    level+=1
                else:
                    transition(xx, yy, 5, target_room, timer)
                    pause(data, xx, yy, 4)
                    level = 1
                    lifes = 3
                darken = True
                floor = 1
                speed = speed0
                backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
                backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
                backdround_image_rect = backdround_image.get_rect()
                for j in range(1, 5):
                    for i in range(len(data[str(j) + "-floor"]["cokes"])):
                        data[str(j) + "-floor"]["cokes"][i][2] = True
                target_room = data[str(level) + "-floor"]["rooms"][randint(0, len(data[str(level) + "-floor"]["rooms"])-1)][0]
                timer = level_1_timer
                coke_time = 0
                if level == 2:
                    timer = level_2_timer
                elif level == 3:
                    timer = level_3_timer
                elif level == 4:
                    timer = level_4_timer
                speak_sound.play()
                transition(xx, yy, 1, target_room, timer)
                main_game_sound.play(-1)
                x = 6004.592527820984 
                y = 9488.892630683886
                x_plus_move = False
                x_minus_move = False
                y_plus_move = False
                y_minus_move = False    

    if darken:
        if darken_num-darken_coef >= 0:
            darken_num-=darken_coef
        else:
            darken_num = 255
            darken = False

    darken_surface.set_alpha(darken_num)
    darken_surface.fill((0, 0, 0))

    for i in range(len(data[str(floor) + "-floor"]["npc"])):
        if data[str(floor) + "-floor"]["npc"][i][8] < data[str(floor) + "-floor"]["npc"][i][9] and data[str(floor) + "-floor"]["npc"][i][7]:
            data[str(floor) + "-floor"]["npc"][i][8]+=10
        else:
            data[str(floor) + "-floor"]["npc"][i][8] = 0
            data[str(floor) + "-floor"]["npc"][i][7] = False

        if data[str(floor) + "-floor"]["npc"][i][5] >= data[str(floor) + "-floor"]["npc"][i][6]:
            if data[str(floor) + "-floor"]["npc"][i][4] == 1:
                data[str(floor) + "-floor"]["npc"][i][4] = 4
            else:
                data[str(floor) + "-floor"]["npc"][i][4] = 1
            data[str(floor) + "-floor"]["npc"][i][5] = 0
            
        else:
            if data[str(floor) + "-floor"]["npc"][i][4] != 4:
                data[str(floor) + "-floor"]["npc"][i][5] += 6
            else:
                data[str(floor) + "-floor"]["npc"][i][5] += 180

    if x_plus and y_plus and x_ac and y_ac:
        x+=x_ac/(2**(1/2))
        y+=y_ac/(2**(1/2))
    else:
        if x_plus:
            x+=x_ac
        if y_plus:
            y+=y_ac
    if fps_tick0 >= fps_tick:
        screen.fill((0, 0, 0))
        backdround_image_rect[0] = xx//2 - x
        backdround_image_rect[1] = yy//2 - y
        screen.blit(backdround_image, backdround_image_rect)
        if mode == 1:
            for i in data[str(floor) + "-floor"]["stairs"]:
                pygame.draw.circle(screen, (255, 255, 0), (i[0]  - x + xx//2, i[1] - y + yy//2), 50)
            for i in data[str(floor) + "-floor"]["rooms"]:
                text = font_36.render(str(i[0]), True, (255, 0 , 0))
                text_rect = text.get_rect(center=(i[1]  - x + xx//2, i[2] - y + yy//2))
                pygame.draw.circle(screen, (0, 255, 0), (i[1]  - x + xx//2, i[2] - y + yy//2), 50)
                screen.blit(text, text_rect)
            for i in data[str(floor) + "-floor"]["blocks"]:
                pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(i[0] - x + xx//2, i[1] - y + yy//2, i[2], i[3]))
            for i in data[str(floor) + "-floor"]["npc"]:
                pygame.draw.circle(screen, (0, 255, 0), ((i[0]) - x + xx//2, (i[1]) - y + yy//2), 40)
            for i in data[str(floor) + "-floor"]["cokes"]:
                pygame.draw.circle(screen, (0, 255, 0), ((i[0]) - x + xx//2, (i[1]) - y + yy//2), 40)
            #screen.blit(npc_images[0][i[8][0]-1][i[8][1]-1], npc_rect)
            if mouse_hold:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(min(x_mode_1, x_mode_2) - x + xx//2, min(y_mode_1, y_mode_2) - y + yy//2, abs(x_mode_1 - x_mode_2), abs(y_mode_1 - y_mode_2)))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(xx//2 - player_size, yy//2 - player_size, 2*player_size+1, 2*player_size+1))
        for i in data[str(floor) + "-floor"]["npc"]:
            if x + xx//2 + 200 >= i[0] >= x - xx//2 - 200 and y + yy//2 + 200 >= i[1] >= y - yy//2 - 200:
                npc_rect = npc_images[i[2]-1][i[3]-1][i[4]-1].get_rect()
                npc_rect.center = (i[0] - x + xx//2, i[1] - y + yy//2)
                screen.blit(npc_images[i[2]-1][i[3]-1][i[4]-1], npc_rect)
                if i[7] == True:
                    text = font.render("Watch where you're going!", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(i[0]  - x + xx//2, i[1] - y + yy//2 - 70))
                    pygame.draw.rect(screen, (40, 40, 40), text_rect)
                    screen.blit(text, text_rect)
        for i in data[str(floor) + "-floor"]["stairs"]:
            if x + xx//2 + 200 >= i[0] >= x - xx//2 - 200 and y + yy//2 + 200 >= i[1] >= y - yy//2 - 200:
                arrow_rect.center = (i[0] - x + xx//2, i[1] - y + yy//2)
                if i[4] != -1:
                    screen.blit(arrow_up, arrow_rect)
                else:
                    screen.blit(arrow_down, arrow_rect)
        for i in data[str(floor) + "-floor"]["cokes"]:
            if x + xx//2 + 200 >= i[0] >= x - xx//2 - 200 and y + yy//2 + 200 >= i[1] >= y - yy//2 - 200 and i[2]:
                coke_rect.center = (i[0] - x + xx//2, i[1] - y + yy//2)
                screen.blit(coke, coke_rect)
        player_rect = npc_images[0][player_animation[0]-1][player_animation[1]-1].get_rect()
        player_rect.center = (xx//2, yy//2)
        screen.blit(npc_images[2][player_animation[0]-1][player_animation[1]-1], player_rect)
        screen.blit(bag, bag_rect)

        text = font_36.render("Target room: " + str(target_room), True, (0, 0, 0))
        text_rect = text.get_rect(center=(text.get_size()[0]//2  + shift, text.get_size()[1]//2  + shift//2))
        #pygame.draw.rect(screen, (40, 40, 40), text_rect)
        screen.blit(text, text_rect)

        text = font_36.render("Current floor: " + str(floor), True, (0, 0, 0))
        text_rect = text.get_rect(center=(text.get_size()[0]//2  + shift, text.get_size()[1] + text.get_size()[1]//2  + shift//2))
        #pygame.draw.rect(screen, (40, 40, 40), text_rect)
        screen.blit(text, text_rect)

        text = font_36.render("Time: " + str(round(timer/1000)) + " sec", True, (0, 0, 0))
        text_rect = text.get_rect(center=(text.get_size()[0]//2  + shift, text.get_size()[1]*2 + text.get_size()[1]//2  + shift//2))
        #pygame.draw.rect(screen, (40, 40, 40), text_rect)
        screen.blit(text, text_rect)

        text = font_36.render("level: " + str(level), True, (0, 0, 0))
        text_rect = text.get_rect(center=(text.get_size()[0]//2  + shift, text.get_size()[1]*3 + text.get_size()[1]//2  + shift//2))
        #pygame.draw.rect(screen, (40, 40, 40), text_rect)
        screen.blit(text, text_rect)

        text = font_36.render("Lifes: ", True, (0, 0, 0))
        text_rect = text.get_rect(center=(text.get_size()[0]//2  + shift, text.get_size()[1]*4 + text.get_size()[1]//2  + shift//2))
        #pygame.draw.rect(screen, (40, 40, 40), text_rect)
        screen.blit(text, text_rect)

        for i in range(lifes):
            heart_rect.center = (150 + i*50  + shift,  text.get_size()[1]*4 + heart.get_size()[1]//2  + shift//2)
            screen.blit(heart, heart_rect)

        if coke_time:
            text = font_36.render("Speed: " + str(round(coke_time/1000)) + " sec", True, (0, 0, 0))
            text_rect = text.get_rect(center=(text.get_size()[0]//2  + shift, text.get_size()[1]*4 + text.get_size()[1]//2 + heart.get_size()[1]  + shift//2))
            #pygame.draw.rect(screen, (40, 40, 40), text_rect)
            screen.blit(text, text_rect)

        if darken:
            screen.blit(darken_surface, (0, 0))
        pygame.display.update()
        fps_tick0 = 0
    else:
        fps_tick0+=10
    pygame.time.wait(10)
