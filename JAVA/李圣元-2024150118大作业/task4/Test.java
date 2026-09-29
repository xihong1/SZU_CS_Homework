package com.lsy.task4;

public class Test {
    public static void main(String[] args) {
        Machine machine = new Machine();
        Goods goods1 = new Goods("水", false);
        Goods goods2 = new Goods("酒", true);
        try {
            machine.checkBag(goods1);
            machine.checkBag(goods2);
        } catch (DangerException e) {
            e.toshow();
        }
    }
}
