package com.liheng.chapter_003;

/**
 * 
 * 递归：N的阶乘
 * 
 * @author Administrator
 *
 */
public class Test003 {

	public static void main(String[] args) {
		System.out.println( factorial(16) );
	}

	/**
	 *  n! 表示 n的 阶乘
	 * @param n
	 * @return
	 */
	private static int factorial(int n ) {
		if( n == 1 ) {      //  ←------基线条件
			return 1;
		} 
		return  n * factorial( n-1 ); //←------递归条件
	}
 
}
