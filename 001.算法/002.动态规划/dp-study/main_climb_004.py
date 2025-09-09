def climb_stairs(n: int) -> int:
    """动态规划解法：爬楼梯问题"""
    if n <= 1:
        return 1

    a, b = 1, 1  # dp[0], dp[1]
    for _ in range(2, n + 1):
        c = a + b  # dp[i] = dp[i-1] + dp[i-2]
        a, b = b, c
    return b


def main():
    # 小测试
    print(climb_stairs(2))  # 2: (1+1), (2)
    print(climb_stairs(3))  # 3: (1+1+1), (1+2), (2+1)
    print(climb_stairs(8))  # 8


if __name__ == "__main__":
    main()
