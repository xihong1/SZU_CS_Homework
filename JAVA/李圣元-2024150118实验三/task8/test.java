package com.lsy.task8;

public class test {
    //模拟银行用户
    static class bank{
        private double balance;
        private final String account;
        public bank(double balance, String account) {
            this.balance = balance;
            this.account = account;
        }

        public synchronized void withdraw(double count){
            if(balance < count){
                System.out.println("余额不足");
                return;
            }
            balance -= count;
            System.out.println("取款成功" + count + ", 当前余额" + balance);
        }

        public synchronized double getBalance() {
            return balance;
        }
        public String getAccount() {
            return account;
        }
    }
    //创建线程类
    static class withdrawThread extends Thread{
        private bank bank;
        private double withdrawCount;
        public withdrawThread(bank bank, double withdrawCount) {
            this.bank = bank;
            this.withdrawCount = withdrawCount;
        }
        @Override
        public void run() {
            bank.withdraw(withdrawCount);
        }
    }

    public static void main(String[] args) {
        bank bank = new bank(1000, "张三");
        withdrawThread thread1 = new withdrawThread(bank, 500);
        withdrawThread thread2 = new withdrawThread(bank, 300);
        thread1.start();
        thread2.start();
    }


}
