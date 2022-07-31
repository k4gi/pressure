from __future__ import annotations
from typing import Iterator, List, Tuple, TYPE_CHECKING
from game_map import GameMap
import tile_types
import random
import tcod
if TYPE_CHECKING:
	from entity import Entity


class RectangularRoom:
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height

	@property
	def centre(self) -> Tuple[int, int]:
		centre_x = int((self.x1 + self.x2) / 2)
		centre_y = int((self.y1 + self.y2) / 2)
		return centre_x, centre_y

	@property
	def inner(self) -> Tuple[slice, slice]:
		inner_x = slice(self.x1 +1, self.x2)
		inner_y = slice(self.y1 +1, self.y2)
		return inner_x, inner_y

	def intersects(self, other: RectangularRoom) -> bool:
		return (
			self.x1 <= other.x2 and
			self.x2 >= other.x1 and
			self.y1 <= other.y2 and
			self.y2 >= other.y1
		)


def tunnel_between( start: Tuple[int, int], end: Tuple[int, int] ) -> Iterator[Tuple[int, int]]:
	"""return an L-shaped tunnel between two points"""
	x1, y1 = start
	x2, y2 = end

	if random.random() < 0.5:
		#horizontally then vertically
		corner_x, corner_y = x2, y1
	else:
		corner_x, corner_y = x1, y2

	for x, y in tcod.los.bresenham( (x1,y1), (corner_x,corner_y) ).tolist():
		yield x, y
	for x, y in tcod.los.bresenham( (corner_x,corner_y), (x2,y2) ).tolist():
		yield x, y


def generate_dungeon(
	map_width: int,
	map_height: int,
	max_rooms: int,
	room_min_size: int,
	room_max_size: int,
	player: Entity,
) -> GameMap:
	dungeon = GameMap(map_width, map_height)
	rooms: List[RectangularRoom] = []

	for r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)

		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height - 1)

		new_room = RectangularRoom(x, y, room_width, room_height)

		if any(new_room.intersects(other_room) for other_room in rooms):
			continue #don't use this room

		dungeon.tiles[new_room.inner] = tile_types.floor

		if len(rooms) == 0:
			player.x, player.y = new_room.centre
		else:
			for x, y in tunnel_between(rooms[-1].centre, new_room.centre):
				dungeon.tiles[x,y] = tile_types.floor

		rooms.append(new_room)

	return dungeon


def generate_test_dungeon(map_width, map_height) -> GameMap:
	dungeon = GameMap(map_width,map_height)

	room_1 = RectangularRoom(x=0,y=0,width=4,height=4)
	room_2 = RectangularRoom(x=6,y=4,width=4,height=4)

	dungeon.tiles[room_1.inner] = tile_types.floor
	dungeon.tiles[room_2.inner] = tile_types.floor

	for x, y in tunnel_between(room_1.centre, room_2.centre):
		dungeon.tiles[x, y] = tile_types.floor

	return dungeon

