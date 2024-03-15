import json
import time
import numpy as np
class A_vehicle:
    def __init__(self, identifier, comms, intersection, location):
        self.identifier = identifier
        self.comms = comms
        self.intersection = intersection
        self.location = location # current location of this vehicle
    def getID(self):
        return self.identifier
        
    def calculate_distance(self, location1, ISCenter):
        # ISCenter = intersection center
        return np.sqrt((location1[0] - ISCenter[0])**2 + (location1[1] - ISCenter[1])**2)
    
    def update_location(self, new_location):
        self.location = new_location
        distance_to_intersection = self.calculate_distance(self.location, self.intersection.location)

    def approach_intersection(self):
        message = json.dumps({"vehicle_id": self.identifier, "status": "approaching"})
        self.comms.send_message(message)

    def enter_intersection(self):
        if not self.intersection.check_collision():
            message = json.dumps({"vehicle_id": self.identifier, "status": "entering"})
            self.comms.send_message(message)
            time.sleep(1)
            self.leave_intersection()
        else:
            pass  # Add collision handling logic here

    def leave_intersection(self):
        message = json.dumps({"vehicle_id": self.identifier, "status": "leaving"})
        self.comms.send_message(message)