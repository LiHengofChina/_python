package com.liheng.chapter_004.a;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * 
 * ����������Ԫ�صĺ�
 * 
 * ʹ��ѭ���ǿ���ֱ����ͣ�
 * 
 * ��������Ҫ��ʹ��"�ݹ�" ջ��(˫�˶��а�)
 *
 */
public class Test001_002 {
	public static void main(String[] args) {
//		Stack<Integer>  statck = new Stack<Integer>();
		Deque<Integer>  statck = new ArrayDeque<Integer>();
		statck.push(2);
		statck.push(3);
		statck.push(6);
		System.out.println( getSum(statck) );
	}

	private static int getSum(Deque<Integer> /*Stack<Integer>*/ stack) {
		if(stack.isEmpty()) {// ====================> ��������
			return 0;
		}else {
			return stack.pop() + getSum(stack); // ====================> �ݹ�����
			 									// "ջ��Ԫ��" + "���������Ԫ�صĺ�"
		}
	}
}
