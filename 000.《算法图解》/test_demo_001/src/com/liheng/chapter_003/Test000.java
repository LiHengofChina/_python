package com.liheng.chapter_003;

/**
 * �ݹ飺��ѭ���ݹ�
 * @author Administrator
 */
public class Test000 {
	public static void main(String[] args) {
		countdown(10);
	}
	private static void countdown(int i ) {
		System.out.println( i );
		countdown(i-1);// ��------�ݹ�����
	}
}
