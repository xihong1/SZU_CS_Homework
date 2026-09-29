package com.lsy.task4;

public class DangerException extends Exception {
    public DangerException(String message) {
        super(message);
    }
    public void toshow() {
        System.out.println(getMessage());
    }
}
