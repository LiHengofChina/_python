package com.liheng.chapter_003;

/**
 * 
 * �ݹ飺�������� ��  �ݹ�����
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
		
		if( i <= 1 ) {     // ��------��������
			return;
		}else {
			countdown(i-1);// ��------�ݹ�����
		}
		
	}
}
