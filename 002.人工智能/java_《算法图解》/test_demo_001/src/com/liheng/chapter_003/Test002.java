package com.liheng.chapter_003;

/**
 * ’ª”Îµ˜”√’ª
 * @author Administrator
 *
 */
public class Test002 {
	public static void main(String[] args) {
		greet("liheng");
	}
	
	private static void greet(String name) {
		 
		 System.out.println("hello, " + name + "!");
		 greet2(name);
		 
		 System.out.println("getting ready to say bye...");
		 bye();

	}
	
	private static void greet2(String name) {
		System.out.println( "how are you, " + name + "?");
	}
	
	private static void bye() {
		  System.out.println("ok bye!");
	}
	
}
