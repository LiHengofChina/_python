package com.liheng.chapter_004.b;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * ��дһ���ݹ麯���������б������Ԫ������ java��
 */
public class Test002_001 {
	public static void main(String[] args) {
		Deque<Integer>  statck = new ArrayDeque<Integer>();

		statck.push(2);
		statck.push(3);
		statck.push(6);		

		System.out.println( getCount(statck) );

	}
	private static int getCount(Deque<Integer> statck) {
		
		if( statck.isEmpty()) {
			return 0;
		}
		statck.pop();
		return 1+ getCount(statck);

	}
}
