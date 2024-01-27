import pygame
import random
import math
from pygame import mixer
import cv2
import mediapipe as mp
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#Capture webcam
cam = cv2.VideoCapture(0)
pygame.init()
#screen size
Screen = pygame.display.set_mode((900,800)) 
#sounds
# mixer.music.load("background.wav")
# mixer.music.play(-1)
#title
pygame.display.set_caption("In the space")
icon = pygame.image.load("001-startup.png")
pygame.display.set_icon(icon)
#playerg
playerimg =pygame.image.load("001-spaceship.png")
playerx =450
playery =650
playerx_change=0
playery_change=0
def player(playerx ,playery):
    Screen.blit(playerimg ,(playerx ,playery))
#missile
missimg =pygame.image.load("002-bullet.png")
missx =1000
missy =1000
missx_change =0
missy_change =0
miss_state ="ready"
def missile(x,y):
    Screen.blit(missimg,(x ,y))
#collision
def shoot_out(missx,missy,enemyx,enemyy):
    distance = math.sqrt(math.pow(enemyx-missx,2) + (math.pow(enemyy-missy,2)))
    if distance <30:
        return True
    else:
        return False
#enemy
enemyimg =pygame.image.load("001-rock.png")
enemyx = random.randint(0 ,832)
enemyy = random.randint(0,100)
enemyx_change=0
enemyy_change=0
def enemy(enemyx,enemyy):
    Screen.blit(enemyimg,(enemyx ,enemyy ))
disenemy =pygame.image.load("002-asteroids.png")
dis_enemyx =1000
dis_enemyy =1000
def dis_enemy(enemyx , enemyy):
    Screen.blit(disenemy,(enemyx ,enemyy ))
#master_enemy

m_enemyimg= pygame.image.load("001-space-ship.png")

m_enemyx = random.randint(0 ,732)
m_enemyy = random.randint(0,100)
m_enemyx_change=0
m_enemyy_change=0
def m_enemy(m_enemyx,m_enemyy):
    Screen.blit(m_enemyimg,(m_enemyx ,m_enemyy ))
#game_over
life =0
khatam =False
def game_over(life):
    if life ==3 :
        return True

#score
score_value =0

font = pygame.font.Font('freesansbold.ttf',32)
textx =0
texty =0
def print_score(x,y):
    score =font.render("Score :" +str(score_value),True,(200,200,200))
    Screen.blit(score,(x ,y ))
#game loop
running =True
left_wait=0
right_wait=0
down_wait=0
rotate_wait=0
fallspeed_real=0.45
fallspeed=fallspeed_real
while running :
    Screen.fill((0,0,50))
    sucess,img=cam.read()
    imgg = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(imgg, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = imgg.shape
                if id == 0:
                    x = []
                    y = []
                x.append(int((lm.x) * w))
                y.append(int((1 - lm.y) * h))

                #This will track the hand gestures
                if len(y) > 20:
                    if (x[0] > x[3] > x[4]) and not(y[20] > y[17]):
                        left_wait += 2
                    if not(x[0] > x[3] > x[4]) and (y[20] > y[17]):
                        right_wait += 2
                    if (x[8]): 
                        rotate_wait += 2
                    if not(x[0] > x[3] > x[4]) and not(y[20] > y[17]):
                        down_wait+=2


            mpDraw.draw_landmarks(imgg, handLms, mpHands.HAND_CONNECTIONS)

    

    cv2.namedWindow("WebCam")
    cv2.moveWindow("WebCam", 20, 121)
    cv2.imshow("WebCam", imgg)
    cv2.waitKey(2)
    
    if down_wait>=0.25:
        playerx_change=0

    if left_wait>=0.25:
        playerx_change = -15
        left_wait = 0
        right_wait = 0
        rotate_wait = 0
        down_wait = 0
    if right_wait>=0.25:
        playerx_change = 15
        left_wait = 0
        right_wait = 0
        rotate_wait = 0
        down_wait = 0
    if rotate_wait>=0.25:
        if miss_state == "ready":
                missx=playerx +10
                missy=playery +10
                missile(missx,missy)
                miss_state = "fire"
                # missile_sound = mixer.Sound("C:\\Users\\DELL\\Desktop\\game\\laser.wav")
                # missile_sound.play()
    
    playerx += playerx_change
    if playerx >= 832:
        playerx = 832
    elif playerx <=0:
        playerx =0
    colli =shoot_out(missx,missy,enemyx,enemyy)
    if colli:
        dis_enemyx = enemyx
        dis_enemyy = enemyy
        miss_state = "ready"
        enemyx = random.randint(0 ,832)
        enemyy = random.randint(0,100)  
        Screen.blit(enemyimg,(enemyx ,enemyy ))
        score_value+= 1
    dis_enemy(dis_enemyx,dis_enemyy)
    m_colli =shoot_out(missx,missy,m_enemyx,m_enemyy)
    if m_colli:
        dis_enemyx = m_enemyx
        dis_enemyy = m_enemyy
        miss_state = "ready"
        m_enemyx = random.randint(0 ,832)
        m_enemyy = random.randint(0,100)  
        Screen.blit(enemyimg,(m_enemyx ,m_enemyy ))
        score_value+= 1
    player(playerx,playery)
    enemy(enemyx-16,enemyy-10)
    if score_value <= 10:
        m_enemy(m_enemyx,m_enemyy)
    missile(missx,missy)
    missy_change =100
    missy -= missy_change
    if missy <= 0:
        miss_state = "ready" 
    enemyy_change =5
    enemyy +=enemyy_change
    m_enemyy_change =5
    m_enemyy +=m_enemyy_change
    
    if enemyy >=600:
        life= life+1
        khatam = game_over(life)
        enemyx = random.randint(0 ,832)
        enemyy = random.randint(0,100)
    if khatam :
        font2 = pygame.font.Font('freesansbold.ttf',50)
        khatam =font2.render("GAME OVER " ,True,(250,200,200))
        Screen.blit(khatam,(340,400 ))
        playerx_change = 0

    print_score(textx,texty)
    if missy ==enemyy:
            enemyy=1000
            enemyy=1000
    pygame.display.update()
