package com.liheng.chapter_002;

/**
 * ѡ������ ��python�汾˼·��
 * 
 * O(n^2) һ���ٶȽ����������㷨��
 * 
 * @author Administrator
 *
 */
public class Test001_002 {
	public static void main(String[] args) {
		
		int[] input = { 5, 3, 6, 2, 10 };

		//��1��. ���ҵ���Сֵ֮�󣬷���һ���µ����飬
		//��2��. Ȼ��ʣ�µ����ݼ����ҵ���С��ֵ��
		// TODO: ����д��ʹ��Python����ʵ�֣���Ϊpython�� arr.pop(smallest) ����
		//       ����ȡ�������е� ָ��ֵ������

		System.out.println(input[findSmallest(input)]); 
	}
	/**
	 * ���������ҵ���С��Ԫ��
	 * @param input
	 * @return
	 */
	private static int  findSmallest(int[] input) {
		
		int small = input[0];//��С��ֵ//�ѵ�һ��ֵĬ�ϵ�����Сֵ
		
		int small_index = 0;//��СԪ�ص�����
		
		for(int i = 1 ; i < input.length ; i++ ) {
			if( input[i] < small ) {//�����֮ǰ��ֵ��С��˵�� i ��Ӧ��ֵ��С��
				small = input[i]; //������Сֵ��������һ�αȽ�
				small_index = i ; //����ָ��
			}
			
		}
		
		return small_index;//������Сֵ�Ľű�
	}
}

