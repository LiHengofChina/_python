package com.liheng.chapter_004.a;

/**
 * 
 * ����������Ԫ�صĺ�
 * 
 * ʹ��ѭ���ǿ���ֱ����ͣ�
 * 
 * ��������Ҫ��ʹ�� "�ݹ�" ������棨ջ�棩
 *
 */
public class Test001_001 {
	public static void main(String[] args) {
		int[] input = {2,3,6};
		
		System.out.println( getSum(input) );
		
	}
	private static int getSum(int[] input) {
		if( input.length == 0) {// ====================> ��������
			return 0;
		}else {
			
			//ʣ�µ�Ԫ�ز���һ���µ����飬����python����ֱ�ӽ�ȡ��
			int[] n = new int[input.length-1];
			for( int i = 1 ; i < input.length; i++ ) {
				n[i-1] =input[i];
			}
			return input[0] +  getSum(n);// ====================>  �ݹ�����
										 // "��һ��Ԫ�ؼ�" + "���������Ԫ�صĺ�"
 
		}

	}
}
