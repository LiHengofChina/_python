package com.liheng.test;

public class Tool {
	// ��һ������, ������һ���󶥶�(������)
	/**
	 * ���ܣ� ��� �� �� i ��Ӧ�ķ�Ҷ�ӽ����������ɴ󶥶� ���� int arr[] = {4, 6, 8, 5, 9}; => i = 1 =>
	 * adjustHeap => �õ� {4, 9, 8, 5, 6} ��������ٴε��� adjustHeap ������� i = 0 => �õ� {4, 9,
	 * 8, 5, 6} => {9,6,8,5, 4}
	 * 
	 * @param arr    ������������
	 * @param i      ��ʾ��Ҷ�ӽ��������������
	 * @param lenght ��ʾ�Զ��ٸ�Ԫ�ؼ��������� length �����𽥵ļ���
	 */
	public static void adjustHeap(int arr[], int i, int lenght) {

		int temp = arr[i];// ��ȡ����ǰԪ�ص�ֵ����������ʱ����
		// ��ʼ����
		// ˵��
		// 1. k = i * 2 + 1 k �� i�������ӽ��
		for (int k = i * 2 + 1; k < lenght; k = k * 2 + 1) {
			if (k + 1 < lenght && arr[k] < arr[k + 1]) { // ˵�����ӽ���ֵС�����ӽ���ֵ
				k++; // k ָ�����ӽ��
			}
			if (arr[k] > temp) { // ����ӽ����ڸ����
				arr[i] = arr[k]; // �ѽϴ��ֵ������ǰ���
				i = k; // !!! i ָ�� k,����ѭ���Ƚ�
			} else {
				break;// !
			}
		}
		// ��for ѭ�������������Ѿ�����i Ϊ�������������ֵ�������� �(�ֲ�)
		arr[i] = temp;// ��tempֵ�ŵ��������λ��
	}
}
