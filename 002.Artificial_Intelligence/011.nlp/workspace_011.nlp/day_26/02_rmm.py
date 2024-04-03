
'''
         逆向最大匹配分词示例
        （需要词典）
        （需要假设：最长词为4个字）
'''
class RMM(object):
    def __init__(self):
        self.window_size = 3

    def cut(self, text):
        result = [] # 分词结果
        start = len(text) # 起始位置
        text_len = len(text) # 文本长度

        dic = ["吉林", "吉林市", "市长", "长春", "春药", "药店"]

        while start > 0:
            for size in range(self.window_size, 0, -1):
                piece = text[start-size:start] # 切片
                if piece in dic: # 在字典中
                    result.append(piece) # 添加到列表
                    start -= len(piece)
                    break
                else: # 没在字典中
                    if len(piece) == 1:
                        result.append(piece) # 单个字成词
                        start -= len(piece)
                        break
        result.reverse()
        return result

if __name__ == "__main__":
    text = "吉林市长春药店"
    tk = RMM() # 实例化对象
    result = tk.cut(text)
    print(result)