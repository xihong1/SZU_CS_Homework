package com.lsy.task3;

import java.util.HashSet;
import java.util.Set;

public class test {
    public static void main(String[] args) {
        Set<String> setA = new HashSet<>();
        Set<String> setB = new HashSet<>();
        setA.add("张三");
        setA.add("李四");
        setB.add("王五");
        setB.add("李四");
        Set<String> setAB = new HashSet<>(setA);
        setAB.retainAll(setB);
        System.out.println(setA);
        System.out.println(setB);
        System.out.println(setAB);
    }
}
