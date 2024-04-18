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
backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
backdround_image_rect = backdround_image.get_rect()
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
font = pygame.font.Font(None, 36)
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
speed = 8
player_size = 30
mode = 0
x_mode_1 = int()
y_mode_1 = int()
x_mode_2 = int()
y_mode_2 = int()
mouse_hold = False

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
                    speed = 15
                else:
                    mode = 0
                    speed = 8
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
                        if (((data[str(floor) + "-floor"]["npc"][i][0] + npc_images[0][0][0].get_size()[0]//2) - mouse_x - x + xx//2)**2 + ((data[str(floor) + "-floor"]["npc"][i][1] + npc_images[0][0][0].get_size()[1]//2) - mouse_y - y +yy//2)**2)**(1/2) <= 40:
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
            elif event.key == pygame.K_p:
                if mode == 1:
                    #data["1-floor"]["npc"].clear()
                    None
            elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4:
                if mode == 1:
                    direction = 1
                    if event.key == pygame.K_2:
                        direction = 2
                    elif event.key == pygame.K_3:
                        direction = 3
                    elif event.key == pygame.K_4:
                        direction = 4
                    data["1-floor"]["npc"].append([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, randint(1, len(npc_images)), direction, 1, randint(0, 1000), 1000])
                    #print([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, randint(1, len(npc_images)), 1, 1])
            elif event.key == pygame.K_c:
                if mode == 1:
                    print("Write number: ")
                    room = int(input())
                    data["1-floor"]["rooms"].append([room, pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2])
            elif event.key == pygame.K_v:
                if mode == 1:
                    data["1-floor"]["stairs"].append([pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2, 0, 0, 1])
            elif event.key == pygame.K_x:
                if mode == 1:
                    print(pygame.mouse.get_pos()[0] + x - xx//2, pygame.mouse.get_pos()[1] + y - yy//2)
            elif event.key == pygame.K_r or event.key == pygame.K_t or event.key == pygame.K_y or event.key == pygame.K_u:
                if mode == 1:
                    floor_num = 1
                    if event.key == pygame.K_t:
                        floor_num = 2
                    elif event.key == pygame.K_y:
                        floor_num = 3
                    elif event.key == pygame.K_u:
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
    
        for i in data[str(floor) + "-floor"]["npc"]:
            if ((x - (i[0]+npc_images[0][0][0].get_size()[0]//2))**2 + (y - (i[1]+npc_images[0][0][0].get_size()[1]//2))**2)**(1/2) <= 40:
                x_ac*=-1
                y_ac*=-1

        for i in data[str(floor) + "-floor"]["stairs"]:
            if ((i[0] - x)**2 + (i[1] - y)**2)**(1/2) <= 50:
                floor+=i[4]
                backdround_image = pygame.image.load("images/floors/" + str(floor) + "-floor_kbtu.jpg")
                backdround_image = pygame.transform.scale(backdround_image, (12000, 12000))
                backdround_image_rect = backdround_image.get_rect() 
                x = i[2]
                y = i[3]

    
    for i in range(len(data[str(floor) + "-floor"]["npc"])):
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
                text = font.render(str(i[0]), True, (255, 0 , 0))
                text_rect = text.get_rect(center=(i[1]  - x + xx//2, i[2] - y + yy//2))
                pygame.draw.circle(screen, (0, 255, 0), (i[1]  - x + xx//2, i[2] - y + yy//2), 50)
                screen.blit(text, text_rect)
            for i in data[str(floor) + "-floor"]["blocks"]:
                pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(i[0] - x + xx//2, i[1] - y + yy//2, i[2], i[3]))
            for i in data[str(floor) + "-floor"]["npc"]:
                pygame.draw.circle(screen, (0, 255, 0), ((i[0]+npc_images[0][0][0].get_size()[0]//2) - x + xx//2, (i[1]+npc_images[0][0][0].get_size()[1]//2) - y + yy//2), 40)
            #screen.blit(npc_images[0][i[8][0]-1][i[8][1]-1], npc_rect)
            if mouse_hold:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(min(x_mode_1, x_mode_2) - x + xx//2, min(y_mode_1, y_mode_2) - y + yy//2, abs(x_mode_1 - x_mode_2), abs(y_mode_1 - y_mode_2)))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(xx//2 - player_size, yy//2 - player_size, 2*player_size+1, 2*player_size+1))
        for i in data[str(floor) + "-floor"]["npc"]:
            npc_rect = npc_images[i[2]-1][i[3]-1][i[4]-1].get_rect()
            npc_rect.topleft = (i[0] - x + xx//2, i[1] - y + yy//2)
            screen.blit(npc_images[i[2]-1][i[3]-1][i[4]-1], npc_rect)
        player_rect = npc_images[0][player_animation[0]-1][player_animation[1]-1].get_rect()
        player_rect.center = (xx//2, yy//2)
        screen.blit(npc_images[0][player_animation[0]-1][player_animation[1]-1], player_rect)
        pygame.display.update()
        fps_tick0 = 0
    else:
        fps_tick0+=10
    pygame.time.wait(10)
