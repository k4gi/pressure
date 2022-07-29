from typing import Tuple
from game_map import GameMap
import tile_types


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


def generate_dungeon(map_width, map_height) -> GameMap:
	dungeon = GameMap(map_width,map_height)

	room_1 = RectangularRoom(x=0,y=0,width=4,height=4)
	room_2 = RectangularRoom(x=6,y=0,width=4,height=4)

	dungeon.tiles[room_1.inner] = tile_types.floor
	dungeon.tiles[room_2.inner] = tile_types.floor

	return dungeon

