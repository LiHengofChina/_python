package com.liheng.chapter_002;

/**
 * 
 * 
 * O(n^2) һ���ٶȽ����������㷨��
 * 
 * ѡ������ ��java�汾˼·��
 * 
 * ǰ��ÿ��Ԫ�� �� "��������Ԫ��" �Ƚϣ��ҵ���С����һ��������λ�� 
 * 
 * ð�������ǣ����ڵ�����Ԫ�رȽϡ�
 * 
 * @author Administrator
 *
 */
public class Test001_003 {
	public static void main(String[] args) {

		int[] input = { 5, 3, 6, 2, 10 };

		//==================
		for(int x : input) {
			System.out.print(x + " ");
		}
		System.out.println();


		for( int i = 0 ; i < input.length ; i++ ) {
//			System.out.println("��" + input[i] + "��"); 
			for(int y = i + 1; y < input.length ; y++ ) {
//				System.out.print(input[y] + " ");
				//������ڲ㡱����������С�����ǽ���λ��
				if(input[y] < input[i]) {
					int tmp = input[y];
					input[y]  = input[i];
					input[i]  = tmp;
				}
			}
//			System.out.println();
		}
		
		System.out.println("__________________");
		for(int x : input) {
			System.out.print(x + " ");
		}
		
		

 
	}
}

