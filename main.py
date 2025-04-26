from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random
import base64

app = FastAPI()

# CORS 中间件配置（必须在 app 实例创建后立刻加）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发阶段用 *）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟设备状态
device_status = {
    "uptime": "24h",
    "cpu": "12%",
    "memory": "45%",
    "status": "online",
    "last_updated": datetime.now().isoformat()
}

# 模拟摄像头图像（实际可替换为读取摄像头内容）
def get_mock_image_base64():
    with open("demo.jpg", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# 获取温度接口
@app.get("/api/temperature")
def get_temperature():
    temp = round(random.uniform(20.0, 30.0), 2)
    return {
        "temperature": temp,
        "unit": "°C",
        "timestamp": datetime.now().isoformat()
    }

# 获取设备状态
@app.get("/api/device/status")
def get_status():
    device_status["last_updated"] = datetime.now().isoformat()
    return device_status

# 获取摄像头图像
@app.get("/api/camera")
def get_camera_image():
    image_base64 = get_mock_image_base64()
    return {
        "image": image_base64,
        "content_type": "image/jpeg",
        "timestamp": datetime.now().isoformat()
    }

# 控制指令 - 重启
class ControlCommand(BaseModel):
    action: str

@app.post("/api/control/restart")
def restart_device(cmd: ControlCommand):
    if cmd.action.lower() == "restart":
        return {
            "status": "ok",
            "message": "设备已收到重启命令",
            "timestamp": datetime.now().isoformat()
        }
    return {
        "status": "ignored",
        "message": "不支持的指令",
    }


