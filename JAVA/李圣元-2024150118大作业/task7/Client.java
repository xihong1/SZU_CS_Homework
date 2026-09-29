package com.lsy.task7;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class Client {
    // 服务器IP
    private static final String SERVER_IP = "127.0.0.1";
    private static final int SERVER_PORT = 8888;
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {
        DatagramSocket clientSocket = null;
        Scanner scanner = new Scanner(System.in);
        try {
            clientSocket = new DatagramSocket();
            System.out.println("客户端已启动，连接服务器：" + SERVER_IP + ":" + SERVER_PORT);
            DatagramSocket finalClientSocket = clientSocket;
            new Thread(() -> {
                byte[] receiveBuffer = new byte[BUFFER_SIZE];
                while (!Thread.currentThread().isInterrupted()) {
                    DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                    try {
                        finalClientSocket.receive(receivePacket);
                        String serverMsg = new String(receivePacket.getData(), 0, receivePacket.getLength(), StandardCharsets.UTF_8);
                        System.out.println("服务器：" + serverMsg);
                    } catch (IOException e) {
                        if (!finalClientSocket.isClosed()) {
                            System.err.println("接收服务器消息异常：" + e.getMessage());
                        }
                        break;
                    }
                }
            }).start();
            while (true) {
                System.out.print("客户端：");
                String clientMsg = scanner.nextLine().trim();
                if ("exit".equalsIgnoreCase(clientMsg)) {
                    // 发送退出消息给服务器
                    byte[] exitBuffer = clientMsg.getBytes(StandardCharsets.UTF_8);
                    DatagramPacket exitPacket = new DatagramPacket(exitBuffer, exitBuffer.length,
                            InetAddress.getByName(SERVER_IP), SERVER_PORT);
                    clientSocket.send(exitPacket);
                    System.out.println("客户端正在退出...");
                    break;
                }
                // 发送普通消息
                byte[] sendBuffer = clientMsg.getBytes(StandardCharsets.UTF_8);
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length,
                        InetAddress.getByName(SERVER_IP), SERVER_PORT);
                clientSocket.send(sendPacket);
            }

        } catch (IOException e) {
            System.err.println("客户端启动失败：" + e.getMessage());
        } finally {
            // 关闭资源
            scanner.close();
            if (clientSocket != null && !clientSocket.isClosed()) {
                clientSocket.close();
                System.out.println("客户端已关闭");
            }
        }
    }
}