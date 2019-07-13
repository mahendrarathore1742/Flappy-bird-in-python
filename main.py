import random;
import sys;
import pygame;
from pygame.locals import *;
FPS=32;
SCREENWITDH=300;
SCREENHEIGHT=550;
SCREEN=pygame.display.set_mode((SCREENWITDH,SCREENHEIGHT));
GROUNDY=SCREENHEIGHT*0.8;
GAME_SPRITES={};
GAME_SOUND={};
PLAYER='##Image bird.PNG';
BACKGROUND='## Image background.PNG'
PIPE='## image pipe.PNG'
def welcomeScreen():
    playerx=int(SCREENWITDH/5);
    playery=int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2);
    basex=0;
    messagex=int((SCREENWITDH-GAME_SPRITES['message'].get_width())/2);
    messagey=int(SCREENHEIGHT*0.13);
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit();
                sys.exit();
            elif event.type==KEYDOWN and (event.key==K_ESCAPE or event.key==K_UP):
                return;
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0, 0));
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery));
                SCREEN.blit(GAME_SPRITES['message'],(messagex, messagey));
                SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY));
                pygame.display.update();
                FPSCLOCK.tick(FPS);
def maingame():
    score=0;
    playerx=int(SCREENWITDH/5);
    playery=int(SCREENWITDH/2);
    basex=0;
    newpipe1=getRandomPipe();
    newpipe2=getRandomPipe();
    upperPipes=[
        {'x':SCREENWITDH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWITDH+200+(SCREENWITDH/2),'y':newpipe2[0]['y']}
    ]
    lowerPipes=[
        {'x':SCREENWITDH +200,'y':newpipe1[1]['y']},
        {'x':SCREENWITDH +200+(SCREENWITDH/2),'y':newpipe2[1]['y']}
    ]
    pipevalx=-4;
    playervaly=-9;
    playermaxy=10;
    playerminy=-8;
    playeraccy=1;
    playerflapaccy=-8;
    playerflapped=False;
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit();
                sys.exit();
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervaly=playerflapaccy;
                    playerflapped=True;
                    GAME_SOUND['wing'].play();
        
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes);
        if crashTest:
            return;
        

        playermidpos=playerx + GAME_SPRITES['player'].get_width()/2;
        for pipe in upperPipes:
            pipemidpos=pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2;
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1;
                print(f'your score is {score}');
                GAME_SOUND['point'].play();
        
        if playervaly< playermaxy and not playerflapped:
            playervaly+=playeraccy;
    
        if playerflapped:
            playerflapped=False;
        playerHeight=GAME_SPRITES['player'].get_height();
        playery=playery+min(playervaly,GROUNDY-playery-playerHeight);

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipevalx;
            lowerPipe['x']+=pipevalx;

        if 0<upperPipes[0]['x']< 5:
            newpipe=getRandomPipe();
            upperPipes.append(newpipe[0]);
            lowerPipes.append(newpipe[1]);
 
        if upperPipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0);
            lowerPipes.pop(0);

        SCREEN.blit(GAME_SPRITES['background'],(0,0));

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']));
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']));

        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY));
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery));
        mydigits=[int(x) for x  in list(str(score))];
        width=0;

        for digit in mydigits:
            width+=GAME_SPRITES['number'][digit].get_width();
        xofffset=(SCREENWITDH-width)/2;


        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['number'][digit],(xofffset,SCREENHEIGHT*0.12));
            xofffset+=GAME_SPRITES['number'][digit].get_width();
        pygame.display.update();
        FPSCLOCK.tick(FPS);

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery>GROUNDY-25 or playery<0:
        GAME_SOUND['hit'].play();
        return True;
    
    for pipe in upperPipes:
        pipeheight=GAME_SPRITES['pipe'][0].get_height();
        if (playery<pipeheight+pipe['y'] and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play();
            return True;
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() >pipe['y']) and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['hit'].play();
            return True;
    return False;

def getRandomPipe():
    pipeheight=GAME_SPRITES['pipe'][0].get_height();
    offset=SCREENHEIGHT/3;
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset));
    pipex=SCREENWITDH+10;
    y1=pipeheight-y2+offset;
    pipe=[
        {'x':pipex,'y':-y1},
        {'x':pipex,'y':y2}  
    ]
    return pipe;
if __name__=="__main__":
    pygame.init();
    FPSCLOCK=pygame.time.Clock();
    pygame.display.set_caption('Devleped by mahendra singh');
    GAME_SPRITES['number']=(
        pygame.image.load('##NUMBER PHOTOS 0.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  1.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  2.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  3.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS   4.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  5.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  6.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  7.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  8.PNG').convert_alpha(),
        pygame.image.load('##NUMBER PHOTOS  9.PNG').convert_alpha()
    );
    GAME_SPRITES['message']=pygame.image.load(' # Start Image start.JPG').convert_alpha();
    GAME_SPRITES['base']=pygame.image.load(' #this baes Image bird hit in  base.PNG').convert_alpha();
    GAME_SPRITES['pipe']=(
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    );
    GAME_SOUND['die']=pygame.mixer.Sound('#GIVE PATH FOR DIE SOUND die.wav');
    GAME_SOUND['hit']=pygame.mixer.Sound('GIVE PATH FOR HIT SOUND hit.wav');
    GAME_SOUND['point']=pygame.mixer.Sound('GIVE PATH FOR POINT SOUND point.wav');
    GAME_SOUND['swoosh']=pygame.mixer.Sound('GIVE PATH FOR SWOOSH SOUND swoosh.wav');
    GAME_SOUND['wing']=pygame.mixer.Sound('GIVE PATH FOR WING SOUND wing.wav');
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert();
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha();
    while True:
        welcomeScreen();
        maingame();