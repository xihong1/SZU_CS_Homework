package com.lsy.task5;

public class Test {
        private static final Object lock = new Object();
        private static int flag = 1;
        static class numberGenerator extends Thread {
            public void run() {
                for (int i = 1; i <=52; i++) {
                        synchronized (lock) {
                            while (flag != 1) {
                                try {
                                    lock.wait();
                                } catch (InterruptedException e) {
                                    throw new RuntimeException(e);
                                }
                            }
                            System.out.print(i);
                            if(i%2==0) {
                                flag = 2;
                                lock.notifyAll();
                            }
                        }
                }
            }
        }
        static class charGenerator extends Thread {
            public void run() {
                for (char i = 'A'; i <= 'Z'; i++) {
                        synchronized (lock) {
                            while (flag != 2) {
                                try {
                                    lock.wait();
                                } catch (InterruptedException e) {
                                    throw new RuntimeException(e);
                                }
                            }
                            System.out.print(i);
                            flag = 1;
                            lock.notifyAll();
                        }
                }
            }
        }

    public static void main(String[] args) throws InterruptedException {
        numberGenerator numberGenerator = new numberGenerator();
        charGenerator charGenerator = new charGenerator();
        numberGenerator.start();
        charGenerator.start();
        numberGenerator.join();
        charGenerator.join();
    }
}
