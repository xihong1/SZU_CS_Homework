package com.lsy.task1;

import java.util.Scanner;
import java.util.StringTokenizer;

public class task1 {
    public static void main(String[] args) {
        //输入字符
        String input;
        Scanner sc = new Scanner(System.in);
        input = sc.nextLine();
        System.out.println(input);
        //字符分割
        StringTokenizer st = new StringTokenizer(input);
        StringBuilder s = new StringBuilder();
        //将每个单词首字母转换为大写
        while (st.hasMoreTokens()) {
            StringBuilder temp = new StringBuilder(st.nextToken());
            temp.setCharAt(0, Character.toUpperCase(temp.charAt(0)));
            s.append(temp.toString());
            if(st.hasMoreTokens()){
                s.append(" ");
            }
        }
        String result = s.toString();
        System.out.println(result);
        //反转字符串
        StringBuffer sbf = new StringBuffer(result);
        sbf.reverse();
        System.out.println(sbf.toString());
    }
}
