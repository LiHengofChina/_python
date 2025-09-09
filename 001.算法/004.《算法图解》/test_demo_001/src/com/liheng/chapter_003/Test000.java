package com.liheng.chapter_003;

/**
 * µİ¹é£ºËÀÑ­»·µİ¹é
 * @author Administrator
 */
public class Test000 {
	public static void main(String[] args) {
		countdown(10);
	}
	private static void countdown(int i ) {
		System.out.println( i );
		countdown(i-1);// ¡û------µİ¹éÌõ¼ş
	}
}
