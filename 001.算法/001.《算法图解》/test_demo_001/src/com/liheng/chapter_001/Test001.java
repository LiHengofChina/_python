package com.liheng.chapter_001;


/**
 * 二分法查找 JAVA 实现（循环版）
 * 		//因为可以使用递归或者循环
 * 
 * 2022年8月17日10:35:54
 * 
 * @author Administrator
 *
 */
public class Test001 {
	public static void main(String[] args) {
		
		int[] arr = new int[] {1,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10};
		System.out.println(binary_search(arr,6)); 
	}
	
	private static int binary_search(int[] input, int x) {
		
		
		// low和high用于跟踪要在其中查找的列表部分
		int low = 0;//低位：第一个元素
		int hight = input.length - 1;//高位：最后一个元素
		

		int mid = 0;
		while( low <= hight ) {
			
			mid = ( low + hight ) / 2 ;// 9/2 = 4 ，向下取整 
			
			// 偶数是 "中间偏左" ，奇数 "正好是中间"
			int guess = input[mid];
			
			//如果中间的元素正好是要找到的元素，直接返回 中间的这个脚标
			if(guess == x) {
				return mid ;
			}
			
			//否则调整查找的范围
			if( x < input[mid]) { //要找的数小于中间数
				//低数不变， //高位向左移动一个
				hight = mid - 1;
			}else {//要找的数大于于中间数
				//高位不变， //低位向右移动一个
				low = mid + 1;
			}
		}
		
		//最后没有找到，返回-1。
		return -1;
	}
}
