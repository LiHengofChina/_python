

import asyncio


async def another_coroutine():
    print("Inside another coroutine")
    await asyncio.sleep(5)
    print("Exiting another coroutine")


async def test_001(name):
    print("Start")
    # 创建一个并发任务，这样我们不会立即等待它完成
    task = asyncio.create_task(another_coroutine())
    print("End")# another_coroutine 会 与 test_001同时执行
                #注意这

    # 等待这个任务完成，因为如果主函数结束，所有未完成的任务也会被取消
    await task


if __name__ == '__main__':
    asyncio.run(test_001('Li Heng. '))
    print("bbbbbbbbbbbbbb") #等待上面执行完成，才会执行这里


