
#encoding=utf-8

def findSmallest(arr):
  smallest = arr[0]
  smallest_index = 0
  for i in range(1, len(arr)):
    if arr[i] < smallest:
      smallest = arr[i]
      smallest_index = i
  return smallest_index


def selectionSort(arr):
  newArr = []
  for i in range(len(arr)):
      smallest = findSmallest(arr)
      newArr.append(arr.pop(smallest))  #把最小值放入新数组
  return newArr



if __name__ == "__main__":
    print(selectionSort([5, 3, 6, 2, 10]))
