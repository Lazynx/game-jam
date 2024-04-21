import pygame
import sys
import random

pygame.init()
def survey_game(screen):
    window_width, window_height = screen.get_size()

    background_image = pygame.image.load('images/background/survey-bg.jpeg')
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

    font = pygame.font.Font("PIXY.ttf", 36)
    big_font = pygame.font.Font("PIXY.ttf", 42)

    sprite_images = ["images/npc/1/1/1.PNG", "images/npc/1/1/4.PNG"]
    sprites = [pygame.image.load(img) for img in sprite_images]
    global current_sprite
    current_sprite = 0
    sprite_change_speed = 100

    questions = [
        {"question": "Как закрыть Pygame окно?",
        "answers": ["quit()", "exit()", "close()"],
        "correct": 0},
        {"question": "Что возвращает pygame.mouse.get_pos()?",
        "answers": ["Список", "Тапл", "Словарь"],
        "correct": 1},
        {"question": "Как заполнить экран цветом?",
        "answers": ["fill()", "paint()", "cover()"],
        "correct": 0},
        {"question": "Для чего pygame.mixer?",
        "answers": ["Звук", "Изображения", "События"],
        "correct": 0},
        {"question": "Как проверить нажатие клавиши?",
        "answers": ["pressed()", "down()", "hit()"],
        "correct": 0},
        {"question": "Как ограничить FPS?",
        "answers": ["delay()", "wait()", "tick()"],
        "correct": 2},
        {"question": "Что делает pygame.Surface?",
        "answers": ["Рисует", "Создаёт", "Загружает"],
        "correct": 1},
        {"question": "Что из этого цикл игры?",
        "answers": ["loop()", "cycle()", "main()"],
        "correct": 0},
        {"question": "Какой метод рисует прямоугольник?",
        "answers": ["draw.rect()", "draw.square()", "draw.box()"],
        "correct": 0},
        {"question": "Как запустить Pygame?",
        "answers": ["begin()", "init()", "start()"],
        "correct": 1}
    ]

    selected_questions = random.sample(questions, 3)
    current_question = 0
    selected_answer = None
    correct_answers = 0
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

        results_text = font.render(f"Вы ответили правильно на {correct_answers} из 3 вопросов.", True, (0, 0, 0))

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
                            return
                            running = False
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
                        return
                    else:
                        display_question()

        display_question()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
