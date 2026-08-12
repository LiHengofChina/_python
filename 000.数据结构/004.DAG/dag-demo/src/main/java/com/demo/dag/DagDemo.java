package com.demo.dag;

import java.util.List;

/**
 * DAG + 拓扑排序演示。
 *
 * 场景模拟外键：
 * - 多子依赖一父：订单、地址 都依赖 用户
 * - 一子依赖多父：订单明细 依赖 订单 和 商品
 */
public class DagDemo {

    public static void main(String[] args) {
        Dag dag = new Dag();

        // 边含义：子表 -> 父表（子依赖父）
        dag.addEdge("订单", "用户");
        dag.addEdge("地址", "用户");
        dag.addEdge("订单明细", "订单");
        dag.addEdge("订单明细", "商品");

        dag.printGraph();

        System.out.println();
        System.out.println("===== 拓扑序（被依赖的先，即父表先脱敏/先写入）=====");
        List<String> order = TopologicalSort.sort(dag);
        for (int i = 0; i < order.size(); i++) {
            System.out.println((i + 1) + ". " + order.get(i));
        }

        System.out.println();
        System.out.println("说明：用户、商品 会排在前面；订单明细会排在订单和商品之后。");
    }
}
