#coding=utf-8
#快速排序


def quicksort(array):
  if len(array) < 2:
    return array  #←------基线条件：为空或只包含一个元素的数组是“有序”的
  else:
    pivot = array[0]  #←------递归条件
    less = [i for i in array[1:] if i <= pivot]  #←------由所有小于等于基准值的元素组成的子数组

    greater = [i for i in array[1:] if i > pivot]  #←------由所有大于基准值的元素组成的子数组

    return quicksort(less) + [pivot] + quicksort(greater)

if __name__ == "__main__":
    print(quicksort([10, 5, 2, 3]))
    
