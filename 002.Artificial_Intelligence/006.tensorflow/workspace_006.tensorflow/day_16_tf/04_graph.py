

import tensorflow as tf
'''
  
  ————————————————————  op、图graph、session
  op 存放所有操作
  graph 是 op 的容器 
  session是用来执行graph的
  ————————————————————  打印并查看默认图信息
'''

#【1】示例1：ok
x = tf.constant(100.0)
y = tf.constant(200.0)
res  = tf.add(x,y)
#拿到默认图，并明确指定执行这个图
graph = tf.get_default_graph()
print('默认图',graph)
with tf.Session(graph = graph) as sess:
    # result = sess.run(res)
    result = sess.run([x,y,res])
    print(result)
    print(x.graph)
    print(y.graph)
    print(res.graph)
    print(sess.graph)