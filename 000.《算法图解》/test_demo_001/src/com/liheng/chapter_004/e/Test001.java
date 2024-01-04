package com.liheng.chapter_004.e;

import java.util.Arrays;

/**
 * jdk8版的快速排序
 * @author Administrator
 *
 */
public class Test001 {
	public static void main(String[] args) {

		int[] array = {10, 5, 2, 3};
		quicksort(array);
	}

	private static int[] quicksort(int[] array) {
		if ( array.length < 2 ) {
			 return array;
		}
		
		int pivot = array[0];
		
		int[] less = Arrays.stream(array).filter( i ->  i <= 5).toArray();
		
		int[] greater = Arrays.stream(array).filter( i ->  i <= 5).toArray();
		
		
//		没有找到类似的语法//TODO		
//		quicksort(less) +pivot + quicksort(greater)
		return null;
		
	}
}
