

import tensorflow as tf
'''
  
  ————————————————————  op、图graph、session
  op 存放所有操作
  graph 是 op 的容器 
  session是用来执行graph的
  ————————————————————  在新图中创建op
'''

#【3】示例3 ：新图使用方法
x = tf.constant(100.0)
y = tf.constant(200.0)
old_op  = tf.add(x,y)
#新创建一个图
new_graph= tf.Graph()
with new_graph.as_default(): #临时设置为默认图，再创建op，这时
	new_op = tf.constant('hello world in new_op')

with tf.Session(graph = new_graph) as sess:
    result = sess.run(new_op)#此时 new_op 在 new_graph 上面
    print(result)

with tf.Session() as sess: #旧op
    result = sess.run(old_op)#此时 old_op 还是在  默认图上面
    print(result)
