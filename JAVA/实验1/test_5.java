package com.lsy_stduy.day01;

public class test_5 {
    public static void main(String[] args) {
        for (int i = 2; i <= 10000; i++) {
            if(isTrue(i)) System.out.print(i+" ");
        }
    }

    public static boolean isTrue(int num) {
        int end=(int)Math.sqrt(num);
        int ans=1;
        for (int i = 2; i <= end; i++) {
            if(num%i==0) {
                ans += i;
                if (i * i != num ) ans = ans + num / i;
            }
        }
        return ans==num;
    }
}
