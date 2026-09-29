package com.lsy.task3;

import cn.edu.szu.csse.*;

public class test {
    public static void main(String[] args) {
       String[] names = {"张三", "李四", "王五"};
       Student[] students = new Student[names.length];
       for (int i = 0; i < names.length; i++) {
           students[i] = new Student(names[i]);
       }
       Grade grade = new Grade(students);
       grade.getStudentNames();
    }
}
