import pyautogui as pag

class mouse_controller:
    def __init__(self, mouse_movement_gesture, ts, wScale=5000, hScale=2000):
        self.prev_index_finger_pos = None
        self.mouse_movement_gesture = mouse_movement_gesture
        self.width_scalar = wScale
        self.height_scalar = hScale
        self.last_movement = ts
        self.TIME_PER_MOVEMENT = 250

    def move_mouse(self, position, curr_gesture, timestamp):
        if curr_gesture != self.mouse_movement_gesture:
            return # if gesture is not mouse movement gesture
        if self.prev_index_finger_pos == None:
            self.prev_index_finger_pos = position
        elif timestamp >= self.last_movement + self.TIME_PER_MOVEMENT:
            x_delta, y_delta = self.calculate_finger_movement(position, self.prev_index_finger_pos)
            pag.moveRel(int(x_delta * self.width_scalar), int(y_delta * self.height_scalar))
            self.prev_index_finger_pos = position
            self.last_movement = timestamp

    def calculate_finger_movement(self, curr_pos, prev_pos):
        return (curr_pos[0] - prev_pos[0]), (curr_pos[1] - prev_pos[1])