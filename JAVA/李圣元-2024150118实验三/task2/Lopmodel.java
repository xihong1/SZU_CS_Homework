package com.lsy.task2;

public class Lopmodel implements Comparable<Lopmodel> {
    String type;
     Integer value;
    public Lopmodel(String type, Integer value) {
        this.type = type;
        this.value = value;
    }
    String getType() {
        return type;
    }
    Integer getValue() {
        return value;
    }
    @Override
    public int compareTo(Lopmodel o) {
        return value-o.getValue();
    }
}
