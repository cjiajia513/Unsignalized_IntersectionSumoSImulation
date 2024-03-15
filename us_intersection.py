from CAV_vehicle import A_vehicle

class US_Intersection:
    def __init__(self, location,max_vehicles):
        self.max_vehicles = max_vehicles
        self.vehicles = {}
        self.location = location

    def add_vehicle(self, A_vehicle):
        if len(self.vehicles) < self.max_vehicles:
            self.vehicles[A_vehicle.getID] = A_vehicle
            
    def check_collision(self):
       return False
