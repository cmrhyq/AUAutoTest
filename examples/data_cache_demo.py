"""
数据缓存模块使用示例

演示 DataCache 的基本功能和使用方法
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import threading
import time
from core.cache.data_cache import DataCache, get_cache


def basic_usage_demo():
    """基本使用示例"""
    print("=" * 60)
    print("基本使用示例")
    print("=" * 60)
    
    # 获取缓存实例
    cache = DataCache.get_instance()
    
    # 存储不同类型的数据
    cache.set("user_id", 12345)
    cache.set("username", "test_user")
    cache.set("user_data", {"name": "张三", "age": 30, "email": "test@example.com"})
    cache.set("tags", ["python", "testing", "automation"])
    
    print(f"存储的用户ID: {cache.get('user_id')}")
    print(f"存储的用户名: {cache.get('username')}")
    print(f"存储的用户数据: {cache.get('user_data')}")
    print(f"存储的标签: {cache.get('tags')}")
    
    # 检查键是否存在
    print(f"\n'user_id' 是否存在: {cache.has('user_id')}")
    print(f"'nonexistent' 是否存在: {cache.has('nonexistent')}")
    
    # 获取不存在的键（使用默认值）
    print(f"\n获取不存在的键（默认值）: {cache.get('nonexistent', 'default_value')}")
    
    # 查看缓存大小
    print(f"\n缓存中的项目数: {cache.size()}")
    print(f"所有键: {cache.get_all_keys()}")
    
    print()


def singleton_demo():
    """单例模式示例"""
    print("=" * 60)
    print("单例模式示例")
    print("=" * 60)
    
    # 多次获取实例
    cache1 = DataCache.get_instance()
    cache2 = get_cache()
    cache3 = DataCache.get_instance()
    
    # 验证是同一个实例
    print(f"cache1 和 cache2 是同一个实例: {cache1 is cache2}")
    print(f"cache2 和 cache3 是同一个实例: {cache2 is cache3}")
    print(f"实例ID: cache1={id(cache1)}, cache2={id(cache2)}, cache3={id(cache3)}")
    
    # 在一个实例中设置数据
    cache1.set("shared_data", "这是共享数据")
    
    # 在另一个实例中读取
    print(f"\n通过 cache2 读取 cache1 设置的数据: {cache2.get('shared_data')}")
    print(f"通过 cache3 读取 cache1 设置的数据: {cache3.get('shared_data')}")
    
    print()


def update_demo():
    """更新数据示例"""
    print("=" * 60)
    print("更新数据示例")
    print("=" * 60)
    
    cache = DataCache.get_instance()
    cache.clear()
    
    # 首次设置
    cache.set("counter", 0)
    print(f"初始值: {cache.get('counter')}")
    
    # 多次更新
    for i in range(1, 6):
        cache.set("counter", i)
        print(f"更新后的值: {cache.get('counter')}")
    
    print()


def thread_safety_demo():
    """线程安全示例"""
    print("=" * 60)
    print("线程安全示例")
    print("=" * 60)
    
    cache = DataCache.get_instance()
    cache.clear()
    
    num_threads = 5
    operations_per_thread = 10
    
    def worker(thread_id):
        """每个线程执行的工作"""
        for i in range(operations_per_thread):
            key = f"thread_{thread_id}_item_{i}"
            value = f"value_from_thread_{thread_id}_{i}"
            cache.set(key, value)
            time.sleep(0.001)  # 模拟一些处理时间
            
            # 验证数据
            retrieved = cache.get(key)
            if retrieved != value:
                print(f"错误: 线程 {thread_id} 数据不一致!")
    
    print(f"启动 {num_threads} 个线程，每个线程执行 {operations_per_thread} 次操作...")
    
    # 创建并启动线程
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    
    print(f"所有线程完成!")
    print(f"耗时: {elapsed_time:.2f} 秒")
    print(f"缓存中的项目总数: {cache.size()}")
    print(f"预期项目数: {num_threads * operations_per_thread}")
    
    if cache.size() == num_threads * operations_per_thread:
        print("✓ 线程安全验证通过!")
    else:
        print("✗ 线程安全验证失败!")
    
    print()


def api_test_scenario_demo():
    """API 测试场景示例"""
    print("=" * 60)
    print("API 测试场景示例")
    print("=" * 60)
    
    cache = DataCache.get_instance()
    cache.clear()
    
    # 模拟 API 测试流程
    print("1. 创建用户 API 测试")
    cache.set("created_user_id", "user_12345")
    cache.set("auth_token", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    print(f"   保存用户ID: {cache.get('created_user_id')}")
    print(f"   保存认证令牌: {cache.get('auth_token')[:30]}...")
    
    print("\n2. 获取用户详情 API 测试")
    user_id = cache.get("created_user_id")
    token = cache.get("auth_token")
    print(f"   使用缓存的用户ID: {user_id}")
    print(f"   使用缓存的令牌进行认证")
    
    # 模拟获取到的用户详情
    user_details = {
        "id": user_id,
        "name": "测试用户",
        "email": "test@example.com"
    }
    cache.set("user_details", user_details)
    print(f"   保存用户详情: {cache.get('user_details')}")
    
    print("\n3. 更新用户 API 测试")
    user_id = cache.get("created_user_id")
    print(f"   使用缓存的用户ID进行更新: {user_id}")
    
    print("\n4. 删除用户 API 测试")
    user_id = cache.get("created_user_id")
    print(f"   使用缓存的用户ID进行删除: {user_id}")
    
    print("\n5. 测试完成，清理缓存")
    print(f"   清理前缓存大小: {cache.size()}")
    cache.clear()
    print(f"   清理后缓存大小: {cache.size()}")
    
    print()


def main():
    """主函数"""
    print("\n")
    print("*" * 60)
    print("数据缓存模块 (DataCache) 使用示例")
    print("*" * 60)
    print()
    
    # 运行各个示例
    basic_usage_demo()
    singleton_demo()
    update_demo()
    thread_safety_demo()
    api_test_scenario_demo()
    
    print("=" * 60)
    print("演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
