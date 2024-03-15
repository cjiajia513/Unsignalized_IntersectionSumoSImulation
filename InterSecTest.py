import asyncio
import json
import math
import random
import time
import paho.mqtt.client as mqtt

# MQTT Broker的地址和端口
broker_address = "192.168.50.94"
broker_port = 1883

# 车辆数量
num_cars = 5

# 车辆信息
cars = {}

# 订阅的主题
subscribe_topic = "car/+/position"

# 发布的主题
publish_topic = "car/position"

# MQTT回调函数 - 连接成功
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

    # 订阅车辆位置信息主题
    client.subscribe(subscribe_topic)

# MQTT回调函数 - 接收到消息
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    # 解析收到的消息
    car_id = int(topic.split("/")[1])
    data = json.loads(payload)
    
    # 更新车辆信息
    cars[car_id]["position"] = data["position"]
    cars[car_id]["velocity"] = data["velocity"]

# 发布车辆位置信息
async def publish_car_position(client, car_id):
    while True:
        # 随机生成新的位置和速度
        position = random.uniform(0, 100)
        velocity = random.uniform(0, 10)
        
        # 更新车辆信息
        cars[car_id]["position"] = position
        cars[car_id]["velocity"] = velocity
        
        # 构建消息
        message = {
            "position": position,
            "velocity": velocity
        }
        payload = json.dumps(message)
        
        # 发布消息
        client.publish(publish_topic, payload)
        
        # 等待0.1秒
        await asyncio.sleep(0.1)

# 计算车辆之间的距离
async def calculate_distances():
    while True:
        # 计算所有车辆之间的距离
        for i in range(num_cars):
            for j in range(i + 1, num_cars):
                car1 = cars[i]
                car2 = cars[j]
                distance = abs(car1["position"] - car2["position"])
                print(f"Distance between Car {i} and Car {j}: {distance}")
        
        # 等待0.1秒
        await asyncio.sleep(0.1)

# 主函数
def main():
    # 初始化车辆信息
    for i in range(num_cars):
        cars[i] = {
            "position": 0,
            "velocity": 0
        }
    
    # 创建MQTT客户端
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    # 连接到MQTT Broker
    client.connect(broker_address, broker_port, 60)
    
    # 启动异步事件循环
    loop = asyncio.get_event_loop()
    
    try:
        # 启动任务
        tasks = [
            loop.create_task(publish_car_position(client, i)) for i in range(num_cars)
        ]
        tasks.append(loop.create_task(calculate_distances()))
        
        # 开始事件循环
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        pass
    finally:
        # 断开MQTT连接
        client.disconnect()
        loop.close()

if __name__ == "__main__":
    main()