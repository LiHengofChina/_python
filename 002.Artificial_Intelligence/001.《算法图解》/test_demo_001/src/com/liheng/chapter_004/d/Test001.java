package com.liheng.chapter_004.d;


/**
 * ���ַ����� JAVA ʵ�֣��ֶ���֮�����ݹ�棩
 * 
 * 2022��8��17��10:35:54
 * 
 * @author Administrator
 *
 */
public class Test001 {
	public static void main(String[] args) {

		int[] arr = new int[] {1,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10};

		
		int low = 0;//��λ����һ��Ԫ��
		int hight = arr.length - 1;//��λ�����һ��Ԫ��
		
		System.out.println(binary_search(arr,6,low, hight));

	}
	
	private static int binary_search(int[] input, int x,int low,int hight) {

		if(low > hight) {
			return -1;
		}
		int mid = ( low + hight ) / 2 ; 
		
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
		return binary_search(input,x,low, hight);			
	}
}
