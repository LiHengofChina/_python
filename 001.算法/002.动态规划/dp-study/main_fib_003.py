def fib_bu(n: int) -> int:
    """自底向上（Bottom-Up）动态规划求斐波那契"""
    if n <= 1:
        return n

    a, b = 0, 1  #定义两个变量 a = 0 b = 1 ， dp[0], dp[1]
                 # 在 Fibonacci 的代码里： a 表示 fib(i-2) b 表示 fib(i-1)
    """
     dp[]，表示一个数组，用来存储子问题的结果。

     状态定义：dp[i] = 第 i 个斐波那契数
     转移方程：dp[i] = dp[i-1] + dp[i-2]
    """


    for _ in range(2, n + 1): #指定循环范围
        c = a + b  # dp[i] = dp[i-1] + dp[i-2]
        a, b = b, c # 这里的意思是往后移动一次， b的值给a， c的值给b，c是新算出来的值
    return b


def main():
    n = 3000
    print(f"fib({n}) = {fib_bu(n)}")


if __name__ == "__main__":
    main()
