#!/usr/bin/env python3


import tcod
from engine import Engine
from input_handlers import EventHandler
from entity import Entity


def main() -> None:
    screen_width = 16
    screen_height = 16

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity( int(screen_width/2), int(screen_height/2), '@', (255,255,255) )
    npc = Entity( int(screen_width/2 -4), int(screen_height/2), '@', (255,255,0) )
    entities = {npc, player}
    
    engine = Engine(entities=entities, event_handler=event_handler, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Pressure",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            
            events = tcod.event.wait()
            engine.handle_events(events)



if __name__ == "__main__":
    main()
