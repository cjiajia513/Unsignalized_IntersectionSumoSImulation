import traci
import random
import math
import xml.etree.ElementTree as ET

import cpm_cfg as conf
import shutil
import glob
import os


output_dir = './output'

# Check if the output directory exists, if not, create it
# Define the current directory and the output directory
current_dir = '.' # or specify the directory where your files are
output_dir = './output'

# Make sure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"The directory {output_dir} was created.")
else:
    print(f"The directory {output_dir} already exists.")
    
# 初始化仿真参数
sumoBinary = "sumo-gui"  # 使用图形界面进行仿真，可视化车辆运动
sumoCmd = [sumoBinary, "-c", "sumo.sumocfg"]

# 启动仿真
traci.start(sumoCmd)

# 交叉路口中心的坐标（示例值，根据实际仿真环境替换）
intersection_center = (0, 0)
# 检查范围的半径
check_radius = 200

# 交叉路口中的车辆及其轨迹
intersection_vehicles = {}

# 从路由文件中读取路由ID列表
rou_xml = ET.parse('intersection.rou.xml')
routes = rou_xml.getroot()
route_ids = [route.attrib['id'] for route in routes if route.tag == 'route']

net_xml = ET.parse('intersection.net.xml')
nets = net_xml.getroot()
for junction in nets.findall('junction'):
    junction_id = junction.get('id')
    print(junction_id)
# 生成车辆的函数
# Initialize a global counter for vehicle IDs
# Global vehicle ID counter
vehicle_id_counter = 0

def generate_vehicle(vehicle_type, route_ids):
    global vehicle_id_counter  # Use the global counter
    vehicle_id_base = "veh"
    vehicle_id = vehicle_id_base + str(vehicle_id_counter)
    
    # Ensure the generated vehicle_id is unique
    while vehicle_id in traci.vehicle.getIDList():
        # If the vehicle_id exists, increment the counter and generate a new one
        vehicle_id_counter += 1
        vehicle_id = vehicle_id_base + str(vehicle_id_counter)
    
    route_id = random.choice(route_ids)  # Randomly choose a route ID from the route list
    
    # Add the vehicle with the given type to the simulation
    traci.vehicle.add(vehicle_id, route_id, typeID=vehicle_type)
    
    # Equip the vehicle with an SSM (Safety Surrogate Measures) device
    # This assumes that the SSM device is properly configured in SUMO to accept these parameters
    # ssm_output_file = f"ssm_output_{vehicle_id}.xml"
    # traci.vehicle.setParameter(vehicle_id, "has.ssm.device", ssm_output_file)
    
    vehicle_id_counter += 1  # Increment the counter for the next vehicle
    return vehicle_id

# 计算两点之间的距离的函数
def calculate_distance(pos_a, pos_b):
    return math.sqrt((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)














# Define the function to check if a vehicle is approaching the junction
def vehicle_approaching_junction(vehicle_id, junction_id):
    # Get the vehicle's route (list of edges)
    route = traci.vehicle.getRoute(vehicle_id)
    # Get the current edge index in the route
    route_index = traci.vehicle.getRouteIndex(vehicle_id)
    # Get the current lane ID
    current_lane_id = traci.vehicle.getLaneID(vehicle_id)
    
    # If the vehicle is not at the last edge of the route
    if route_index < len(route) - 1:
        next_lane_id = route[route_index+1]
        approaching = True
    else:
        # The vehicle is at the last edge of the route, no next edge
        next_lane_id = None
        approaching = False

    return current_lane_id, next_lane_id, approaching

maxVehicleNumber = 100
# 无限循环，直到手动停止
try:
    while True :
        traci.simulationStep()  # 进行下一个仿真步骤
        if traci.simulation.getMinExpectedNumber() < maxVehicleNumber:
            new_vehicle_id = generate_vehicle(vehicle_type= "passenger", route_ids=route_ids)
        
        # 检查并更新交叉路口中的车辆
        for new_vehicle_id in traci.vehicle.getIDList():
            position = traci.vehicle.getPosition(new_vehicle_id)
            distance = calculate_distance(position, intersection_center)
            print(f"The distance = {distance}")
            # check is approch the junction
            current_lane_id, next_lane_id, approaching = vehicle_approaching_junction(new_vehicle_id, 'intersection')

            # 如果车辆进入交叉路口200米范围内
            if distance < check_radius :
                if new_vehicle_id not in intersection_vehicles:
                    intersection_vehicles[new_vehicle_id] = []
                intersection_vehicles[new_vehicle_id].append(position)
                
                if approaching:
                    print(f"Vehicle {new_vehicle_id} is approaching the junction 'intersection'.")
                    print(f"Current lane ID: {current_lane_id}")
                    
                    traci.vehicle.setColor(new_vehicle_id, (255, 0,0, 255))  # red
                else:
                    traci.vehicle.setColor(new_vehicle_id, (128,128,128, 255)) # gray

            # 如果车辆离开交叉路口200米范围外
            elif new_vehicle_id in intersection_vehicles and distance >= check_radius:
                # 这里可以做额外的处理，例如保存轨迹数据到文件
                del intersection_vehicles[new_vehicle_id]

except KeyboardInterrupt:
    # 关闭TraCI连接
    # Find all files in the current directory that match the 'ssm*.xml' pattern
    file_pattern = os.path.join(current_dir, 'ssm*.xml')
    ssm_files = glob.glob(file_pattern)

    # Move each file to the output directory
    for file_path in ssm_files:
        # Extract the file name from the full file path
        file_name = os.path.basename(file_path)
        # Define the new file path in the output directory
        new_file_path = os.path.join(output_dir, file_name)
        # Move the file
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_path} to {new_file_path}")
    traci.close()