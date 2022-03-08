import random
import pygame
from pygame.locals import *

"""  Version 1.2  """
"""  2021-11-06   """

class Path:
    def __init__(  self ):
        self.paths = {}

    def __init__(  self, paths ):
        self.paths = paths

    def addPath(self, key, to):
        self.paths[key] = to

    def getPaths(self):
        return self.paths


class Room:
    def __init__(  self, name, text, view, paths ):
        self.text = text
        self.view = view
        self.name = name
        self.paths = paths
    

class CodingPiratesDungeon:
    """ Coding Pirates Dungeon class for rendering and preparing a pygame environment """

    def __init__(self, resourcePath, width, height, title):
        pygame.init()

        self.startRoomName = "start"

        self.rooms = []

        self.resourcePath = resourcePath

        self.display_width = width
        self.display_height = height
        self.view = None
        uiBg_temp = pygame.image.load(resourcePath+"ui-bg.png")
        self.doorGfx = pygame.image.load(resourcePath+"door.png")
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height), HWSURFACE|DOUBLEBUF|SCALED)
        self.doublebuffer = self.gameDisplay.copy()

        self.text = []

        self.uiBg = pygame.transform.scale(uiBg_temp, self.doublebuffer.get_rect().size)

        pygame.display.set_caption(title)
        X = -1
        P = -2
        self.view = [
            [0,0,0,0,0],
            [X,0,0,0,X],
            [X,0,0,0,X],
            [X,0,P,0,X],
        ]

        self.ROAD_DOOR_CLOSED = [
            [1,1,0,1,1],
            [X,1,0,1,X],
            [X,1,4,1,X],
            [X,1,P,1,X],
        ]

        self.ROAD_DOOR_OPEN = [
            [1,1,0,1,1],
            [X,1,0,1,X],
            [X,1,3,1,X],
            [X,1,P,1,X],
        ]

        self.ROAD_HALLWAY = [
            [1,1,0,1,1],
            [X,1,0,1,X],
            [X,1,0,1,X],
            [X,1,P,1,X],
        ]

        self.ROAD_LEFT_TURN = [
            [1,1,1,1,1],
            [X,1,1,1,X],
            [X,0,0,1,X],
            [X,1,P,1,X],
        ]

        self.ROAD_RIGHT_TURN = [
            [1,1,1,1,1],
            [X,1,1,1,X],
            [X,1,0,0,X],
            [X,1,P,1,X],
        ]

        self.ROAD_SPLIT_2 = [
            [1,1,1,1,1],
            [X,1,0,1,X],
            [X,0,0,0,X],
            [X,1,P,1,X],
        ]

        self.ROAD_SPLIT_2_LEFT = [
            [1,1,0,1,1],
            [X,1,0,1,X],
            [X,0,0,1,X],
            [X,1,P,1,X],
        ]
        self.ROAD_SPLIT_2_RIGHT = [
            [1,1,0,1,1],
            [X,1,0,1,X],
            [X,1,0,0,X],
            [X,1,P,1,X],
        ]

        self.ROAD_SPLIT_3 = [
            [1,1,0,1,1],
            [X,1,0,1,X],
            [X,0,0,0,X],
            [X,1,P,1,X],
        ]
        self.ROAD_DEADEND = [
            [1,1,1,1,1],
            [X,1,1,1,X],
            [X,1,0,1,X],
            [X,1,P,1,X],
        ]        
        self.ROAD_OUTSIDE = [
            [1,1,2,1,1],
            [X,1,0,1,X],
            [X,1,0,1,X],
            [X,1,P,1,X],
        ]        
        self.loadResources( )

    def addRoom(self, room):
        self.rooms.append( room )

    def findRoom(self, name):
        for room in self.rooms:
            if room['navn'] == name:
                return room
        return None

    def setStartRoom(self,name):
        self.startRoomName = name

    def run(self):
        stop = False

        clock = pygame.time.Clock()
        startRoom = self.findRoom(self.startRoomName)

        if startRoom == None:
            print("Der var intet 'start' rum")
            self.end()

        currentRoom = startRoom

        room = 1
        while not stop:
            ## Paint the dungeon
            self.setView( currentRoom['gang'] )

            ## Set the text
            self.setText( currentRoom['text'] )

            ## deal with the keys
            sti = currentRoom['sti']
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key in sti:
                        if sti[event.key] == "exit": #special case
                            self.end()
                        
                        currentRoom = self.findRoom( sti[event.key] )
                        
            if currentRoom == None:
                print("Room was 'None'")
                self.end()

            self.paint()
        clock.tick(60)





    def loadResources(self):

        #pygame.font.init()
        self.myfont = pygame.font.SysFont('Monospaced', 14)

        outsidePath = self.resourcePath+"outside.png"
        path = self.resourcePath + "wall_grey.png"

        self.background = [
            
            self._flipImage(self._loadPartialImage(path, 0,0, 176, 120)),
            self._loadPartialImage(path, 0,0, 176, 120),
        ]

        self.game_area = pygame.Surface((self.background[0].get_width(), self.background[0].get_height()), pygame.SRCALPHA)

        doorTemp1 = pygame.Surface( (128,96), pygame.SRCALPHA )
        doorTemp1.blit( self._loadPartialImage(path, 240,  120*3,  128, 96),  (0,0)  )
        doorTemp1.blit( self.doorGfx,  (30,9)  )

        doorTemp2 = pygame.Surface( (80,64), pygame.SRCALPHA )
        doorTemp2.blit( self._loadPartialImage(path, 160,  120*3,  80, 64),  (0,0)  )
        doorTemp2.blit( pygame.transform.scale(self.doorGfx, (50, 47)),  (15,7)  )

        doorTemp3 = pygame.Surface( (48,40), pygame.SRCALPHA )
        doorTemp3.blit( self._loadPartialImage(path, 112,  120*3,  48, 40),  (0,0)  )
        doorTemp3.blit( pygame.transform.scale(self.doorGfx, (32, 30)),  (8,4)  )

        self.doorFrame = [
            [None, None],
            [self._loadPartialImage(path, 240,  120*3,  128, 96), doorTemp1],
            [self._loadPartialImage(path, 160,  120*3,   80, 64), doorTemp2], # no locked door here..
            [self._loadPartialImage(path, 112,  120*3,   48, 40), doorTemp3], # no locked door here..
        ]

        self.outsideWall = [
                None,
                self._loadPartialImage(outsidePath, 240,  0,  128, 96),
                self._loadPartialImage(outsidePath, 160,  0,   80, 64),
                self._loadPartialImage(outsidePath, 112,  0,   48, 40),
        ]

        self.walls = [
            [
                None,
                self._loadPartialImage(path, 240,  120,  128, 96),
                self._loadPartialImage(path, 160,  120,   80, 64),
                self._loadPartialImage(path, 112,  120,   48, 40),
            ],
            [
                None,
                self._loadPartialImage(path, 240,  240,  128, 96),
                self._loadPartialImage(path, 160,  240,   80, 64),
                self._loadPartialImage(path, 112,  240,   48, 40),
            ],
        ]

        self.walls_left = [
        [
            self._loadPartialImage(path, 0,        120, 24, 120),
            self._loadPartialImage(path, 24,       120, 24, 120),
            self._loadPartialImage(path, 24+24,    120, 16, 120),
            self._loadPartialImage(path, 24+24+16, 120,  8, 120),
        ],
        [
            self._loadPartialImage(path, 0,        240, 24, 120),
            self._loadPartialImage(path, 24,       240, 24, 120),
            self._loadPartialImage(path, 24+24,    240, 16, 120),
            self._loadPartialImage(path, 24+24+16, 240,  8, 120),
        ],
        ]

        self.walls_right = [
        [
            self._flipImage(self.walls_left[0][0]),
            self._flipImage(self.walls_left[0][1]),
            self._flipImage(self.walls_left[0][2]),
            self._flipImage(self.walls_left[0][3]),
        ],
        [
            self._flipImage(self.walls_left[1][0]),
            self._flipImage(self.walls_left[1][1]),
            self._flipImage(self.walls_left[1][2]),
            self._flipImage(self.walls_left[1][3]),
        ],
        ]

    def _loadPartialImage(self, str, x, y, width, height):
        temp = pygame.Surface((width, height), pygame.SRCALPHA)
        img = pygame.image.load(str)
        temp.blit(img, (0, 0), (x, y, width, height) )
        return temp

    def _flipImage(self, img):
        return pygame.transform.flip(img, True, False)

    def setText(self, t):
        self.text = t
        return self.text

    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
        rect = Rect(rect)
        y = rect.top
        lineSpacing = 0
        fontHeight = font.size("Tg")[1]
        while text:
            i = 1
            if y + fontHeight > rect.bottom:
                break
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[i:]
        return y-rect.top # return the total height

    def paint(self):
        background = self.background
        game_area = self.game_area
        doublebuffer = self.doublebuffer
        gameDisplay = self.gameDisplay

        currentTileset = 0

        pygame.draw.rect(game_area, (22,22,22), (0,0,220,150), width=0)

        DISTANCE_FAR = 3
        DISTANCE_MEDIUM = 2
        DISTANCE_CLOSE = 1
        DISTANCE_HERE = 0

        background = self.background[currentTileset]
        game_area.blit( background, (0,0), (0,0, background.get_width(), background.get_height())  )



        wall_width = self.walls[currentTileset][DISTANCE_FAR].get_width()
        start_x = background.get_width() / 2 - (wall_width * 5)/2
        start_y = background.get_height() / 2 - 35 - 1
        for x in range(0,5):
            cell = self.view[0][x]
            if (cell > 0):
                sw = self.walls[currentTileset][DISTANCE_FAR]
                if cell == 2: sw = self.outsideWall[DISTANCE_FAR]
                if cell == 3: sw = self.doorFrame[DISTANCE_FAR][0]
                if cell == 4: sw = self.doorFrame[DISTANCE_FAR][1]
                game_area.blit(sw, (start_x + x * wall_width, start_y), (0,0,sw.get_width(),sw.get_height()) )
            if (cell == 0):
                if x <= 2 and x > 0 and self.view[0][x-1] > 0:
                    sw = self.walls_left[currentTileset][DISTANCE_FAR]
                    game_area.blit( sw , (start_x + x * wall_width, start_y ), (0,0,sw.get_width(),sw.get_height()) )
                if x >= 2 and x < 4 and self.view[0][x+1] > 0:
                    sw = self.walls_right[currentTileset][DISTANCE_FAR]
                    game_area.blit( sw , (start_x + x * wall_width + (wall_width - sw.get_width()) , start_y ), (0,0,sw.get_width(),sw.get_height()) )



        wall_width = self.walls[currentTileset][DISTANCE_MEDIUM].get_width()
        start_x = background.get_width() / 2 - (wall_width * 5)/2
        start_y = background.get_height() / 2 - 35 - 8
        for x in range(0,5):
            cell = self.view[1][x]
            if (cell > 0):
                sw = self.walls[currentTileset][DISTANCE_MEDIUM]
                if cell == 2: sw = self.outsideWall[DISTANCE_MEDIUM]
                if cell == 3: sw = self.doorFrame[DISTANCE_MEDIUM][0]
                if cell == 4: sw = self.doorFrame[DISTANCE_MEDIUM][1]
                game_area.blit(sw, (start_x + x * wall_width, start_y), (0,0,sw.get_width(),sw.get_height()) )
            if (cell == 0):
                if x <= 2 and x > 0 and self.view[1][x-1] > 0:
                    sw = self.walls_left[currentTileset][DISTANCE_MEDIUM]
                    game_area.blit( sw , (start_x + x * wall_width, start_y ), (0,0,sw.get_width(),sw.get_height()) )
                if x >= 2 and x < 4 and self.view[1][x+1] > 0:
                    sw = self.walls_right[currentTileset][DISTANCE_MEDIUM]
                    game_area.blit( sw , (start_x + x * wall_width + (wall_width - sw.get_width()) , start_y ), (0,0,sw.get_width(),sw.get_height()) )


        wall_width = self.walls[currentTileset][DISTANCE_CLOSE].get_width()
        start_x = background.get_width() / 2 - (wall_width * 5)/2
        start_y = background.get_height() / 2 - 35 - 16
        for x in range(0,5):
            cell = self.view[2][x]
            if (cell > 0):
                sw = self.walls[currentTileset][DISTANCE_CLOSE]
                if cell == 2: sw = self.outsideWall[DISTANCE_CLOSE]
                if cell == 3: sw = self.doorFrame[DISTANCE_CLOSE][0]
                if cell == 4: sw = self.doorFrame[DISTANCE_CLOSE][1]
                game_area.blit(sw, (start_x + x * wall_width, start_y-1), (0,0,sw.get_width(),sw.get_height()) )
            if (cell == 0):
                if x <= 2 and x > 0 and self.view[2][x-1] > 0:
                    sw = self.walls_left[currentTileset][DISTANCE_CLOSE]
                    game_area.blit( sw , (start_x + x * wall_width, start_y ), (0,0,sw.get_width(),sw.get_height()) )
                if x >= 2 and x < 4 and self.view[2][x+1] > 0:
                    sw = self.walls_right[currentTileset][DISTANCE_CLOSE]
                    game_area.blit( sw , (start_x + x * wall_width + (wall_width - sw.get_width()) , start_y ), (0,0,sw.get_width(),sw.get_height()) )


        if self.view[3][1] > 0:
            sw = self.walls_left[currentTileset][DISTANCE_HERE]
            game_area.blit( sw , ( 0, 0 ), (0,0,sw.get_width(),sw.get_height()) )
        if self.view[3][3] > 0:
            sw = self.walls_right[currentTileset][DISTANCE_HERE]
            game_area.blit( sw , ( background.get_width()-sw.get_width(), 0 ), (0,0,sw.get_width(),sw.get_height()) )


        # game_area
        doublebuffer.blit( self.uiBg, (0,0), (0,0, self.uiBg.get_width(), self.uiBg.get_height())  )
        pygame.draw.rect(doublebuffer, (0,0,0), (10,10, game_area.get_width()+10,game_area.get_height()+10), width=0)
        doublebuffer.blit( game_area, (15,15) )


        # text_area
        start_x = game_area.get_width()+10+10+10
        start_y = 10
        w = doublebuffer.get_width() - start_x - 10
        h = doublebuffer.get_height() - 20
        pygame.draw.rect(doublebuffer, (0,0,0), (start_x, start_y, w, h), width=0)

        y = start_y + 5
        for t in self.text:
            height = self.drawText(doublebuffer, 
                        t, 
                        (255,255,255), 
                        (start_x+5, y, w-10, h-10), 
                        self.myfont, True) + 5
            y = y + height # move down
            h = h - height # but less space available

        gameDisplay.blit( pygame.transform.scale(doublebuffer, gameDisplay.get_rect().size), (0, 0))
        #gameDisplay.blit( doublebuffer, (0,0))
        pygame.display.flip()

    def getView(self):
        return self.view

    def setView(self, view):
        self.view = view

    def end(self):
        pygame.quit()
        exit()
