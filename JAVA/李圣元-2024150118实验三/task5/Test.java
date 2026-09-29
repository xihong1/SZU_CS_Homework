package com.lsy.task5;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Scanner;

public class Test {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String str = sc.nextLine();
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy年MM月dd日");
        LocalDate date1 = LocalDate.parse(str, dtf);
        String str1 = sc.nextLine();
        LocalDate date2 = LocalDate.parse(str1, dtf);
        long days= ChronoUnit.DAYS.between(date1,date2);
        //long days=date1.toEpochDay()-date2.toEpochDay();
        System.out.println(days);
    }
}
