package com.liheng.chapter_004.a;

/**
 * 
 * 求数组所有元素的和
 * 
 * 使用循环是可以直接求和，
 * 
 * 但是这里要求使用 "递归" ，数组版（栈版）
 *
 */
public class Test001_001 {
	public static void main(String[] args) {
		int[] input = {2,3,6};
		
		System.out.println( getSum(input) );
		
	}
	private static int getSum(int[] input) {
		if( input.length == 0) {// ====================> 基线条件
			return 0;
		}else {
			
			//剩下的元素产生一个新的数组，不像python可以直接截取。
			int[] n = new int[input.length-1];
			for( int i = 1 ; i < input.length; i++ ) {
				n[i-1] =input[i];
			}
			return input[0] +  getSum(n);// ====================>  递归条件
										 // "第一个元素加" + "后面的所有元素的和"
 
		}

	}
}
