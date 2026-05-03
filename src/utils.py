"""
工具函数模块
"""
import cv2
import numpy as np
import os
from pathlib import Path


def load_images(data_dir):
    """
    从目录加载所有标定图片
    
    Args:
        data_dir: 图片目录路径
    
    Returns:
        图片数组列表
    """
    images = []
    image_files = []
    
    # 支持的图片格式
    supported_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    
    for fmt in supported_formats:
        image_files.extend(Path(data_dir).glob(fmt))
        image_files.extend(Path(data_dir).glob(fmt.upper()))
    
    image_files.sort()
    
    print(f"🔍 找到 {len(image_files)} 张图片")
    
    for img_file in image_files:
        img = cv2.imread(str(img_file), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            print(f"  ✓ 加载: {img_file.name}")
    
    return images


def find_chessboard_corners(images, pattern_size=(8, 6)):
    """
    在标定图片中查找棋盘格角点
    
    Args:
        images: 灰度图像列表
        pattern_size: 棋盘格大小 (宽, 高)
    
    Returns:
        所有找到的角点坐标
    """
    print(f"\n🔎 查找棋盘格角点 (模式: {pattern_size[0]}x{pattern_size[1]})...")
    
    all_corners = []
    all_ids = []
    
    for idx, gray in enumerate(images):
        # 查找棋盘格角点
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        if ret:
            # 精化角点位置
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            all_corners.append(corners_refined)
            all_ids.append(idx)
            print(f"  ✓ 图片 {idx}: 找到 {len(corners)} 个角点")
        else:
            print(f"  ✗ 图片 {idx}: 未找到棋盘格")
    
    print(f"\n✅ 成功检测 {len(all_corners)} 张图片的角点")
    return all_corners, all_ids


def create_object_points(pattern_size=(8, 6), square_size=1.0):
    """
    创建真实世界的棋盘格点坐标
    
    Args:
        pattern_size: 棋盘格大小
        square_size: 棋盘格单位 (如 1.0 表示 1cm)
    
    Returns:
        object_points 数组
    """
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    objp *= square_size
    
    return objp


def ensure_output_dir(output_dir):
    """确保输出目录存在"""
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
