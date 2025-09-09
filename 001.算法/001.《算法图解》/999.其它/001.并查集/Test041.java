package com.huaweiod2024.a;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;

/**
 * 华为OD机试真题-精准核酸检测-2023年OD统一考试（C卷）

5
1,2
1,1,0,1,0
1,1,0,0,0
0,0,1,0,1
1,0,0,1,0
0,0,1,0,1

 * @author 86136
 *
 */
public class Test041 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        //总人数
        int n = Integer.parseInt(sc.nextLine());

        //确诊病例
        int[] confirmed = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt).toArray();


        //每个人是否接触的信息矩阵，
        int[][] matrix = new int[n][n];
        for (int i = 0; i < n; i++) {
            matrix[i] = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt).toArray();
        }
 
        System.out.println(getResult(n, confirmed, matrix));
    }

    public static int getResult(int n, int[] confirmed, int[][] matrix) {

    	//创建并查集
    	UnionFindSet ufs = new UnionFindSet(n);

    	//遍历了所有的人员编号，表示当前正在处理的是编号为 i 的人员。
        for (int i = 0; i < n; i++) {
        	// 从当前人员编号 i 开始，遍历了剩余的人员编号
            for (int j = i; j < n; j++) {//内层循环越来越少，因为矩阵当中，matrix[i][j]和 matrix[j][i]是等价的。
            						 	 //所以只循环一半就可以了。
            	//通过  matrix[i][j] 来判断，当前编号为i的人员，
            	//与编号为j的人员是否有接触
                if (matrix[i][j] == 1) {
                    ufs.union(i, j);//合并到一个子集体
                }
            }
        }

        //统计每个元素，所在 “子集合的元素数量”。
        int[] cnts = new int[n];
        for (int i = 0; i < n; i++) {
            int fa = ufs.find(i);
            cnts[fa]++;
        } 

        HashSet<Integer> confirmed_fa = new HashSet<>();

        int ans = 0;
        for (int i : confirmed) {//循环确证病例，
            int fa = ufs.find(i);//找到确证病例，所在的根节点
            if (confirmed_fa.contains(fa)) {//
            	 continue;//统计过了，就不在计算
            }
            confirmed_fa.add(fa);
            ans += cnts[fa];//把人数进行累加。
        }
        return ans - confirmed.length;//减去确诊的

    }
}

/**
 * 数据结构：并查集
 */
class UnionFindSet {

	//初始化，并查集，初始状态，每个元素根节点就是自己
	//fa脚标是编号，而值是"根节点编号"，默认是自己。
    int[] fa;
    public UnionFindSet(int n) {
        this.fa = new int[n];
        for (int i = 0; i < n; i++) {
        	fa[i] = i;
        }
    }
    //查找x的根节点，中途会进行路径压缩
    public int find(int x) {
        if (x != this.fa[x]) {//如果根节点不是自己则，继续查找
            this.fa[x] = this.find(this.fa[x]);//路径压缩，查找过的元素将会进行路径压缩。
            								   //将“元素x”到“其根节点的路径上”的“所有节点”直接连接到“根节点”。
            return this.fa[x];
        }
        return x;//值相等，那么自己就是根节点。
    }

    public void union(int x, int y) {
        int x_fa = this.find(x);
        int y_fa = this.find(y);
 
        if (x_fa != y_fa) {
            this.fa[y_fa] = x_fa;
            // y 所在集合的根节点指向元素 x 所在集合的根节点。
        }
    }
}
