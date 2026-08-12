package com.demo.dag;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 【有向无循环图对象】
 * 简单的有向图（用于表达 DAG）。
 * 顶点：表名；有向边：from -> to，
 * 表示 from 依赖 to（子表依赖父表）。
 */
public class Dag {

    /***
     *   key：某张表
     * value：它直接依赖的表集合（外键指向的那些父表）
     *
     * 依赖集合为空：这张表当前不依赖别的表（常是父表/起点）
     *
     * 【图里每张表都是顶点（不管依赖是否为空）】
     *
     */
    private final Map<String, Set<String>> adjacency = new LinkedHashMap<>();

    /**
     * 添加顶点（表）。重复添加会被忽略。
     * 【往图里加一个顶点（一张表）。】
     */
    public void addVertex(String vertex) {
        adjacency.computeIfAbsent(vertex, key -> new LinkedHashSet<>());
    }

    /**
     * 添加有向边：from -> to。
     * 外键语义示例：订单 -> 用户，表示「订单依赖用户」。
     * 【用来加一条有向边：from → to。】
     * 如 ：addEdge("订单", "用户")
     * 表示：订单依赖用户（子表 → 父表）。
     */
    public void addEdge(String from, String to) {
        addVertex(from);
        addVertex(to);
        adjacency.get(from).add(to);
    }

    /**
     * 所有顶点。
     */
    public Set<String> getVertices() {
        return Collections.unmodifiableSet(adjacency.keySet());
    }

    /**
     * 某个顶点直接指向的后继（它依赖的表）。
     */
    public Set<String> getSuccessors(String vertex) {
        Set<String> successors = adjacency.get(vertex);
        if (successors == null) {
            return Collections.emptySet();
        }
        return Collections.unmodifiableSet(successors);
    }

    /**
     * 打印邻接关系，方便观察。
     */
    public void printGraph() {
        System.out.println("===== DAG 邻接表（from -> to，表示 from 依赖 to）=====");
        for (Map.Entry<String, Set<String>> entry : adjacency.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }
    }

    /**
     * 返回边列表，便于调试。
     */
    public List<String> listEdges() {
        List<String> edges = new ArrayList<>();
        for (Map.Entry<String, Set<String>> entry : adjacency.entrySet()) {
            for (String to : entry.getValue()) {
                edges.add(entry.getKey() + " -> " + to);
            }
        }
        return edges;
    }
}
