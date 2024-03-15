import random
import math

class Trajectory:
    def __init__(self, width, speed_min, speed_max, controlRegion):
        self.width = width  # 交叉口道路宽度
        self.speed_min = speed_min  # 最小速度（公里每小时）
        self.speed_max = speed_max  # 最大速度（公里每小时）
        self.x = 0
        self.y = 0
        self.direction = None
        self.speed = 0
        self.controlRegion = controlRegion
        self.generate_starting_point()
        self.choose_direction()
        self.set_speed()

    def generate_starting_point(self):
        # 随机选择起始道路（x轴或y轴上）
        on_x_road = random.choice([True, False])

        if on_x_road:
            self.x = random.uniform(-self.width/2, self.width/2)
            self.y = random.choice([-1, 1]) * random.uniform(0, self.controlRegion)
        else:
            self.y = random.uniform(-self.width/2, self.width/2)
            self.x = random.choice([-1, 1]) * random.uniform(0, self.controlRegion)
        return (self.x, self.y)

    def choose_direction(self):
        # 随机选择方向：左转、右转或直行
        self.direction = random.choice(["left", "right", "straight"])

    def set_speed(self):
        # 随机设置速度在速度区间内
        self.speed = random.uniform(self.speed_min, self.speed_max)

    def simulate_movement(self):
        # 根据选择的方向和速度模拟移动
        # 这里只是简单地根据方向更新x或y坐标
        # 实际情况下，可能需要更复杂的逻辑来考虑转弯的动态
        if self.direction == "left":
            self.x -= self.speed / 3.6  # 转换速度到米每秒
            self.y += self.speed / 3.6
        elif self.direction == "right":
            self.x += self.speed / 3.6
            self.y -= self.speed / 3.6
        elif self.direction == "straight":
            if abs(self.x) < abs(self.y):  # 假设在y轴道路上
                self.y += math.copysign(self.speed / 3.6, self.y)
            else:  # 假设在x轴道路上
                self.x += math.copysign(self.speed / 3.6, self.x)

    def generate_trajectory(self):
        # 生成整个轨迹
        self.generate_starting_point()
        self.choose_direction()
        self.set_speed()
        self.simulate_movement()
        return self.x, self.y, self.direction, self.speed

# 用法示例
# trajectory = Trajectory(width=10, speed_min=30, speed_max=60)
# start_x, start_y, direction, speed = trajectory.generate_trajectory()
# print(f"Starting point: ({start_x}, {start_y}), Direction: {direction}, Speed: {speed} km/h")