import json
import pygame
import sys
import os
from random import randint
pygame.init()

floor = 1
xx = 1200
yy = 800
fps = 100
fps_tick = 1000/fps
fps_tick0 = 0
screen = pygame.display.set_mode((xx, yy))
file = open('data.json', 'r')
data = json.loads(file.read())
file.close()
backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
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
resize_coef = 10/4
backdround_image = pygame.transform.scale(backdround_image, (backdround_image.get_size()[0]*resize_coef, backdround_image.get_size()[1]*resize_coef))
backdround_image_rect = backdround_image.get_rect()

x_map = backdround_image.get_size()[0]
y_map = backdround_image.get_size()[1]
x = x_map//2
y = y_map//2
x_plus_move = False
x_minus_move = False
y_plus_move = False
y_minus_move = False
x_ac = 0
y_ac = 0
ac_slow = 0.7
ac_speed = 0.5
speed = 9
player_size = 30
mode = 0
x_mode_1 = int()
y_mode_1 = int()
x_mode_2 = int()
y_mode_2 = int()
npc_set_mode = False
new_npc = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                else:
                    mode = 0
            elif event.key == pygame.K_q:
                if mode == 1:
                    for i in range(len(data[str(floor) + "-floor"]["blocks"])):
                        block = data[str(floor) + "-floor"]["blocks"][i]
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if block[0] <= mouse_x + x - xx//2 <= block[0] + block[2] and block[1] <= mouse_y + y - yy//2 <= block[1] + block[3]:
                            del data[str(floor) + "-floor"]["blocks"][i]
                            break
            elif event.key == pygame.K_p:
                data["1-floor"]["blocks"].clear()
            elif event.key == pygame.K_n:
                if npc_set_mode:
                    npc_set_mode = False
                    if new_npc != []:
                        data[str(floor) + "-floor"]["npc"].append(new_npc)
                else:
                    npc_set_mode = True
                    new_npc.clear()
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
                    if not npc_set_mode:
                        x_mode_1, y_mode_1 = pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2
                    else:
                        if new_npc == []:
                            new_npc.append(randint(1, len(npc_list)))
                            new_npc.append(pygame.mouse.get_pos()[0] + x - xx//2)
                            new_npc.append(pygame.mouse.get_pos()[1] + y - yy//2)
                            new_npc.append(0)
                            new_npc.append(0)
                            new_npc.append(randint(1000,5000))
                            new_npc.append([0, 0])
                            new_npc.append([[pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2]])
                            new_npc.append([1, 1, 1000])
                        else:
                            new_npc[7].append([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if mode == 1:
                    if not npc_set_mode:
                        data[str(floor) + "-floor"]["blocks"].append([min(x_mode_1, x_mode_2), min(y_mode_1, y_mode_2), abs(x_mode_1 - x_mode_2), abs(y_mode_1 - y_mode_2)])
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
    
    for i in range(len(data[str(floor) + "-floor"]["npc"])):
        if len(data[str(floor) + "-floor"]["npc"][i][7]) != 1:
            if data[str(floor) + "-floor"]["npc"][i][4] >= data[str(floor) + "-floor"]["npc"][i][5]:
                data[str(floor) + "-floor"]["npc"][i][4] = 0
                if data[str(floor) + "-floor"]["npc"][i][3] != len(data[str(floor) + "-floor"]["npc"][i][7]) - 1:
                    data[str(floor) + "-floor"]["npc"][i][6][0] = (data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3] + 1][0] - data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3]][0]) / ((data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3] + 1][0])**2 + (data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3]][0])**2)**(1/2)
                    data[str(floor) + "-floor"]["npc"][i][6][1] = (data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3] + 1][1] - data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3]][1]) / ((data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3] + 1][1])**2 + (data[str(floor) + "-floor"]["npc"][i][7][data[str(floor) + "-floor"]["npc"][i][3]][1])**2)**(1/2)
            elif data[str(floor) + "-floor"]["npc"][i][6] != []:
                data[str(floor) + "-floor"]["npc"][i][4]+=10

    for i in data[str(floor) + "-floor"]["blocks"]:
        x_prev = x
        y_prev = y + y_ac
        if y_prev + player_size > i[1] and y_prev - player_size < i[1] + i[3] and x_prev + player_size > i[0] and x_prev - player_size < i[0] + i[2]:
            y_plus = False
        x_prev = x + x_ac
        y_prev = y
        if y_prev + player_size > i[1] and y_prev - player_size < i[1] + i[3] and x_prev + player_size > i[0] and x_prev - player_size < i[0] + i[2]:
            x_plus = False
    
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
            for i in data[str(floor) + "-floor"]["blocks"]:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(i[0] - x + xx//2, i[1] - y + yy//2, i[2], i[3]))
            for i in data[str(floor) + "-floor"]["npc"]:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(i[1] - x + xx//2+15, i[2] - y + yy//2 + 25, 2*player_size+1, 2*player_size+1))
            #screen.blit(npc_images[0][i[8][0]-1][i[8][1]-1], npc_rect)
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(min(x_mode_1, x_mode_2) - x + xx//2, min(y_mode_1, y_mode_2) - y + yy//2, abs(x_mode_1 - x_mode_2), abs(y_mode_1 - y_mode_2)))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(xx//2 - player_size, yy//2 - player_size, 2*player_size+1, 2*player_size+1))
        for i in data[str(floor) + "-floor"]["npc"]:
            npc_rect = npc_images[0][i[8][0]-1][i[8][1]-1].get_rect()
            npc_rect.topleft = (i[1] - x + xx//2, i[2] - y + yy//2)
            screen.blit(npc_images[0][i[8][0]-1][i[8][1]-1], npc_rect)
        player_rect = npc_images[0][player_animation[0]-1][player_animation[1]-1].get_rect()
        player_rect.center = (xx//2, yy//2)
        screen.blit(npc_images[0][player_animation[0]-1][player_animation[1]-1], player_rect)
        pygame.display.update()
        fps_tick0 = 0
    else:
        fps_tick0+=10
    pygame.time.wait(10)
