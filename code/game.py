from settings import * 
from random import *
from timer import Timer

class Game:
    def __init__(self):
        #General 
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        #lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(60)


        #tetromino
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites)

        #timer
        self.timers = {
            'vertical move': Timer(UPDATE_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(COLLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()),1)
        for row in range(ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(),y))
        
        self.surface.blit(self.line_surface, (0,0))

    def imput(self):
        keys = pygame.key.get_pressed()
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()

    def run(self):

        #update
        self.timer_update()
        self.sprites.update()
        self.sprites.draw(self.surface)

        #drawing
        self.surface.fill(GRAY)
        self.draw_grid()
        self.display_surface.blit(self.surface,(PADDING,PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Tetromino: 
    def __init__(self, shape, group) :
        
        #setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.colour = TETROMINOS[shape]['color']

        # create blocks 
        self.blocks = [Block(group, pos ,self.colour) for pos in self.block_positions]
    
    def move_horizontal(self,amount):
        for block in self.blocks:
            block.pos.x += amount 

    def move_down(self):
        for block in self.blocks:
            block.pos.y += 1 

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos ,color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)
        

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)
    
    def update(self):
        self.rect.topleft =  self.pos * CELL_SIZE

