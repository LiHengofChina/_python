package com.liheng.chapter_003;

/**
 * 
 * 递归：基线条件 和  递归条件
 * 
 * @author Administrator
 *
 */
public class Test001 {
	public static void main(String[] args) {
		countdown(10);
	}
	private static void countdown(int i ) {
		System.out.println( i );
		
		if( i <= 1 ) {     // ←------基线条件
			return;
		}else {
			countdown(i-1);// ←------递归条件
		}
		
	}
}
