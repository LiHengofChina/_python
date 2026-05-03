

import asyncio

"""
并发运行
"""

async def another_coroutine():
    print("aaaaaaaa")
    for i in range(10):
        print("aaaaaaa: " + str(i))
        await asyncio.sleep(1)
    print("aaaaaaaa")

async def another_coroutine_2():
    print("bbbbbbbbbbbbbbbbbbbbbbbbbb")
    for i in range(10):
        print("bbbbbbbbbbbbbbbbbbbbbbbbbb" + str(i))
        await asyncio.sleep(2)
    print("bbbbbbbbbbbbbbbbbbbbbbbbbb")


async def test_001(name):
    print("Start")

    x = another_coroutine() # x 是 coroutine类型
    task = asyncio.create_task(x)      # 创建一个并发任务，这里我们不会等待它完成

    task2 = asyncio.create_task(another_coroutine_2())   # 创建一个并发任务，这里我们不会等待它完成

    print("End")# another_coroutine 、another_coroutine_2、test_001 同时执行


    # 等待这个任务完成，因为如果主函数结束，所有未完成的任务也会被取消
    await task
    await task2
    print("Type of task:", type(task))      # _asyncio.Task
    print("Type of task2:", type(task2))    # _asyncio.Task
    print("Parent class of task:", type(task).__bases__) #打印它的父类
    print("Parent class of task2:", type(task2).__bases__) #打印它的父类

    print("Type of x:", type(x))    #

if __name__ == '__main__':
    asyncio.run(test_001('Li Heng. '))
    print("bbbbbbbbbbbbbb") #等待上面执行完成，才会执行这里


