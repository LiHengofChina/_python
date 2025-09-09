def lcs_length_and_table(a: str, b: str):
    """返回 LCS 长度和 DP 表（用于回溯）"""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = dp[i - 1][j] if dp[i - 1][j] >= dp[i][j - 1] else dp[i][j - 1]
    return dp[n][m], dp


def lcs_reconstruct(a: str, b: str, dp) -> str:
    """利用 DP 表从右下角回溯出一条 LCS"""
    i, j = len(a), len(b)
    ans = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            ans.append(a[i - 1])
            i -= 1
            j -= 1
        else:
            # 走向较大的那个子问题
            if dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
    return "".join(reversed(ans))


def main():
    a = "ABCBDAB"
    b = "BDCABA"
    length, dp = lcs_length_and_table(a, b)
    subseq = lcs_reconstruct(a, b, dp)
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"LCS length = {length}")
    print(f"One LCS    = {subseq!r}")


if __name__ == "__main__":
    main()
