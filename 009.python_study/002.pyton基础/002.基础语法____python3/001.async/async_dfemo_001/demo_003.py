

import asyncio

"""
拿到返回值
"""

async def another_coroutine():
    print("aaaaaaaa")
    return 5

async def test_001(name):
    print("Start")
    x = another_coroutine() # x 是 coroutine类型
    task = asyncio.create_task(x)      # 创建一个并发任务，这里我们不会等待它完成

    print("End")# another_coroutine 、another_coroutine_2、test_001 同时执行

    # 等待这个任务完成，并获取返回的值
    result = await task
    print("Result from another_coroutine:", result)

if __name__ == '__main__':
    asyncio.run(test_001('Li Heng. '))
    print("bbbbbbbbbbbbbb") #等待上面执行完成，才会执行这里


