# 正向最大匹配分词示例
class MM(object):
    def __init__(self):
        self.window_size = 3

    def cut(self, text):
        result = [] # 分词结果
        start = 0 # 起始位置
        text_len = len(text) # 文本长度

        dic = ["吉林", "吉林市", "市长", "长春", "春药", "药店"]

        while text_len > start:
            for size in range(self.window_size + start, start, -1): # 取最大长度，逐步比较减小
                piece = text[start:size] # 切片
                if piece in dic: # 在字典中
                    result.append(piece) # 添加到列表
                    start += len(piece)
                    break
                else: # 没在字典中，什么都不做
                    if len(piece) == 1:
                        result.append(piece) # 单个字成词
                        start += len(piece)

        return result

if __name__ == "__main__":
    text = "吉林市长春药店"
    tk = MM() # 实例化对象
    result = tk.cut(text)
    print(result)