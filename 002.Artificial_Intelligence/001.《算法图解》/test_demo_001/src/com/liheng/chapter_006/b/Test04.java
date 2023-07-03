package com.liheng.chapter_006.b;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Java版，广度优先搜索
 */
public class Test04 {


	private static boolean test() {
		//创建图
		Map<String,String[]> graph = new HashMap<>();
		graph.put("you", new String[]{"alice","bob","claire"});

		graph.put("bob", new String[]{"anuj", "peggy"});
		graph.put("alice", new String[]{"peggy"});
		graph.put("claire", new String[]{"thom", "jonny"});
		graph.put("anuj", new String[]{});
		graph.put("peggy", new String[]{});
		graph.put("thom", new String[]{});
		graph.put("jonny", new String[]{});
						
		//广度优先搜索
		Deque<String> search_queue = new ArrayDeque<String>();
		
		for(String str: graph.get("you")) {
			search_queue.add(str);
		}
		List<String> searched = new ArrayList<String>();
		while(!search_queue.isEmpty()) {
			String person = search_queue.pop();
			System.out.println("_________" + person);
			if(!searched.contains(person)) {
				if(person_is_seller(person)) {
					System.out.println(person + " is a mango seller! ");
					return true;
				}else {
					for(String str: graph.get(person)) {
						search_queue.add(str);
					}
					searched.add(person);
				}
			}
		}
		return false;
	}	
	private static boolean person_is_seller(String persion) {
		return persion.charAt(persion.length()-1) == 'm';
	}
	public static void main(String[] args) {
		test();
	}

}
