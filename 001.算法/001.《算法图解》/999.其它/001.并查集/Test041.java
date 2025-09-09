package com.huaweiod2024.a;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;

/**
 * ��ΪOD��������-��׼������-2023��ODͳһ���ԣ�C��

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

        //������
        int n = Integer.parseInt(sc.nextLine());

        //ȷ�ﲡ��
        int[] confirmed = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt).toArray();


        //ÿ�����Ƿ�Ӵ�����Ϣ����
        int[][] matrix = new int[n][n];
        for (int i = 0; i < n; i++) {
            matrix[i] = Arrays.stream(sc.nextLine().split(",")).mapToInt(Integer::parseInt).toArray();
        }
 
        System.out.println(getResult(n, confirmed, matrix));
    }

    public static int getResult(int n, int[] confirmed, int[][] matrix) {

    	//�������鼯
    	UnionFindSet ufs = new UnionFindSet(n);

    	//���������е���Ա��ţ���ʾ��ǰ���ڴ�����Ǳ��Ϊ i ����Ա��
        for (int i = 0; i < n; i++) {
        	// �ӵ�ǰ��Ա��� i ��ʼ��������ʣ�����Ա���
            for (int j = i; j < n; j++) {//�ڲ�ѭ��Խ��Խ�٣���Ϊ�����У�matrix[i][j]�� matrix[j][i]�ǵȼ۵ġ�
            						 	 //����ֻѭ��һ��Ϳ����ˡ�
            	//ͨ��  matrix[i][j] ���жϣ���ǰ���Ϊi����Ա��
            	//����Ϊj����Ա�Ƿ��нӴ�
                if (matrix[i][j] == 1) {
                    ufs.union(i, j);//�ϲ���һ���Ӽ���
                }
            }
        }

        //ͳ��ÿ��Ԫ�أ����� ���Ӽ��ϵ�Ԫ����������
        int[] cnts = new int[n];
        for (int i = 0; i < n; i++) {
            int fa = ufs.find(i);
            cnts[fa]++;
        } 

        HashSet<Integer> confirmed_fa = new HashSet<>();

        int ans = 0;
        for (int i : confirmed) {//ѭ��ȷ֤������
            int fa = ufs.find(i);//�ҵ�ȷ֤���������ڵĸ��ڵ�
            if (confirmed_fa.contains(fa)) {//
            	 continue;//ͳ�ƹ��ˣ��Ͳ��ڼ���
            }
            confirmed_fa.add(fa);
            ans += cnts[fa];//�����������ۼӡ�
        }
        return ans - confirmed.length;//��ȥȷ���

    }
}

/**
 * ���ݽṹ�����鼯
 */
class UnionFindSet {

	//��ʼ�������鼯����ʼ״̬��ÿ��Ԫ�ظ��ڵ�����Լ�
	//fa�ű��Ǳ�ţ���ֵ��"���ڵ���"��Ĭ�����Լ���
    int[] fa;
    public UnionFindSet(int n) {
        this.fa = new int[n];
        for (int i = 0; i < n; i++) {
        	fa[i] = i;
        }
    }
    //����x�ĸ��ڵ㣬��;�����·��ѹ��
    public int find(int x) {
        if (x != this.fa[x]) {//������ڵ㲻���Լ��򣬼�������
            this.fa[x] = this.find(this.fa[x]);//·��ѹ�������ҹ���Ԫ�ؽ������·��ѹ����
            								   //����Ԫ��x����������ڵ��·���ϡ��ġ����нڵ㡱ֱ�����ӵ������ڵ㡱��
            return this.fa[x];
        }
        return x;//ֵ��ȣ���ô�Լ����Ǹ��ڵ㡣
    }

    public void union(int x, int y) {
        int x_fa = this.find(x);
        int y_fa = this.find(y);
 
        if (x_fa != y_fa) {
            this.fa[y_fa] = x_fa;
            // y ���ڼ��ϵĸ��ڵ�ָ��Ԫ�� x ���ڼ��ϵĸ��ڵ㡣
        }
    }
}
