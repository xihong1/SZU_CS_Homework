package com.lsy.task2;

import java.util.Comparator;
import java.util.Map;
import java.util.TreeMap;

public class test1 {
    public static void main(String[] args) {
        TreeMap<Lopmodel, String> map = new TreeMap<>();
        map.put(new Lopmodel("lop1", 100), "a");
        map.put(new Lopmodel("lop2", 20), "b");
        map.put(new Lopmodel("lop3", 300), "c");
        map.put(new Lopmodel("lop4", 400), "d");
        map.put(new Lopmodel("lop5", 10), "e");
        map.put(new Lopmodel("lop6", 60), "f");
        map.put(new Lopmodel("lop7", 700), "g");
        map.put(new Lopmodel("lop8", 80), "h");
        map.put(new Lopmodel("lop9", 90), "i");
        map.put(new Lopmodel("lop10", 15), "j");
        for(Map.Entry<Lopmodel, String> entry: map.entrySet()){
            System.out.println(entry.getKey().getType()+" "+entry.getKey().getValue()+" "+entry.getValue());
        }
        System.out.println("-----------------");
        TreeMap<Lopmodel2, String> map2 = new TreeMap<>(new  Comparator<Lopmodel2>() {
            @Override
            public int compare(Lopmodel2 o1, Lopmodel2 o2) {
                return o1.value-o2.value;
            }
        });
        map2.put(new Lopmodel2("lop1", 100), "a");
        map2.put(new Lopmodel2("lop2", 20), "b");
        map2.put(new Lopmodel2("lop3", 300), "c");
        map2.put(new Lopmodel2("lop4", 400), "d");
        map2.put(new Lopmodel2("lop5", 10), "e");
        map2.put(new Lopmodel2("lop6", 60), "f");
        map2.put(new Lopmodel2("lop7", 700), "g");
        map2.put(new Lopmodel2("lop8", 80), "h");
        map2.put(new Lopmodel2("lop9", 90), "i");
        map2.put(new Lopmodel2("lop10", 15), "j");
        for(Map.Entry<Lopmodel2, String> entry: map2.entrySet()){
            System.out.println(entry.getKey().getType()+" "+entry.getKey().getValue()+" "+entry.getValue());
        }


    }
}
