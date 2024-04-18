import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption('Викторина Pygame')
window_width, window_height = screen.get_size()

background_image = pygame.image.load('images/background/survey-bg.jpeg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

font = pygame.font.Font(None, 36)

sprite_images = ["images/npc/1/1/1.PNG", "images/npc/1/1/4.PNG"]
sprites = [pygame.image.load(img) for img in sprite_images]
current_sprite = 0
sprite_change_speed = 100

questions = [
    {"question": "Что делает функция pygame.init()?",
     "answers": ["Закрывает Pygame", "Инициализирует все импортированные модули Pygame",
                 "Открывает новое окно браузера"], "correct": 1},
    {"question": "Какой метод используется для обновления всего экрана в Pygame?",
     "answers": ["pygame.display.update()", "pygame.update()", "pygame.refresh()"], "correct": 0},
    {"question": "Как создать окно игры размером 800x600 пикселей?",
     "answers": ["pygame.display.set_mode((600, 800))", "pygame.display.set_mode((800, 600))",
                 "pygame.screen.set_size(800, 600)"], "correct": 1},
    {"question": "Для чего используется pygame.event.get()?",
     "answers": ["Для получения текущего состояния клавиш", "Для загрузки изображений",
                 "Для обработки очереди событий"], "correct": 2},
    {"question": "Какой тип данных возвращается функцией pygame.key.get_pressed()?",
     "answers": ["Список", "Словарь", "Кортеж"], "correct": 0},
    {"question": "Что из перечисленного не является стандартным типом события в Pygame?",
     "answers": ["pygame.QUIT", "pygame.PLAY", "pygame.MOUSEBUTTONDOWN"], "correct": 1},
    {"question": "Какая функция используется для загрузки изображений в Pygame?",
     "answers": ["pygame.image.load()", "pygame.load.image()", "pygame.images.get()"], "correct": 0},
    {"question": "Какая функция устанавливает заголовок окна в Pygame?",
     "answers": ["pygame.display.set_title()", "pygame.display.set_caption()", "pygame.window.title()"], "correct": 1},
    {"question": "Какой аргумент необходимо использовать, чтобы pygame.display.flip() обновлял только часть экрана?",
     "answers": ["Передать список прямоугольников", "Никаких дополнительных аргументов не требуется",
                 "Передать координаты верхнего левого угла"], "correct": 1},
    {"question": "Как в Pygame создать звуковой объект?",
     "answers": ["pygame.Sound()", "pygame.audio.Sound()", "pygame.mixer.Sound()"], "correct": 2}
]

selected_questions = random.sample(questions, 3)
current_question = 0
selected_answer = None
correct_answers = 0
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
    sprite_rect = sprite.get_rect(midleft=(0, window_height // 2))
    screen.blit(sprite, sprite_rect)

    question = selected_questions[current_question]
    text_surface = font.render(question['question'], True, (0, 0, 0))
    bubble_x = sprite_rect.right + 20
    bubble_y = window_height // 2 - 100
    bubble_surface = pygame.Surface((text_surface.get_width() + 20, (len(question['answers']) + 1) * 50), pygame.SRCALPHA)
    pygame.draw.rect(bubble_surface, (255, 255, 255), bubble_surface.get_rect(), border_radius=5)
    bubble_rect = bubble_surface.get_rect(topleft=(bubble_x, bubble_y))
    screen.blit(bubble_surface, bubble_rect)
    screen.blit(text_surface, (bubble_x + 10, bubble_y + 5))

    answer_rects.clear()
    for i, answer in enumerate(question['answers']):
        answer_surface = font.render(f"{i + 1}. {answer}", True, (0, 0, 0))
        answer_text_rect = answer_surface.get_rect(topleft=(bubble_x + 10, bubble_y + 55 + i * 50))
        answer_rect = pygame.Rect(bubble_x + 10, bubble_y + 55 + i * 50, bubble_surface.get_width() - 20, answer_surface.get_height())
        answer_rects.append(answer_rect)
        screen.blit(answer_surface, answer_text_rect)


def show_results():
    screen.blit(background_image, (0, 0))
    results_text = font.render(f"Вы ответили правильно на {correct_answers} из 3 вопросов.", True, (230, 230, 230))
    screen.blit(results_text, (100, window_height / 2))
    pygame.display.flip()
    pygame.time.wait(10000)


display_question()


running = True
clock = pygame.time.Clock()

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
                    running = False
                else:
                    display_question()

    display_question()
    pygame.display.flip()

pygame.quit()
sys.exit()