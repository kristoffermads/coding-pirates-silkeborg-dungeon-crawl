import pygame
from pygame.locals import *
from CodingPiratesDungeon import CodingPiratesDungeon, Path, Room

dungeon = CodingPiratesDungeon('./assets/images/', 400, 250, 'EoB Coding Pirates Generator')


"""
dungeon.setDungeon([
    "....................",
    ".........         ..",
    "......... ....... ..",
    "......... ....... ..",
    "......... ....... ..",
    "......... ....... ..",
    "......... ....... ..",
    "......... ...     ..",
    "......... ... ......",
    "......... .1     ....",
    "......... 3     ....",
    "......... .     ....",
    "......... ..........",
    ".........S..........",
    "....................",
])
"""









dungeon.addRoom({
    "navn"  : "start",
    "text"  : [
            "Du er fanget i en grotte - se om du kan komme ud",
            "",
            "Tryk [S] for at vende dig om",
        ], 
    "gang"  : dungeon.ROAD_DOOR_CLOSED,
    "sti"   : {
        pygame.K_s: "gang1"
    },
})

dungeon.addRoom({
    "navn"  : "gang1",
    "text"  : [
            "Gangen fortsætter ud i mørket. Du kan høre en uhyggelig lyd, som knive der skraber mod gulvet..",
            "",
            "Tryk [W] for at gå frem",
            "Tryk [S] for at gå tilbage",
        ], 
    "gang"  : dungeon.ROAD_HALLWAY,
    "sti"   : {
        pygame.K_w: "gang2",
        pygame.K_s: "start"
    }
})

dungeon.addRoom({
    "navn"  : "gang2",
    "text"  : [
            "Vejen deler sig i tre. Mod højre kan du mærke en let brise.",
            "",
            "Tryk [W] for at gå frem",
            "Tryk [S] for at gå tilbage",
            "Tryk [D] for at gå til højre",
            "Tryk [A] for at gå til venstre",
        ], 
    "gang"  : dungeon.ROAD_SPLIT_3,
    "sti"   : {
        pygame.K_w: "gang3",
        pygame.K_s: "gang1",
        pygame.K_d: "gang4",
        pygame.K_a: "udgang"
    }
})

dungeon.addRoom({
    "navn"  : "gang3",
    "text"  : [
            "Øv - en blindgyde..",
            "",
            "Tryk [S] for at gå tilbage til de 3 veje",
        ], 
    "gang"  : dungeon.ROAD_DEADEND,
    "sti"   : {
        pygame.K_s: "gang2"
    }
})

dungeon.addRoom({
    "navn"  : "gang4",
    "text"  : [
            "Øv - en blindgyde.. (2)",
            "",
            "Tryk [S] for at gå tilbage til de 3 veje",
        ], 
    "gang"  : dungeon.ROAD_DEADEND,
    "sti"   : {
        pygame.K_s: "gang2"
    }
})

dungeon.addRoom({
    "navn"  : "udgang",
    "text"  : [
            "Hurra du fandt ud!",
            "",
            "Tryk [S] for at gå tilbage",
            "Tryk [W] for at gå ud",
        ], 
    "gang"  : dungeon.ROAD_OUTSIDE,
    "sti"   : {
        pygame.K_s: "gang2",
        pygame.K_w: "exit",
    }
})

dungeon.setStartRoom("start")

dungeon.run()
