"""
相机标定主程序
使用棋盘格图像标定相机内参和畸变系数
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from calibration import CameraCalibrator
from utils import load_images, find_chessboard_corners, ensure_output_dir
from visualize import draw_chessboard_corners, visualize_calibration_result, create_calibration_report


def main():
    """主函数"""
    
    print("=" * 60)
    print("🎥 相机标定系统")
    print("=" * 60)
    print()
    
    # 配置参数
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
    
    # 棋盘格参数：调整这些参数以匹配你的棋盘格
    PATTERN_SIZE = (8, 6)          # 棋盘格大小 (宽, 高)
    SQUARE_SIZE = 1.0              # 棋盘格单位尺寸（任意单位）
    
    print(f"📁 数据目录: {DATA_DIR}")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📐 棋盘格: {PATTERN_SIZE[0]}x{PATTERN_SIZE[1]}")
    print()
    
    # 步骤 1：加载图片
    print("📥 步骤 1: 加载标定图片")
    print("-" * 60)
    
    if not os.path.exists(DATA_DIR):
        print(f"❌ 错误: 数据目录不存在 {DATA_DIR}")
        print("💡 请先在 data/ 目录下放入棋盘格图片")
        return
    
    images = load_images(DATA_DIR)
    
    if len(images) == 0:
        print("❌ 错误: 没有找到图片文件")
        print("💡 请将棋盘格图片放入 data/ 目录")
        return
    
    if len(images) < 3:
        print("❌ 错误: 需要至少 3 张图片")
        print(f"💡 当前只有 {len(images)} 张图片")
        return
    
    # 步骤 2：检测棋盘格角点
    print("\n📥 步骤 2: 检测棋盘格角点")
    print("-" * 60)
    
    all_corners, all_ids = find_chessboard_corners(images, PATTERN_SIZE)
    
    if len(all_corners) < 3:
        print("❌ 错误: 检测到的有效图片太少")
        print(f"💡 有效图片数: {len(all_corners)}")
        return
    
    # 步骤 3：创建标定器并添加角点
    print("\n📥 步骤 3: 准备标定数据")
    print("-" * 60)
    
    calibrator = CameraCalibrator(PATTERN_SIZE, SQUARE_SIZE)
    
    for img_id, corners in zip(all_ids, all_corners):
        image_shape = images[img_id].shape
        calibrator.add_corners(corners, image_shape)
    
    print(f"✅ 准备了 {len(all_corners)} 张有效图片进行标定")
    
    # 步骤 4：执行标定
    print("\n📥 步骤 4: 执行标定计算")
    print("-" * 60)
    
    success = calibrator.calibrate()
    
    if not success:
        print("❌ 标定失败，请检查图片质量")
        return
    
    # 步骤 5：输出结果
    print("\n📥 步骤 5: 输出结果")
    print("-" * 60)
    
    ensure_output_dir(OUTPUT_DIR)
    
    calibrator.print_calibration_result()
    
    # 保存 JSON 格式结果
    json_path = os.path.join(OUTPUT_DIR, 'calibration_result.json')
    calibrator.save_result(json_path)
    
    # 可视化结果
    print("\n📥 步骤 6: 生成可视化")
    print("-" * 60)
    
    # 选择有效图片进行绘制
    valid_images = [images[idx] for idx in all_ids]
    draw_chessboard_corners(valid_images, all_corners, OUTPUT_DIR)
    visualize_calibration_result(calibrator, valid_images, all_corners, OUTPUT_DIR)
    create_calibration_report(calibrator, all_corners, OUTPUT_DIR)
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 标定完成！")
    print("=" * 60)
    print(f"📊 结果已保存到: {OUTPUT_DIR}")
    print()


if __name__ == '__main__':
    main()
