package com.lsy.task4;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class Serve {
    private static final int SERVER_PORT = 8888;
    public static void main(String[] args) {
        ServerSocket serverSocket = null;
        Socket clientSocket = null;
        Scanner scanner = new Scanner(System.in);
        Thread receiveThread = null;
        try {
            serverSocket = new ServerSocket(SERVER_PORT);
            System.out.println("服务器启动");
            clientSocket = serverSocket.accept();
            System.out.println("客户端已连接：" + clientSocket.getInetAddress() + ":" + clientSocket.getPort());
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream(), StandardCharsets.UTF_8));
            Writer out = new OutputStreamWriter(
                    clientSocket.getOutputStream(), StandardCharsets.UTF_8);
            Socket finalClientSocket = clientSocket;
            ServerSocket finalServerSocket = serverSocket;
            receiveThread = new Thread(() -> {
                String clientMsg;
                try {
                    while ((clientMsg = in.readLine()) != null) {
                        System.out.println("客户端：" + clientMsg);
                        if ("bye".equalsIgnoreCase(clientMsg)) {
                            System.out.println("客户端发送bye，关闭连接");
                            finalClientSocket.close();
                            finalServerSocket.close();
                            break;
                        }
                        String response = "Server received: " + clientMsg;
                        out.write(response + "\n");
                        out.flush();
                    }
                } catch (IOException e) {
                    if (!finalClientSocket.isClosed()) {
                        System.err.println("接收客户端消息异常：" + e.getMessage());
                    }
                }
            });
            receiveThread.start();
            receiveThread.join();
        } catch (IOException e) {
            System.err.println("服务器启动/运行失败：" + e.getMessage());
        } catch (InterruptedException e) {
            System.err.println("服务器线程等待被中断：" + e.getMessage());
        } finally {
            scanner.close();
            try {
                if (clientSocket != null && !clientSocket.isClosed()) {
                    clientSocket.close();
                }
                if (serverSocket != null && !serverSocket.isClosed()) {
                    serverSocket.close();
                }
            } catch (IOException e) {
                System.err.println("关闭服务器资源异常：" + e.getMessage());
            }
            System.out.println("服务器已关闭");
        }
    }
}