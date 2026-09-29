package com.lsy_stduy.day01;

public class test_6 {
    public static void main(String[] args) {
        double ans=0;
        for (int i = 0; i < 30; i++) {
            double tempSon=i+2.0;
            double tempMother=i*2+2.0;
            ans+=tempSon/tempMother;
        }
        System.out.println(ans);
    }

}
