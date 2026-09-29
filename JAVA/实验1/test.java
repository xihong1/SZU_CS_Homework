package com.lsy_stduy.day01;

import java.util.Scanner;

public class test {
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        int user=sc.nextInt();
        if(user<=50) System.out.println(0.4*user);
        else if (user <= 100) {
            System.out.println(20+0.6*(user-50));
        }
        else{
            System.out.println(20+30+(user-100)*0.8);
        }
    }
}
