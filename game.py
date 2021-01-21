import random , pygame
pygame.init()


class Sounds:
    die = pygame.mixer.Sound(r"Sounds\die.wav")
    hit = pygame.mixer.Sound(r"Sounds\hit.wav")
    swoosh = pygame.mixer.Sound(r"Sounds\swoosh.wav")
    point = pygame.mixer.Sound(r"Sounds\point.wav")
    wing = pygame.mixer.Sound(r"Sounds\die.wav")
    

class Bird:
    def __init__(self,location,x,y,speed):
        self.image = pygame.image.load(location)
        self.x = x
        self.y = y
        self.speed = speed
        self.jump = False
    def draw(self):
        screen.blit(self.image,(self.x,self.y))
    def move(self):
        if self.jump == False:
            self.y += self.speed
        else: self.y-= self.speed*3


class Pipe:
    def __init__(self,up,down,x,y,speed):
        self.up = pygame.image.load(up)
        self.down =  pygame.image.load(down)
        self.x = x
        self.y = y
        self.speed = speed
    def draw(self,screen):
        screen.blit(self.up,(self.x,self.y))
        screen.blit(self.down,(self.x,self.y+420))
    def move(self):
        self.x-=self.speed  
        if self.x<=0:
            self.x = 500
            self.y = random.randint(-250,-100)


class Functions:
    score = 0
    font = pygame.font.SysFont('PlayfairDisplay',32)

    @classmethod
    def print_score(cls):
        screen.blit(cls.font.render("Score: "+str(cls.score),True,(255,255,255)),(10,10))

    @classmethod
    def event_listener(cls,running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not running:
                    running = True
                else: running = False
            
            if event.type == pygame.KEYDOWN:
                if running == None: running = True
                if event.key == pygame.K_SPACE and running == True:
                    Sounds.wing.play()
                    bird.jump = True

            if event.type == pygame.KEYUP and running == True:
                bird.jump = False
        return running

    @classmethod
    def crash(cls,pipe,bird):
        if pipe.x == bird.x+20:
            if bird.y <= 320+pipe.y or bird.y>pipe.y+420:
                Sounds.hit.play()
                Sounds.die.play()
                print("GAME OVER")
                return True
            else: 
                Sounds.point.play()
                cls.score+=1
                return False
    
    @classmethod
    def update(cls):
        new = False
        with open('highscore.txt','a+') as f:
            f.seek(0)
            hs = f.readlines()
            if int(hs[0]) < cls.score:
                f.truncate(0)
                f.write(str(cls.score))
                new = True
        if new == True:
            return 'New Highscore!!'
        return 'Your Highscore is '+hs[0]

if __name__ == '__main__':
    up = r"Images\pipe-up.png"
    down = r"Images\pipe-down.png"

    bird = Bird(r"Images\Bird.png",100,300,0.5)
    pipe1 = Pipe(up,down,300,-170,0.5)
    pipe2 = Pipe(up,down,550,-100,0.5)
    pipes = [pipe1,pipe2]

    background = pygame.image.load(r"Images\Background.png")
    base = pygame.image.load(r"Images\base.png")
    intro = pygame.image.load(r"Images\intro.png")
    over = pygame.image.load(r"Images\gameover.png")

    screen = pygame.display.set_mode((288,516))
    pygame.display.set_caption("FLAPPY BIRD")
     
    running = None
    screen.blit(background,(0,0))

    while running == None:
        screen.blit(intro,(50,100))
        if Functions.event_listener(running) != None: running = True
        pygame.display.update()

    while running:
        screen.blit(background,(0,0))
        if not Functions.event_listener(running): running = False
    
        bird.draw()
        bird.move()

        for pipe in pipes:
            pipe.draw(screen)
            pipe.move()
            if Functions.crash(pipe,bird) == True:
                running = False
            elif bird.y >410: running = False
            
        Functions.print_score()
        screen.blit(base,(0,410))
        pygame.display.update()

    
    while not running:
        screen.blit(background,(0,0))
        screen.blit(over,(50,150))
        text = Functions.font.render("Your Score was "+str(Functions.score),True,(255,255,255))
        screen.blit(text,(50,200))
        screen.blit(Functions.font.render(Functions.update(),True,(255,255,255)),(45,230))
        pygame.display.update()
        if Functions.event_listener(running): running = True

