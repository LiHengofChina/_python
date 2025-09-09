from functools import lru_cache

# 使用 lru_cache 装饰器自动实现记忆化
@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    """用记忆化递归计算斐波那契数"""
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def main():
    n = 300
    print(f"fib({n}) = {fib_memo(n)}")


if __name__ == "__main__":
    main()
