package com.liheng.chapter_002;

/**
 * 选择排序 （python版本思路）
 * 
 * O(n^2) 一种速度较慢的排序算法。
 * 
 * @author Administrator
 *
 */
public class Test001_002 {
	public static void main(String[] args) {
		
		int[] input = { 5, 3, 6, 2, 10 };

		//（1）. 当找到最小值之后，放入一个新的数组，
		//（2）. 然后剩下的内容继续找到最小的值。
		// TODO: 这种写法使用Python更好实现，因为python有 arr.pop(smallest) 方法
		//       就是取出数组中的 指定值，弹出

		System.out.println(input[findSmallest(input)]); 
	}
	/**
	 * 从数组中找到最小的元素
	 * @param input
	 * @return
	 */
	private static int  findSmallest(int[] input) {
		
		int small = input[0];//最小的值//把第一个值默认当成最小值
		
		int small_index = 0;//最小元素的索引
		
		for(int i = 1 ; i < input.length ; i++ ) {
			if( input[i] < small ) {//如果比之前的值还小，说明 i 对应的值更小。
				small = input[i]; //更换最小值，用于下一次比较
				small_index = i ; //更换指针
			}
			
		}
		
		return small_index;//返回最小值的脚标
	}
}

