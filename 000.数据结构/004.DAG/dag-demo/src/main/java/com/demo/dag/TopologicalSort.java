package com.demo.dag;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;

/**
 * DAG 上的拓扑排序（Kahn 算法：按入度消点）。
 *
 * 约定：边 from -> to 表示 from 依赖 to。
 * 拓扑序结果：被依赖的在前，依赖方在后（父表在前，子表在后）。
 */
public final class TopologicalSort {

    private TopologicalSort() {
    }

    /**
     * 对 DAG 做拓扑排序。
     *
     * @param dag 有向图
     * @return 拓扑序（父先子后）
     * @throws IllegalStateException 存在环时抛出
     */
    public static List<String> sort(Dag dag) {
        // 1. 计算每个点的入度
        //    边 A -> B 表示 A 依赖 B，则对「脱敏顺序」来说，应先处理 B 再处理 A。
        //    为了让「入度为 0 的点先出队」对应「先处理被依赖方」，
        //    这里按「反向依赖」统计入度：B 被 A 依赖时，给 A 计入度。
        Map<String, Integer> inDegree = new HashMap<>();
        for (String vertex : dag.getVertices()) {
            inDegree.put(vertex, 0);
        }
        for (String from : dag.getVertices()) {
            for (String to : dag.getSuccessors(from)) {
                // from 依赖 to => from 需要等 to 完成 => from 的入度 +1
                inDegree.put(from, inDegree.get(from) + 1);
            }
        }

        // 2. 入度为 0 的点：当前没有未完成的依赖，可以先处理（父表）
        Queue<String> queue = new ArrayDeque<>();
        for (Map.Entry<String, Integer> entry : inDegree.entrySet()) {
            if (entry.getValue() == 0) {
                queue.offer(entry.getKey());
            }
        }

        // 3. 不断取出入度为 0 的点，并减少依赖它的点的入度
        List<String> order = new ArrayList<>();
        while (!queue.isEmpty()) {
            String current = queue.poll();
            order.add(current);

            // 谁依赖了 current？即边 from -> current
            for (String from : dag.getVertices()) {
                Set<String> successors = dag.getSuccessors(from);
                if (!successors.contains(current)) {
                    continue;
                }
                int nextDegree = inDegree.get(from) - 1;
                inDegree.put(from, nextDegree);
                if (nextDegree == 0) {
                    queue.offer(from);
                }
            }
        }

        // 4. 若还有点没进结果，说明有环
        if (order.size() != dag.getVertices().size()) {
            throw new IllegalStateException("图中存在环，无法进行拓扑排序");
        }
        return order;
    }
}
