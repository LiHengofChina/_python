package com.liheng.chapter_003;

/**
 * 
 * �ݹ飺N�Ľ׳�
 * 
 * @author Administrator
 *
 */
public class Test003 {

	public static void main(String[] args) {
		System.out.println( factorial(16) );
	}

	/**
	 *  n! ��ʾ n�� �׳�
	 * @param n
	 * @return
	 */
	private static int factorial(int n ) {
		if( n == 1 ) {      //  ��------��������
			return 1;
		} 
		return  n * factorial( n-1 ); //��------�ݹ�����
	}
 
}
