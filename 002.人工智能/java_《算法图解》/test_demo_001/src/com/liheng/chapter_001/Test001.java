package com.liheng.chapter_001;


/**
 * ���ַ����� JAVA ʵ�֣�ѭ���棩
 * 		//��Ϊ����ʹ�õݹ����ѭ��
 * 
 * 2022��8��17��10:35:54
 * 
 * @author Administrator
 *
 */
public class Test001 {
	public static void main(String[] args) {
		
		int[] arr = new int[] {1,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10};
		System.out.println(binary_search(arr,6)); 
	}
	
	private static int binary_search(int[] input, int x) {
		
		
		// low��high���ڸ���Ҫ�����в��ҵ��б���
		int low = 0;//��λ����һ��Ԫ��
		int hight = input.length - 1;//��λ�����һ��Ԫ��
		

		int mid = 0;
		while( low <= hight ) {
			
			mid = ( low + hight ) / 2 ;// 9/2 = 4 ������ȡ�� 
			
			// ż���� "�м�ƫ��" ������ "�������м�"
			int guess = input[mid];
			
			//����м��Ԫ��������Ҫ�ҵ���Ԫ�أ�ֱ�ӷ��� �м������ű�
			if(guess == x) {
				return mid ;
			}
			
			//����������ҵķ�Χ
			if( x < input[mid]) { //Ҫ�ҵ���С���м���
				//�������䣬 //��λ�����ƶ�һ��
				hight = mid - 1;
			}else {//Ҫ�ҵ����������м���
				//��λ���䣬 //��λ�����ƶ�һ��
				low = mid + 1;
			}
		}
		
		//���û���ҵ�������-1��
		return -1;
	}
}
