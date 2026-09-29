package com.lsy.task4;

public class Machine {
    public void checkBag(Goods goods) throws DangerException {
        if (goods.isDangerous) {
            throw new DangerException(goods.name + "是危险商品");
        }
    }
}
