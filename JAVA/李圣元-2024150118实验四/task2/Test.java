package com.lsy.task2;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class Student implements Comparable<Student>{
    public String name;
    public int age;
    public int score;
    public Student(String name,int age,int score){
        this.name=name;
        this.age=age;
        this.score=score;
    }
    @Override
    public int compareTo(Student o) {
        return o.score-this.score;
    }
}
public class Test {
    private static final String inputPath="D:/code/java/Java_task/src/com/lsy/task2/students.txt";
    private static final String outputPath="D:/code/java/Java_task/src/com/lsy/task2/students_sorted.txt";
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(inputPath));
        BufferedWriter writer = new BufferedWriter(new FileWriter(outputPath));
        String line;
        reader.readLine();
        List<Student> students = new ArrayList<>();
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split(",");
            String name = parts[0];
            int age = Integer.parseInt(parts[1]);
            int score = Integer.parseInt(parts[2]);
            students.add(new Student(name, age, score));
        }
        Collections.sort(students);
        for(Student student:students){
            System.out.println(student.name+","+student.age+","+student.score);
            writer.write(student.name+","+student.age+","+student.score);
            writer.newLine();
        }
        writer.close();
        reader.close();
    }
}
