package com.lsy.task2;

public class Circle {
    public static final  double PI= 3.14;
    private  double radius;
    Circle(double radius) {
        this.radius = radius;
    }
    public double getRadius() {
        return radius;
    }
    public void setRadius(double radius) {
        this.radius = radius;
    }
    public double getArea() {
        return PI * radius * radius;
    }
    public double getCircumference() {
        return 2 * PI * radius;
    }
}
