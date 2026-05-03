"""
相机标定核心模块
"""
import cv2
import numpy as np
import json
from utils import create_object_points


class CameraCalibrator:
    """相机标定类"""
    
    def __init__(self, pattern_size=(8, 6), square_size=1.0):
        """
        初始化标定器
        
        Args:
            pattern_size: 棋盘格大小 (宽, 高)
            square_size: 棋盘格单位尺寸
        """
        self.pattern_size = pattern_size
        self.square_size = square_size
        self.pattern_points = create_object_points(pattern_size, square_size)
        
        self.object_points = []
        self.image_points = []
        self.image_shape = None
        
        self.camera_matrix = None
        self.dist_coeffs = None
        self.rvecs = None
        self.tvecs = None
        self.reprojection_error = None
    
    def add_corners(self, image_corners, image_shape):
        """
        添加检测到的角点
        
        Args:
            image_corners: 检测到的角点坐标
            image_shape: 图像尺寸 (height, width)
        """
        self.object_points.append(self.pattern_points)
        self.image_points.append(image_corners)
        self.image_shape = image_shape
    
    def calibrate(self):
        """
        执行标定
        
        Returns:
            标定是否成功
        """
        print("\n📐 开始相机标定...")
        
        if len(self.object_points) < 3:
            print("❌ 错误: 需要至少 3 张图片才能标定")
            return False
        
        try:
            # 执行标定
            ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
                self.object_points,
                self.image_points,
                self.image_shape,
                None,
                None
            )
            
            if ret:
                self.camera_matrix = camera_matrix
                self.dist_coeffs = dist_coeffs
                self.rvecs = rvecs
                self.tvecs = tvecs
                
                # 计算重投影误差
                self._calculate_reprojection_error()
                
                print("✅ 标定成功！")
                return True
            else:
                print("❌ 标定失败")
                return False
                
        except Exception as e:
            print(f"❌ 标定过程出错: {e}")
            return False
    
    def _calculate_reprojection_error(self):
        """计算重投影误差"""
        total_error = 0
        total_points = 0
        
        for i in range(len(self.object_points)):
            proj_points, _ = cv2.projectPoints(
                self.object_points[i],
                self.rvecs[i],
                self.tvecs[i],
                self.camera_matrix,
                self.dist_coeffs
            )
            
            error = cv2.norm(self.image_points[i], proj_points, cv2.NORM_L2) / len(proj_points)
            total_error += error
            total_points += 1
        
        self.reprojection_error = total_error / total_points
        print(f"📊 平均重投影误差: {self.reprojection_error:.4f} 像素")
    
    def get_calibration_result(self):
        """获取标定结果"""
        if self.camera_matrix is None:
            return None
        
        return {
            'camera_matrix': self.camera_matrix.tolist(),
            'distortion_coefficients': self.dist_coeffs.flatten().tolist(),
            'reprojection_error': float(self.reprojection_error),
            'pattern_size': self.pattern_size,
            'square_size': self.square_size,
            'image_shape': list(self.image_shape)
        }
    
    def save_result(self, output_path):
        """
        保存标定结果到文件
        
        Args:
            output_path: 输出文件路径
        """
        result = self.get_calibration_result()
        
        if result is None:
            print("❌ 没有标定结果可保存")
            return False
        
        try:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 标定结果已保存: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
            return False
    
    def print_calibration_result(self):
        """打印标定结果"""
        if self.camera_matrix is None:
            print("❌ 没有标定结果")
            return
        
        print("\n" + "="*50)
        print("🎥 相机标定结果")
        print("="*50)
        
        print("\n📷 相机内参矩阵:")
        print(self.camera_matrix)
        
        print("\n🔧 畸变系数:")
        print(self.dist_coeffs.flatten())
        
        print(f"\n📊 重投影误差: {self.reprojection_error:.4f} 像素")
        
        print(f"\n📐 使用图片数: {len(self.object_points)}")
        print(f"📏 图像分辨率: {self.image_shape[1]}x{self.image_shape[0]}")
        
        print("\n" + "="*50)
