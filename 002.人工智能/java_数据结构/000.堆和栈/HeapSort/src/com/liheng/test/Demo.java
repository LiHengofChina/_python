package com.liheng.test;

import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;

public class Demo {

	public static void main(String[] args) {
		//要求将数组进行升序排序
		//int arr[] = {4, 6, 8, 5, 9};

		// 创建要给 10 个的随机的数组
		int[] array = new int[10];
		for (int i = 0; i < 10; i++) {
			array[i] = (int) (Math.random() * 10); // 生成一个[0, 8000000) 数
		} 
		System.out.println(array.length); 
		
		System.out.println("排序前");
		Date data1 = new Date();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		String date1Str = simpleDateFormat.format(data1);
		System.out.println("排序前的时间是=" + date1Str);
		
		heapSort(array);
		
		Date data2 = new Date();
		String date2Str = simpleDateFormat.format(data2);
		System.out.println("排序前的时间是=" + date2Str);
		
	}

	//编写一个堆排序的方法
	public static void heapSort(int[] array) {
		
		System.out.println("堆排序!!");
		
//		//分步完成
//		adjustHeap(arr, 1, arr.length);
//		System.out.println("第一次" + Arrays.toString(arr)); // 4, 9, 8, 5, 6
//		
//		adjustHeap(arr, 0, arr.length);
//		System.out.println("第2次" + Arrays.toString(arr)); // 9,6,8,5,4
		System.out.println("排序前==== " + Arrays.toString(array));
		//完成我们最终代码
		//将无序序列构建成一个堆，根据升序降序需求选择大顶堆或小顶堆
		for(int i = array.length / 2 -1; i >=0; i--) {
			Tool.adjustHeap(array, i, array.length);
		}
		System.out.println("变成大顶堆=" + Arrays.toString(array));

		
		/*
		 * 2).将堆顶元素与末尾元素交换，将最大元素"沉"到数组末端;
　　			3).重新调整结构，使其满足堆定义，然后继续交换堆顶元素与当前末尾元素，反复执行调整+交换步骤，直到整个序列有序。
		 */
		int temp = 0; 
		for(int j = array.length-1;j >0; j--) {
			//交换
			temp = array[j];
			array[j] = array[0];
			array[0] = temp;
			Tool.adjustHeap(array, 0, j); 
		}
		System.out.println("排序后==== " + Arrays.toString(array));
		//System.out.println("数组=" + Arrays.toString(arr)); 
		
	}
	
	
}
