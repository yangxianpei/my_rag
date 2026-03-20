import time
import asyncio


# 同步版本
def sync_demo():
    def task(name, delay):
        print(f"{name} 开始")
        time.sleep(delay)  # 阻塞调用
        print(f"{name} 完成")

    start = time.time()
    task("任务1", 2)
    task("任务2", 1)
    print(f"总耗时: {time.time() - start:.2f}秒")


# 异步版本
async def async_demo():
    async def task(name, delay):
        print(f"{name} 开始")
        await asyncio.sleep(delay)  # 非阻塞等待
        print(f"{name} 完成")

    start = time.time()
    await asyncio.gather(task("任务1", 2), task("任务2", 1))
    print(f"总耗时: {time.time() - start:.2f}秒")


# 运行对比
print("=== 同步版本 ===")
sync_demo()  # 耗时约3秒

print("\n=== 异步版本 ===")
asyncio.run(async_demo())  # 耗时约2秒
