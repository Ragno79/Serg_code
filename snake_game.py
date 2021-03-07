from tkinter import *
import time
import random

Game_Running = True
# Создание игрового пространства

game_width = 500  # Длина экрана 
game_height = 500  # ширина экрана
snake_item = 20  # Элемент змейки (ячейка таблицы)
snake_color1 = 'red'  # Внутрениий цвет квадратика
snake_color2 = 'yellow'  # Внешний цвет квадратика (задний)

virtual_game_x = game_width // snake_item  # Координаты для подарка как бы внутри сетки 50х50 для х
virtual_game_y = game_height // snake_item  # Координаты для подарка как бы внутри сетки 50х50 для у

snake_x = virtual_game_x // 2  # Координата по х
snake_y = virtual_game_y // 2  # Координата по у
snake_x_nav = 0  # Координата сдига
snake_y_nav = 0  # Координата сдвига

snake_list = []  # Список кооридинат змейки
snake_size = 3  # Длина змейки

prezents_list = []  # Список координат подарков
prezents_size = 25  # Количество подарков на экране

window = Tk()
window.title('Игра Змейка')
window.resizable(0, 0)  # Неизменяемое окно
window.wm_attributes('-topmost', 1)  # Наше окно поверх всех окон

canvas = Canvas(window, width=game_width, height=game_height, bd=0, highlightthickness=0)
canvas.pack()
window.update()

prezent_color1 = 'blue'
prezent_color2 = 'black'

for i in range(prezents_size):  # Расстановка подарков по рандомным координатам
    x = random.randrange(virtual_game_x)
    y = random.randrange(virtual_game_y)
    id1 = canvas.create_oval(x * snake_item, y * snake_item, x * snake_item + snake_item,
                             y * snake_item + snake_item, fill=prezent_color2)
    id2 = canvas.create_oval(x * snake_item + 2, y * snake_item + 2, x * snake_item + snake_item - 2,
                             y * snake_item + snake_item - 2, fill=prezent_color1)
    prezents_list.append([x, y, id1, id2])


def snake_paint_item(canvas, x, y):  # функция рисующая элемент змейки
    global snake_list
    id1 = canvas.create_rectangle(x * snake_item, y * snake_item, x * snake_item + snake_item,
                                  y * snake_item + snake_item, fill=snake_color2)
    id2 = canvas.create_rectangle(x * snake_item + 2, y * snake_item + 2, x * snake_item + snake_item - 2,
                                  y * snake_item + snake_item - 2, fill=snake_color1)
    snake_list.append([x, y, id1, id2])
    # print(snake_list)


snake_paint_item(canvas, snake_x, snake_y)  # Русуем квадратик


def check_can_we_delete_snake_item():
    global snake_list
    if len(snake_list) >= snake_size:
        temp_item = snake_list.pop(0)
        canvas.delete(temp_item[2])
        canvas.delete(temp_item[3])


def check_if_we_found_prezent():
    global snake_size
    for i in range(len(prezents_list)):
        if prezents_list[i][0] == snake_x and prezents_list[i][1] == snake_y:
            snake_size = snake_size + 1
            canvas.delete(prezents_list[i][2])
            canvas.delete(prezents_list[i][3])
        # print("Found")
    # print(snake_x,snake_y)


'''
Ниже, первоначальный код, для управления клавишами до while 
'''


def snake_move(event):
    global snake_x, snake_y, snake_x_nav, snake_y_nav
    if event.keysym == "Up":
        snake_x_nav = 0
        snake_y_nav = -1
        check_can_we_delete_snake_item()
    elif event.keysym == "Down":
        snake_x_nav = 0
        snake_y_nav = 1
        check_can_we_delete_snake_item()
    elif event.keysym == "Left":
        snake_x_nav = -1
        snake_y_nav = 0
        check_can_we_delete_snake_item()
    elif event.keysym == "Right":
        snake_x_nav = 1
        snake_y_nav = 0
        check_can_we_delete_snake_item()
        # После создания автоматического управления, эти команды тут убираем, иначе задваивается нажатие
    # snake_x = snake_x + snake_x_nav
    # snake_y = snake_y + snake_y_nav
    # snake_paint_item(canvas, snake_x, snake_y)
    check_if_we_found_prezent()


canvas.bind_all('<KeyPress-Left>', snake_move)
canvas.bind_all('<KeyPress-Right>', snake_move)
canvas.bind_all('<KeyPress-Up>', snake_move)
canvas.bind_all('<KeyPress-Down>', snake_move)


def game_over():
    global Game_Running
    Game_Running = False


def check_if_borders():
    if snake_x > virtual_game_x or snake_x < 0 or snake_y > virtual_game_y or snake_y < 0:
        game_over()


def check_we_touch_self(f_x, f_y):  # Аргументы будущее х и будущее у
    global Game_Running
    if not (snake_x_nav == 0 and snake_y_nav == 0):
        for i in range(len(snake_list)):
            if snake_list[i][0] == f_x and snake_list[i][1] == f_y:
                Game_Running = False


while Game_Running:
    check_can_we_delete_snake_item()
    check_if_we_found_prezent()
    check_if_borders()
    check_we_touch_self(snake_x + snake_x_nav, snake_y + snake_y_nav)
    snake_x = snake_x + snake_x_nav
    snake_y = snake_y + snake_y_nav
    snake_paint_item(canvas, snake_x, snake_y)
    window.update_idletasks()
    window.update()
    time.sleep(0.15)


def fun_nothing(
        event):  # После выхода из цикла по концу игры, не можем нажимать далее клавиши тк они ведут к пустой функции
    pass


canvas.bind_all('<KeyPress-Left>', fun_nothing)
canvas.bind_all('<KeyPress-Right>', fun_nothing)
canvas.bind_all('<KeyPress-Up>', fun_nothing)
canvas.bind_all('<KeyPress-Down>', fun_nothing)
