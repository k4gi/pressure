from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
	keymap = {
		"move_up": [tcod.event.K_UP, tcod.event.K_w, tcod.event.K_k],
		"move_down": [tcod.event.K_DOWN, tcod.event.K_s, tcod.event.K_j],
		"move_left": [tcod.event.K_LEFT, tcod.event.K_a, tcod.event.K_h],
		"move_right": [tcod.event.K_RIGHT, tcod.event.K_d, tcod.event.K_l],
		"escape": [tcod.event.K_ESCAPE],
	}

	def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
		raise SystemExit()

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
		action: Optional[Action] = None

		key = event.sym

		if key in self.keymap["move_up"]:
			action = MovementAction(dx=0, dy=-1)
		elif key in self.keymap["move_down"]:
			action = MovementAction(dx=0, dy=1)
		elif key in self.keymap["move_left"]:
			action = MovementAction(dx=-1, dy=0)
		elif key in self.keymap["move_right"]:
			action = MovementAction(dx=1, dy=0)

		elif key in self.keymap["escape"]:
			action = EscapeAction()

		return action

