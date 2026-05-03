"""
结果可视化模块
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os


# 设置中文字体支持
rcParams['font.sans-serif'] = ['DejaVu Sans']


def draw_chessboard_corners(images, all_corners, output_dir):
    """
    在图像上绘制检测到的角点
    
    Args:
        images: 原始图像列表
        all_corners: 检测到的角点列表
        output_dir: 输出目录
    """
    print("\n🎨 绘制角点检测结果...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, (image, corners) in enumerate(zip(images, all_corners)):
        # 转换为彩色图显示
        image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # 绘制角点
        image_with_corners = cv2.drawChessboardCorners(
            image_color,
            (8, 6),  # 图案大小
            corners,
            True
        )
        
        # 保存结果图
        output_path = os.path.join(output_dir, f"corners_{idx:02d}.jpg")
        cv2.imwrite(output_path, image_with_corners)
        print(f"  ✓ 保存: {output_path}")


def visualize_calibration_result(calibrator, images, all_corners, output_dir):
    """
    可视化标定结果
    
    Args:
        calibrator: CameraCalibrator 对象
        images: 原始图像列表
        all_corners: 检测到的角点
        output_dir: 输出目录
    """
    print("\n📊 生成标定结果可视化...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Camera Calibration Results', fontsize=16, fontweight='bold')
    
    # 1. 显示相机内参矩阵
    ax = axes[0, 0]
    ax.text(0.5, 0.5, 'Camera Matrix\n' + 
            f'fx={calibrator.camera_matrix[0, 0]:.1f}\n' +
            f'fy={calibrator.camera_matrix[1, 1]:.1f}\n' +
            f'cx={calibrator.camera_matrix[0, 2]:.1f}\n' +
            f'cy={calibrator.camera_matrix[1, 2]:.1f}',
            ha='center', va='center', fontsize=12, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax.set_title('Camera Intrinsic Parameters')
    ax.axis('off')
    
    # 2. 显示畸变系数
    ax = axes[0, 1]
    dist_coeffs = calibrator.dist_coeffs.flatten()
    ax.text(0.5, 0.5, 'Distortion Coefficients\n' +
            f'k1={dist_coeffs[0]:.6f}\n' +
            f'k2={dist_coeffs[1]:.6f}\n' +
            f'p1={dist_coeffs[2]:.6f}\n' +
            f'p2={dist_coeffs[3]:.6f}\n' +
            f'k3={dist_coeffs[4]:.6f}',
            ha='center', va='center', fontsize=12, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax.set_title('Distortion Coefficients')
    ax.axis('off')
    
    # 3. 重投影误差
    ax = axes[1, 0]
    ax.text(0.5, 0.5, f'Reprojection Error\n{calibrator.reprojection_error:.4f} pixels',
            ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    ax.set_title('Calibration Quality')
    ax.axis('off')
    
    # 4. 统计信息
    ax = axes[1, 1]
    ax.text(0.5, 0.5, f'Calibration Statistics\n' +
            f'Images used: {len(all_corners)}\n' +
            f'Resolution: {calibrator.image_shape[1]}x{calibrator.image_shape[0]}\n' +
            f'Pattern size: {calibrator.pattern_size[0]}x{calibrator.pattern_size[1]}\n' +
            f'Square size: {calibrator.square_size} units',
            ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
    ax.set_title('Statistics')
    ax.axis('off')
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'calibration_summary.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ 保存: {output_path}")
    plt.close()


def create_calibration_report(calibrator, all_corners, output_dir):
    """
    创建文本格式的标定报告
    
    Args:
        calibrator: CameraCalibrator 对象
        all_corners: 检测到的角点
        output_dir: 输出目录
    """
    print("\n📝 生成标定报告...")
    
    report = []
    report.append("="*60)
    report.append("CAMERA CALIBRATION REPORT")
    report.append("="*60)
    report.append("")
    
    report.append("CAMERA INTRINSIC PARAMETERS")
    report.append("-" * 60)
    report.append("Camera Matrix (K):")
    for row in calibrator.camera_matrix:
        report.append("  " + "  ".join(f"{val:12.4f}" for val in row))
    report.append("")
    
    report.append("Focal lengths:")
    report.append(f"  fx = {calibrator.camera_matrix[0, 0]:.4f}")
    report.append(f"  fy = {calibrator.camera_matrix[1, 1]:.4f}")
    report.append("")
    
    report.append("Principal point:")
    report.append(f"  cx = {calibrator.camera_matrix[0, 2]:.4f}")
    report.append(f"  cy = {calibrator.camera_matrix[1, 2]:.4f}")
    report.append("")
    
    report.append("DISTORTION COEFFICIENTS")
    report.append("-" * 60)
    dist = calibrator.dist_coeffs.flatten()
    report.append(f"  k1 = {dist[0]:12.8f}")
    report.append(f"  k2 = {dist[1]:12.8f}")
    report.append(f"  p1 = {dist[2]:12.8f}")
    report.append(f"  p2 = {dist[3]:12.8f}")
    report.append(f"  k3 = {dist[4]:12.8f}")
    report.append("")
    
    report.append("CALIBRATION QUALITY")
    report.append("-" * 60)
    report.append(f"  Reprojection Error: {calibrator.reprojection_error:.6f} pixels")
    report.append(f"  Images Used: {len(all_corners)}")
    report.append(f"  Image Resolution: {calibrator.image_shape[1]} x {calibrator.image_shape[0]}")
    report.append("")
    
    report.append("CALIBRATION PATTERN")
    report.append("-" * 60)
    report.append(f"  Pattern Size: {calibrator.pattern_size[0]} x {calibrator.pattern_size[1]}")
    report.append(f"  Square Size: {calibrator.square_size}")
    report.append("")
    
    report.append("="*60)
    
    # 保存报告
    report_text = "\n".join(report)
    report_path = os.path.join(output_dir, 'calibration_report.txt')
    with open(report_path, 'w') as f:
        f.write(report_text)
    
    print(f"  ✓ 保存: {report_path}")
    print("\n" + report_text)
