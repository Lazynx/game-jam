import pygame
import sys
import random

pygame.init()
def survey_game(screen, mode):
    window_width, window_height = screen.get_size()

    background_image = pygame.image.load('images/background/survey-bg.jpeg')
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

    font = pygame.font.Font("PIXY.ttf", 36)
    big_font = pygame.font.Font("PIXY.ttf", 42)

    survey_music = pygame.mixer.Sound("sounds/survey.mp3")
    survey_music.play(-1)

    sprite_images = ["images/npc/1/1/1.PNG", "images/npc/1/1/4.PNG"]
    sprites = [pygame.image.load(img) for img in sprite_images]
    global current_sprite
    current_sprite = 0
    sprite_change_speed = 100

    questions = [
        {"question": "What does the len() function do in Python?",
        "answers": ["Deletes the object", "Returns the number of elements", "Copies the object"],
        "correct": 1},
        {"question": "How to create an empty list in Python?",
        "answers": ["my_list = {}", "my_list = ()", "my_list = []"],
        "correct": 2},
        {"question": "Which method is used to concatenate strings in Python?",
        "answers": ["+ operator", "concat()", "join()"],
        "correct": 2},
        {"question": "What keyword is used to define a function in Python?",
        "answers": ["function", "def", "create"],
        "correct": 1},
        {"question": "What is if in Python?",
        "answers": ["Loop", "Function", "Conditional statement"],
        "correct": 2},
        {"question": "How to convert a string to a number in Python?",
        "answers": ["float()", "int()", "str()"],
        "correct": 1}
    ]
    if mode == 2:
        questions = [
            {"question": "How to create a new Pygame window?",
            "answers": ["pygame.display.set_mode()", "pygame.init()", "pygame.window()"],
            "correct": 0},
            {"question": "Which function is used to load images in Pygame?",
            "answers": ["pygame.load_image()", "pygame.image.load()", "pygame.load()"],
            "correct": 1},
            {"question": "What is the name of the module for working with sound in Pygame?",
            "answers": ["pygame.mixer", "pygame.sound", "pygame.audio"],
            "correct": 0},
            {"question": "What is the name of the function to draw a rectangle in Pygame?",
            "answers": ["pygame.draw.rect()", "pygame.draw.rectangle()", "pygame.draw_square()"],
            "correct": 0},
            {"question": "What is the name of the function to limit FPS in Pygame?",
            "answers": ["pygame.fps_limit()", "pygame.delay()", "pygame.time.Clock()"],
            "correct": 2}
        ]
    elif mode == 3:
        questions = [
            {"question": "How to properly close a Pygame window?",
            "answers": ["pygame.quit() and sys.exit()", "exit()", "close()"],
            "correct": 0},
            {"question": "What does pygame.mouse.get_pos() return?",
            "answers": ["List", "Tuple", "Dictionary"],
            "correct": 1},
            {"question": "How to fill the screen with color in Pygame?",
            "answers": ["screen.fill(color)", "screen.paint(color)", "screen.cover(color)"],
            "correct": 0},
            {"question": "What is pygame.mixer used for?",
            "answers": ["Sound", "Images", "Events"],
            "correct": 0},
            {"question": "How to check for key presses in Pygame?",
            "answers": ["pygame.key.get_pressed()", "pygame.key.down()", "pygame.key.hit()"],
            "correct": 0},
            {"question": "How to limit FPS in Pygame?",
            "answers": ["delay()", "wait()", "tick()"],
            "correct": 2},
            {"question": "What does pygame.Surface do?",
            "answers": ["Draws", "Creates", "Loads"],
            "correct": 1}
        ]
    elif mode == 4:
        questions = [
            {"question": "How to check if an element belongs to a list in Python?",
            "answers": ["contains", "in", "belongsto"],
            "correct": 1},
            {"question": "What is for in Python?",
            "answers": ["Conditional operator", "Loop", "Function"],
            "correct": 1},
            {"question": "What is the function used to load fonts in Pygame?",
            "answers": ["pygame.font.Font()", "pygame.font.SysFont()", "pygame.load.font()"],
            "correct": 0},
            {"question": "Which of the following can be used to implement a game loop in Pygame?",
            "answers": ["While loop", "For loop", "Function loop"],
            "correct": 0},
            {"question": "Which method draws a rectangle in Pygame?",
            "answers": ["pygame.draw.rect()", "pygame.draw.square()", "pygame.draw.box()"],
            "correct": 0},
            {"question": "How to start Pygame?",
            "answers": ["begin()", "init()", "start()"],
            "correct": 1}
        ]

    selected_questions = random.sample(questions, 3)
    current_question = 0
    selected_answer = None
    correct_answers = int(0)
    global answer_rects
    answer_rects = []


    def load_sprites():
        return [pygame.image.load(img) for img in sprite_images]


    def animate_sprite():
        global current_sprite
        current_sprite += 1
        if current_sprite >= len(sprites) * sprite_change_speed:
            current_sprite = 0
        current_sprite_index = (current_sprite // sprite_change_speed) % len(sprites)
        return sprites[current_sprite_index]


    def display_question():
        global answer_rects
        screen.blit(background_image, (0, 0))

        sprite = animate_sprite()
        sprite_rect = sprite.get_rect(midleft=(0, window_height / 2 + 250))
        screen.blit(sprite, sprite_rect)
        question_text = selected_questions[current_question]['question']
        question_surface = big_font.render(question_text, True, (0, 0, 0))
        question_box = pygame.Surface((screen.get_width() - 200, 70), pygame.SRCALPHA)
        pygame.draw.rect(question_box, (255, 255, 255), question_box.get_rect())
        pygame.draw.rect(question_box, (0, 0, 0), question_box.get_rect(), 5)
        question_box.blit(question_surface, (10, 10))
        screen.blit(question_box, (100, screen.get_height() / 2 - 150))

        # Draw the boxes for the answers
        answer_rects.clear()
        horizontal_margin = 50
        for i, answer in enumerate(selected_questions[current_question]['answers']):
            answer_surface = font.render(answer, True, (0, 0, 0))
            answer_box = pygame.Surface((screen.get_width() / 2 - 100, 50), pygame.SRCALPHA)
            pygame.draw.rect(answer_box, (255, 255, 255), answer_box.get_rect())
            pygame.draw.rect(answer_box, (0, 0, 255), answer_box.get_rect(), 5)
            answer_box.blit(answer_surface, (10, 10))

            answer_rect = answer_box.get_rect()
            if i % 2 == 0:  # For left side answers
                answer_rect.x = horizontal_margin
            else:  # For right side answers
                answer_rect.x = screen.get_width() / 2 + horizontal_margin / 2
            answer_rect.y = (i // 2) * 60 + screen.get_height() / 2
            answer_rects.append(answer_rect)

            screen.blit(answer_box, answer_rect.topleft)


    def show_results():
        screen.blit(background_image, (0, 0))

        if correct_answers == 3:
            border_color = (255, 215, 0)
        elif 1 <= correct_answers < 3:
            border_color = (0, 0, 255)
        else:
            border_color = (255, 0, 0)

        results_text = font.render(f"You answered {correct_answers} out of 3 questions correctly.", True, (0, 0, 0))

        text_background = pygame.Surface((results_text.get_width() + 20, results_text.get_height() + 20))
        text_background.fill((255, 255, 255))  # White background
        pygame.draw.rect(text_background, border_color, text_background.get_rect(), 5)  # Draw the border

        text_background_rect = text_background.get_rect(center=(window_width / 2, window_height / 2))
        screen.blit(text_background, text_background_rect)
        screen.blit(results_text, (text_background_rect.x + 10, text_background_rect.y + 10))

        pygame.display.flip()
        pygame.time.wait(5000)

    display_question()


    running = True
    clock = pygame.time.Clock()
    # test
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for index, rect in enumerate(answer_rects):
                    if rect.collidepoint(pos):
                        selected_answer = index
                        if selected_questions[current_question]['correct'] == selected_answer:
                            correct_answers += 1
                        current_question += 1
                        if current_question >= len(selected_questions):
                            show_results()
                            pygame.mixer.stop()
                            return int(correct_answers)
                        else:
                            selected_answer = None
                            display_question()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_answer is not None:
                    if selected_questions[current_question]['correct'] == selected_answer:
                        correct_answers += 1
                    current_question += 1
                    selected_answer = None
                    if current_question >= len(selected_questions):
                        show_results()
                        pygame.mixer.stop()
                        return int(correct_answers)
                    else:
                        display_question()

        display_question()
        pygame.display.flip()
