package com.liheng.test;

import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;

public class Demo {

	public static void main(String[] args) {
		//Ҫ�����������������
		//int arr[] = {4, 6, 8, 5, 9};

		// ����Ҫ�� 10 �������������
		int[] array = new int[10];
		for (int i = 0; i < 10; i++) {
			array[i] = (int) (Math.random() * 10); // ����һ��[0, 8000000) ��
		} 
		System.out.println(array.length); 
		
		System.out.println("����ǰ");
		Date data1 = new Date();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		String date1Str = simpleDateFormat.format(data1);
		System.out.println("����ǰ��ʱ����=" + date1Str);
		
		heapSort(array);
		
		Date data2 = new Date();
		String date2Str = simpleDateFormat.format(data2);
		System.out.println("����ǰ��ʱ����=" + date2Str);
		
	}

	//��дһ��������ķ���
	public static void heapSort(int[] array) {
		
		System.out.println("������!!");
		
//		//�ֲ����
//		adjustHeap(arr, 1, arr.length);
//		System.out.println("��һ��" + Arrays.toString(arr)); // 4, 9, 8, 5, 6
//		
//		adjustHeap(arr, 0, arr.length);
//		System.out.println("��2��" + Arrays.toString(arr)); // 9,6,8,5,4
		System.out.println("����ǰ==== " + Arrays.toString(array));
		//����������մ���
		//���������й�����һ���ѣ���������������ѡ��󶥶ѻ�С����
		for(int i = array.length / 2 -1; i >=0; i--) {
			Tool.adjustHeap(array, i, array.length);
		}
		System.out.println("��ɴ󶥶�=" + Arrays.toString(array));

		
		/*
		 * 2).���Ѷ�Ԫ����ĩβԪ�ؽ����������Ԫ��"��"������ĩ��;
����			3).���µ����ṹ��ʹ������Ѷ��壬Ȼ����������Ѷ�Ԫ���뵱ǰĩβԪ�أ�����ִ�е���+�������裬ֱ��������������
		 */
		int temp = 0; 
		for(int j = array.length-1;j >0; j--) {
			//����
			temp = array[j];
			array[j] = array[0];
			array[0] = temp;
			Tool.adjustHeap(array, 0, j); 
		}
		System.out.println("�����==== " + Arrays.toString(array));
		//System.out.println("����=" + Arrays.toString(arr)); 
		
	}
	
	
}
