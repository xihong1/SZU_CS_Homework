package com.lsy.task4;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class Test {
    public static void main(String[] args) {
        Map<String,Double> map = new HashMap<>();
        map.put("苹果",55.4);
        map.put("香蕉",34.6);
        map.put("橙子",47.5);
        map.put("葡萄",62.5);
        System.out.println(map.values().stream().mapToDouble(Double::doubleValue).sum());
    }
}
