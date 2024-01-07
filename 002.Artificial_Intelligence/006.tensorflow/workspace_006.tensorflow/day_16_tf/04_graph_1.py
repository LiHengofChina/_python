

import tensorflow as tf
'''
  
  ————————————————————  op、图graph、session
  op 存放所有操作
  graph 是 op 的容器 
  session是用来执行graph的
  ————————————————————   错误示例

'''

#【2】示例2 ：Error
x = tf.constant(100.0)
y = tf.constant(200.0)
res  = tf.add(x,y)
#新创建一个图
new_graph= tf.Graph()
with tf.Session(graph = new_graph) as sess:
    result = sess.run(res)#此时 res 在默认图上面，不在新创建的图上面，因此会报错
    print(result)
