import pygame
import socket
import random
from threading import Thread
import pygame
import sys
from snake import Snake
from snake import Enemy
from snake import Food
import pickle

light_green = (0,170,140)
dark_green = (0,140,120)
food_color = (250,200,0)
black = (34,34,34)
red = (255,0,0)
blue = (0,0,255)

renk = random.choice([black, red, blue])


# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "192.168.1.39"
SERVER_PORT = 5555 # server's port

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print(e)
print("[+] Connected.")

def generate_code():
    code_list = []
    letter_list = ["a","b","c","d","e","f","g","h","i","k","l","m","n","o","p","r","s","t","u","v","x","y","z"]
    num_list = ["0","1","2","3","4","5","6","7","8","9"]
    letters = random.sample(letter_list, 3)
    nums = random.sample(num_list, 3)
    for i in letters:
        code_list.append(i)
    for i in nums:
        code_list.append(i)
    random.shuffle(code_list)
    code_str = "".join(code_list)
    return code_str


my_code = generate_code()
user_list = []
dic_to_send = {}
gelen_dic = {}
list_ = []
snake_list = [0] #değiştirilecek
generate_food = False
new_pos = (0, 0) #değiştirelecek

def listen_for_messages():
    global generate_food
    global list_
    global new_pos
    while True:
        try:
            message = pickle.loads(s.recv(1024*2)) #server kodundan 2 elemanlı dictionary atacağım
        except Exception as e:
            print(e)
        
        gelen_dic = message
        generate_food = False
        #print(gelen_dic["new_pos"])
        try:
            new_pos = gelen_dic["new_pos"]
            del gelen_dic["new_pos"]
        except Exception as e:
            print(e)

        index_list = list(gelen_dic)
        list_ = list(gelen_dic) #burada amaç aynı eleman sayısında olsun
        for i in gelen_dic:
            index = index_list.index(i)
            if i != my_code:
                list_[index] = [gelen_dic[i][0][0], gelen_dic[i][0][1]]
        list_.remove(my_code)

# make a thread that listens for messages to this client & print them
try:
    t = Thread(target=listen_for_messages)
except Exception as e:
    print(e)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

def draw_grid(surface):
    for y in range(30):
        for x in range(30):
            if (x+y)%2 == 0:
                renk = light_green
            else:
                renk = dark_green
            light = pygame.Rect((x*20,y*20), (20, 20))
            pygame.draw.rect(surface, renk, light)

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial",20)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()

snake = Snake(renk)
food = Food()
#food_pos = food.position

while True:
    clock.tick(5)

    snake.handle_key()
    snake.move()
    #food.position = food_pos
    food.position = new_pos
    
    if snake.positions[0] == food.position:
            snake.lenght += 1
            snake.score += 1
            #rnd_x = random.randint(0,(30)-1)*20
            #rnd_y = random.randint(0,(30)-1)*20
            #food_pos = (rnd_x, rnd_y)
            generate_food = True
    
    draw_grid(surface)

    # food, snake, enemy updates
    food.update(surface)
    for i in list_:
        enemy = Enemy(i[0], i[1])
        enemy.update(surface)
        if snake.positions[0] in enemy.positions:
            snake.reset()
    
    snake.update(surface)

    screen.blit(surface, (0,0))

    pygame.display.update()
    #print(pro_code)


    # finally, send the message


    snake_list[0] = [snake.color, snake.positions, generate_food]

    dic_to_send[my_code] = snake_list
    try:
        s.send(pickle.dumps(dic_to_send))
    except Exception as e:
        print(e)

# close the socket
s.close()