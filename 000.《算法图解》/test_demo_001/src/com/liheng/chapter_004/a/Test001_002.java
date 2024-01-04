package com.liheng.chapter_004.a;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * 
 * 求数组所有元素的和
 * 
 * 使用循环是可以直接求和，
 * 
 * 但是这里要求使用"递归" 栈版(双端队列版)
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
		if(stack.isEmpty()) {// ====================> 基线条件
			return 0;
		}else {
			return stack.pop() + getSum(stack); // ====================> 递归条件
			 									// "栈顶元素" + "后面的所有元素的和"
		}
	}
}
