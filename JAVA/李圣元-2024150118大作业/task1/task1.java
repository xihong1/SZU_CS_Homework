package com.lsy.task1;


public class task1 {
    public static void main(String[] args) {
        Teacher teacher = new Teacher("张三", 1, "001");
        System.out.println(teacher.getName());
        System.out.println(teacher.getGender());
        System.out.println(teacher.getId());
        teacher.setName("李四");
        teacher.setGender(0);
        teacher.setId("002");
        System.out.println(teacher.getName());
        System.out.println(teacher.getGender());
        System.out.println(teacher.getId());
    }
}

class Teacher {
    private String name;
    private int gender;
    private String id;
    public Teacher(String name, int gender, String id) {
        this.name = name;
        this.gender = gender;
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getGender() {
        return gender;
    }
    public void setGender(int gender) {
        this.gender = gender;
    }
    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
}
