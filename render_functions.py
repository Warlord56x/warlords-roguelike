from __future__ import annotations

from typing import Dict, Tuple, List, TYPE_CHECKING
from entity import Entity, Actor, Item

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def get_entities_at_location(x: int, y: int, game_map: GameMap) -> List[Entity]:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return []

    entities: List[Entity] = []

    for entity in game_map.entities:
        if entity.x == x and entity.y == y:
            entities.append(
                entity
            )

    return entities


def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int


) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width,
                      height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )


def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")


def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)


def render_info_at_mouse_location(
    console: Console, engine: Engine
) -> None:
    x, y = engine.mouse_location

    entities_at_mouse_location = get_entities_at_location(
        x=x, y=y, game_map=engine.game_map
    )

    if len(entities_at_mouse_location) != 0:
        x = x + 1
        y = y - 1

        minwidth = 9
        height = 5
        stacking = False

        for_stack = []

        for entity in entities_at_mouse_location:
            if len(entity.name) > minwidth:
                minwidth = len(entity.name)
            if isinstance(entity, Actor) and entity.ai != None:
                height += 1
            if len(for_stack) > 0 and entity.name == for_stack[-1][0].name:
                for_stack[-1][1] += 1
                stacking = True
            else:
                ent_dict: List[Entity, int] = [entity, 0]
                for_stack.append(ent_dict)

        if stacking:
            minwidth += 3

        if x + minwidth + 2 > console.width:
            x -= minwidth + 3

        console.draw_frame(
            x=x,
            y=y,
            width=minwidth + 2,
            height=len(entities_at_mouse_location) + height,
            title="Info",
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )
        y += 1

        for entity, stack in for_stack:
            if stack > 0:
                console.print(x=x + 1, y=y, string=entity.name +
                              " x" + str(stack + 1))
            else:
                console.print(x=x + 1, y=y, string=entity.name)
            y += 1
            if isinstance(entity, Actor) and entity.ai != None:
                y += 1
                console.print(
                    x=x + 1, y=y, string=str(entity.fighter.hp) + "/" + str(entity.fighter.max_hp))
                y += 1
                console.print(x=x + 1, y=y, string="Defense:" +
                              str(entity.fighter.defense))
                y += 1
                console.print(x=x + 1, y=y, string="Power:" +
                              str(entity.fighter.power))
            last = entity
