package com.lsy_stduy.day01;

import java.util.Arrays;

public class test_3 {
    public static void main(String[] args) {
        double[] numArr=new double[100];
        for (int i = 0; i < numArr.length; i++) {
            numArr[i]=Math.random()*900+100;
        }
        Arrays.sort(numArr);
        double ans=0;
        for (int i = 0; i <10; i++) {
            System.out.println(numArr[numArr.length-i-1]);
            ans+=numArr[numArr.length-i-1];
        }
        System.out.println(ans);
    }

}
