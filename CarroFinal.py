import tkinter as tk
import math
import time
import random

class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
        self.last_output = 0

    def compute(self, error, dt):
        if dt <= 0:
            derivative = 0
        else:
            derivative = (error - self.prev_error) / dt * 0.7
        self.integral = max(-50, min(self.integral + error * dt, 50))
        raw_output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        smoothed_output = 0.3 * raw_output + 0.7 * self.last_output
        self.last_output = smoothed_output
        self.prev_error = error
        return smoothed_output

class LineFollowerCar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.car_x = 150
        self.car_y = 355
        self.car_angle = 0
        self.speed = 1.5
        self.sensor_distance = 30
        self.sensor_offset = 20
        self.pid = PIDController(3, 0.00001, 0.00001)
        self.last_time = time.time()
        self.trail = []
        self.last_angle_change = 0
        self.max_turn_rate = 3.0
        self.stopping = False
        self.pause_until = None
        self.station_name = None
        self.visited_control = False

        self.body = self.create_car_body()
        self.left_wheel = self.create_wheel()
        self.right_wheel = self.create_wheel()
        self.sensor_left = self.create_sensor()
        self.sensor_right = self.create_sensor()
        self.update_car()

    def create_car_body(self):
        return self.canvas.create_polygon(
            0, 0, 20, -15, 40, 0, 20, 30,
            fill='#1ABC9C', outline='#117864', width=2
        )

    def create_wheel(self):
        return self.canvas.create_oval(0, 0, 12, 12, fill='#2C3E50', outline='#1B2631')

    def create_sensor(self):
        return self.canvas.create_oval(0, 0, 10, 10, fill='#E74C3C', outline='#922B21', width=2)

    def update_car(self):
        points = [(0, 0), (20, -15), (40, 0), (20, 30)]
        angle = math.radians(self.car_angle)
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        body_coords = []
        for px, py in points:
            x = self.car_x + px * cos_a - py * sin_a
            y = self.car_y + px * sin_a + py * cos_a
            body_coords.extend([x, y])
        self.canvas.coords(self.body, *body_coords)

        self._update_wheel(self.left_wheel, -10, angle)
        self._update_wheel(self.right_wheel, 10, angle)

        sl, sr = self.get_sensor_positions()
        self.canvas.coords(self.sensor_left, sl[0]-5, sl[1]-5, sl[0]+5, sl[1]+5)
        self.canvas.coords(self.sensor_right, sr[0]-5, sr[1]-5, sr[0]+5, sr[1]+5)

    def _update_wheel(self, wheel, offset, angle):
        x = self.car_x + offset * math.sin(angle)
        y = self.car_y - offset * math.cos(angle)
        self.canvas.coords(wheel, x-6, y-6, x+6, y+6)

    def get_sensor_positions(self):
        a = math.radians(self.car_angle)
        fx = self.car_x + self.sensor_distance * math.cos(a)
        fy = self.car_y + self.sensor_distance * math.sin(a)
        ls = (fx - self.sensor_offset * math.sin(a), fy + self.sensor_offset * math.cos(a))
        rs = (fx + self.sensor_offset * math.sin(a), fy - self.sensor_offset * math.cos(a))
        return ls, rs

    def move(self):
        now = time.time()
        dt = now - self.last_time if now - self.last_time > 0 else 1e-3
        self.last_time = now

        sl, sr = self.get_sensor_positions()
        sc = ((sl[0] + sr[0]) / 2, (sl[1] + sr[1]) / 2)

        if self.pause_until:
            if time.time() < self.pause_until:
                self.canvas.create_text(self.car_x, self.car_y - 30,
                                        text=f"Estación: {self.station_name}",
                                        font=("Arial", 10, "bold"), fill="blue")
                return
            else:
                self.pause_until = None
                self.station_name = None

        if not self.visited_control:
            for name, rect in station_bars.items():
                if name == "Control":
                    if any(rect in self.canvas.find_overlapping(x-5, y-5, x+5, y+5) for x, y in [sl, sr]):
                        self.pause_until = time.time() + 3
                        self.station_name = "Control"
                        self.visited_control = True
                        return

        left_active = self.check_sensor(*sl)
        right_active = self.check_sensor(*sr)
        center_active = self.check_sensor(*sc)

        state = 'none'
        if left_active and right_active:
            state = 'both'
        elif left_active:
            state = 'left'
        elif right_active:
            state = 'right'
        elif center_active:
            state = 'center'

        if state == 'none':
            self.speed = 0.8
            if time.time() - self.last_angle_change > 0.5:
                self.last_angle_change = time.time()
                self.car_angle += 2 if int(time.time()*2)%2==0 else -2
        else:
            self.speed = 1.5 if state == 'both' else 1.3 if state == 'center' else 1.0
            error = {'left': 3, 'right': -3, 'center': 0.5 * self.pid.prev_error}.get(state, 0)
            steering = self.pid.compute(error, dt)
            steering = max(-self.max_turn_rate, min(steering, self.max_turn_rate))
            self.car_angle += steering

        rad = math.radians(self.car_angle)
        self.car_x = max(20, min(self.car_x + self.speed * math.cos(rad), 780))
        self.car_y = max(20, min(self.car_y + self.speed * math.sin(rad), 580))
        self.trail.append((self.car_x, self.car_y))
        if len(self.trail) > 100:
            self.trail.pop(0)
        self.update_car()

    def check_sensor(self, x, y):
        overlap = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        return guide_line in overlap

# ---------- Interfaz ----------
window = tk.Tk()
window.title("Seguidor de Línea - Pista Laberinto")
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

canvas.create_rectangle(0, 0, 800, 600, fill='#D5F5E3')
canvas.create_text(400, 30, text="Pista personalizada estilo laberinto", font=("Arial",14,"bold"))

track_points = [
    (150, 350), (180, 330), (200, 310), (220, 280),
    (250, 250), (280, 240), (300, 250), (320, 270), (340, 300),
    (360, 320), (380, 330), (400, 320), (420, 300), (440, 270),
    (460, 250), (480, 240), (510, 250), (530, 270), (550, 300),
    (570, 320), (590, 330), (610, 320), (630, 300), (650, 270),
    (670, 250), (700, 240), (720, 250), (740, 270), (760, 300),
    (780, 330), (760, 360), (740, 390), (720, 420), (700, 450),
    (670, 470), (630, 480), (590, 470), (550, 460), (510, 450),
    (470, 440), (430, 430), (390, 420), (350, 410), (310, 400),
    (270, 390), (230, 380), (200, 375), (170, 370), (160, 360),
    # curva corregida sin puente
    (150, 350)
]

canvas.create_line(track_points, fill='#566573', width=30, smooth=True)
guide_line = canvas.create_line(track_points, fill='black', width=15, smooth=True)

# Marcar la curva especial
canvas.create_text(170, 360, text="Curva cerrada", font=("Arial", 10, "bold"), fill="red")

stations = {
    "Gasolinera": (550, 200),
    "Mantenimiento": (250, 200),
    "Control": (400, 530)
}
station_bars = {}
for name, (x, y) in stations.items():
    canvas.create_oval(x-20, y-20, x+20, y+20, fill='#58D68D', outline='#196F3D', width=3)
    canvas.create_text(x, y-30, text=name, font=("Arial", 10, "bold"))
    station_bars[name] = canvas.create_rectangle(x-25, y-5, x+25, y+5, fill='', outline='')

car = LineFollowerCar(canvas)

def game_loop():
    car.move()
    if random.random() > 0.5 and not car.stopping:
        canvas.create_oval(car.car_x-1, car.car_y-1, car.car_x+1, car.car_y+1, fill='#F39C12', outline='')
    window.after(30, game_loop)

game_loop()
window.mainloop()
