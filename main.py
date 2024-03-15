from message_com import MessageCom
from CAV_vehicle import A_vehicle
from us_intersection import US_Intersection
from IntersectionPolicyNego import ICpolicy
from AVTrajectory import Trajectory
import cpm_log as logger

import cpm_cfg as conf

logger = logger.Cpmlog().get_logger()




if __name__ == '__main__':
    intersection = US_Intersection(conf.intersetionLocation, max_vehicles=conf.SimulateVehicleNumber)
    comms = MessageCom(broker=conf.mqtt_broker, port=conf.mqtt_port, topic=conf.mqtt_topic)
    comms.connect()
    
    vehicle_count = conf.SimulateVehicleNumber
    # for i in range(vehicle_count):
    #     location = "loc" +str(i+1)
    #     vehicle = A_vehicle(identifier = f"Vehicle{i + 1}", comms=comms, intersection=intersection, location = )
    trajectory1 = Trajectory(width=conf.intersectionWidth, speed_min=conf.AVMinSpeed, speed_max=conf.AVMaxSpeed, controlRegion=conf.intersectionControlRedius)
    start_x1, start_y1,direction1, speed1 = trajectory1.generate_trajectory()
    
    trajectory2 = Trajectory(width=conf.intersectionWidth, speed_min=conf.AVMinSpeed, speed_max=conf.AVMaxSpeed,controlRegion=conf.intersectionControlRedius)
    start_x2, start_y2,direction2, speed2 = trajectory2.generate_trajectory()
     
    # Create vehicles
    vehicle1 = A_vehicle(identifier="Vehicle1", comms=comms, intersection=intersection, location = (start_x1, start_y1))
    vehicle2 = A_vehicle(identifier="Vehicle2", comms=comms, intersection=intersection, location = (start_x2, start_y2))

    # Add vehicles to the intersection
    intersection.add_vehicle(vehicle1)
    intersection.add_vehicle(vehicle2)

    # Simulate vehicles approaching the intersection
    vehicle1.approach_intersection()
    vehicle2.approach_intersection()

    # Simulate vehicles entering the intersection
    vehicle1.enter_intersection()
    vehicle2.enter_intersection()

    comms.disconnect()