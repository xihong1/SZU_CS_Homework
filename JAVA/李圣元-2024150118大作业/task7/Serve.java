package com.lsy.task7;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

public class Serve {
    // 服务器监听端口和数据缓存大小
    private static final int SERVER_PORT = 8888;
    private static final int BUFFER_SIZE = 1024;

    public static void main(String[] args) {
        DatagramSocket serverSocket = null;
        Scanner scanner = new Scanner(System.in);
        try {
            // 1. 创建服务器套接字并绑定端口
            serverSocket = new DatagramSocket(SERVER_PORT);
            System.out.println("UDP服务器已启动，监听端口：" + SERVER_PORT);
            // 存储客户端的地址和端口（用于回复）
            AtomicReference<InetAddress> clientAddress = new AtomicReference<>();
            AtomicInteger clientPort = new AtomicInteger(-1);
            DatagramSocket finalServerSocket = serverSocket;
            new Thread(() -> {
                byte[] receiveBuffer = new byte[BUFFER_SIZE];
                while (!Thread.currentThread().isInterrupted()) {
                    // 创建接收数据包
                    DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                    try {
                        finalServerSocket.receive(receivePacket);
                        clientAddress.set(receivePacket.getAddress());
                        clientPort.set(receivePacket.getPort());
                        String clientMsg = new String(receivePacket.getData(), 0, receivePacket.getLength(), "UTF-8");
                        if ("exit".equalsIgnoreCase(clientMsg)) {
                            continue;
                        }
                        System.out.println("客户端：" + clientMsg);
                    } catch (IOException e) {
                        if (!finalServerSocket.isClosed()) {
                            System.err.println("接收消息异常：" + e.getMessage());
                        }
                        break;
                    }
                }
            }).start();
            while (true) {
                System.out.print("服务器：");
                String serverMsg = scanner.nextLine().trim();
                if ("exit".equalsIgnoreCase(serverMsg)) {
                    System.out.println("服务器正在关闭...");
                    break;
                }
                if (clientAddress.get() == null || clientPort.get() == -1) {
                    System.out.println("错误：暂未连接到客户端，无法发送消息");
                    continue;
                }
                // 将消息转换为字节数组
                byte[] sendBuffer = serverMsg.getBytes(StandardCharsets.UTF_8);
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, clientAddress.get(), clientPort.get());
                serverSocket.send(sendPacket);
            }

        } catch (IOException e) {
            System.err.println("服务器启动失败：" + e.getMessage());
        } finally {
            // 关闭资源
            scanner.close();
            if (serverSocket != null && !serverSocket.isClosed()) {
                serverSocket.close();
                System.out.println("服务器已关闭");
            }
        }
    }
}