from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

app = FastAPI(title="时间管理数据API", description="FastAPI版本")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Mysql#123..'),
    'database': os.getenv('DB_NAME', 'tmp'),
    'charset': 'utf8mb4',
    'autocommit': True
}

# 数据模型
class DashboardData(BaseModel):
    currentday_focus_hour: float
    this_week_completion_rate: float
    time_utilization_efficiency: float
    work_hour: float
    study_hour: float
    sport_hour: float
    read_hour: float
    rest_hour: float
    social_hour: float

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

@app.get("/")
async def root():
    return {"message": "时间管理数据API - FastAPI版本"}

@app.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard_data():
    """获取仪表板数据"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            currentday_focus_hour,
            This_week_completion_rate as this_week_completion_rate,
            time_utilization_efficiency,
            work_hour,
            study_hour,
            sport_hour,
            read_hour,
            rest_hour,
            social_hour
        FROM realtime_ads_current_dashboard_v1_a_dy 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        if not result:
            # 返回默认数据
            return DashboardData(
                currentday_focus_hour=6.5,
                this_week_completion_rate=87.0,
                time_utilization_efficiency=92.0,
                work_hour=4.5,
                study_hour=2.0,
                sport_hour=1.0,
                read_hour=1.5,
                rest_hour=2.5,
                social_hour=1.0
            )
        
        return DashboardData(**result)
        
    except Error as e:
        raise HTTPException(status_code=500, detail=f"查询数据失败: {str(e)}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.get("/api/health")
async def health_check():
    """健康检查"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return {"status": "healthy", "database": "connected"}
        except Error:
            return {"status": "unhealthy", "database": "error"}
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return {"status": "unhealthy", "database": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)