package com.lsy.task7;
import java.util.Random;
public class test {
    // 共享变量，用于线程间通信
    private volatile int currentNumber = -1;
    private volatile boolean shouldStop = false;
    private volatile int numberCount = 0;
    // 生成随机数的线程
    class RandomNumberGenerator extends Thread {
        Random random = new Random();
        @Override
        public void run() {
            while (!shouldStop && numberCount < 10) {
                synchronized (test.this) {
                    currentNumber = random.nextInt(10001);
                    numberCount++;
                    System.out.println(currentNumber);
                    test.this.notifyAll();
                    // 等待消费者线程处理
                    try {
                        test.this.wait();
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }
            }
            shouldStop = true;
            System.out.println("随机数生成器线程结束");
        }
    }
    // 检查素数的线程
    class PrimeChecker extends Thread {
        @Override
        public void run() {
            while (!shouldStop && numberCount < 10) {
                synchronized (test.this) {
                    // 等待新的随机数生成
                    try {
                        test.this.wait(1000); // 等待1秒或通知
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }

                    if (currentNumber != -1) {
                        boolean isPrime = checkPrime(currentNumber);
                        if (isPrime) {
                            shouldStop = true;
                            System.out.println("发现素数，程序停止");
                            test.this.notifyAll();
                            break;
                        }
                        test.this.notifyAll();
                    }
                }
            }
            System.out.println("素数检查器线程结束");
        }
        // 检查是否为素数的方法
        private boolean checkPrime(int number) {
            if (number <= 1) return false;
            if (number == 2) return true;
            if (number % 2 == 0) return false;

            for (int i = 3; i * i <= number; i += 2) {
                if (number % i == 0) {
                    return false;
                }
            }
            return true;
        }
    }

    public void startProgram() throws InterruptedException {
        RandomNumberGenerator generator = new RandomNumberGenerator();
        PrimeChecker checker = new PrimeChecker();
        generator.start();
        checker.start();
        generator.join();
        checker.join();
        System.out.println("总生成随机数" + numberCount + "个");
    }

    public static void main(String[] args) throws InterruptedException {
        new test().startProgram();
    }
}