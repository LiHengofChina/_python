
"""
这个文件演示了递归实现斐波那契数列。
"""

def fib(n: int) -> int:
    if n<=1:
        return n
    return fib(n-1) + fib(n-2)

def main():
    n = 30
    print(f"fib(n) = {fib(n)}")
if __name__ == '__main__':
    main()

