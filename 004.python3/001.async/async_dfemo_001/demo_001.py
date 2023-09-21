

import asyncio


async def another_coroutine():
    print("Inside another coroutine")
    await asyncio.sleep(5)
    print("Exiting another coroutine")

async def test_001(name):
    print("Start")
    await another_coroutine()
    print("End") #需要 another_coroutine 执行完成，才执行这一行


if __name__ == '__main__':
    asyncio.run(test_001('Li Heng. '))
    print("aaaaaaaaaaaaaa") #等待上面执行完成，才会执行这里


