package com.lsy.task1;
import java.util.Scanner;

public class task1 {
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        String num=sc.nextLine();
        StringBuilder sbNum=new StringBuilder(num);
        sbNum=sbNum.reverse();
        String finalNum=sbNum.toString();
        System.out.println(finalNum);
    }
}
