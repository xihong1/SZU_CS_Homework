package com.lsy.task3;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class Student implements Comparable<Student>,Serializable{
    public String name;
    public String ID;
    public double score;
    public Student(String name,String ID,double score){
        this.name=name;
        this.ID=ID;
        this.score=score;
    }
    @Override
    public int compareTo(Student o) {
        return Double.compare(o.score, this.score);
    }
}

public class test {
    private static final String inputPath="D:/code/java/Java_task/src/com/lsy/task3/students.dat";
    private static final String outputPath="D:/code/java/Java_task/src/com/lsy/task3/sorted_students.dat";
    public static void main(String[] args) {
        Student stu1=new Student("张三","2023001",90.0);
        Student stu2=new Student("李四","2023002",85.0);
        Student stu3=new Student("王五","2023003",95.0);
        Student stu4=new Student("赵六","2023004",88.0);
        Student stu5=new Student("钱七","2023005",92.0);
        try {
            FileOutputStream fos = new FileOutputStream(inputPath);
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(stu1);
            oos.writeObject(stu2);
            oos.writeObject(stu3);
            oos.writeObject(stu4);
            oos.writeObject(stu5);
            oos.close();
            fos.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        List<Student> students = new ArrayList<>();
        try {
            FileInputStream fis = new FileInputStream(inputPath);
            ObjectInputStream ois = new ObjectInputStream(fis);
            for(int i=0;i<5;i++){
                Student stu = (Student)ois.readObject();
                students.add(stu);
                System.out.println(stu.name+","+stu.ID+","+stu.score);
            }
            ois.close();
            fis.close();
        } catch (IOException | ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        Collections.sort(students);
        for(Student student:students){
            System.out.println(student.name+","+student.ID+","+student.score);
        }
        try {
            FileOutputStream fos = new FileOutputStream(outputPath);
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            for(Student student:students){
                oos.writeObject(student);
            }
            oos.close();
            fos.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
