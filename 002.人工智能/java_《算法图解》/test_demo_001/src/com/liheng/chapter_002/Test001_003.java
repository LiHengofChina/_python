package com.liheng.chapter_002;

/**
 * 
 * 
 * O(n^2) 一种速度较慢的排序算法。
 * 
 * 选择排序 （java版本思路）
 * 
 * 前面每个元素 和 "后面所有元素" 比较，找到最小的那一个，交换位置 
 * 
 * 冒泡排序是：相邻的两个元素比较。
 * 
 * @author Administrator
 *
 */
public class Test001_003 {
	public static void main(String[] args) {

		int[] input = { 5, 3, 6, 2, 10 };

		//==================
		for(int x : input) {
			System.out.print(x + " ");
		}
		System.out.println();


		for( int i = 0 ; i < input.length ; i++ ) {
//			System.out.println("【" + input[i] + "】"); 
			for(int y = i + 1; y < input.length ; y++ ) {
//				System.out.print(input[y] + " ");
				//如果“内层”的数比外层的小，他们交换位置
				if(input[y] < input[i]) {
					int tmp = input[y];
					input[y]  = input[i];
					input[i]  = tmp;
				}
			}
//			System.out.println();
		}
		
		System.out.println("__________________");
		for(int x : input) {
			System.out.print(x + " ");
		}
		
		

 
	}
}

