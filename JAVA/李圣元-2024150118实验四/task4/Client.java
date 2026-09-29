package com.lsy.task4;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class Client {
    private static final String SERVER_IP = "127.0.0.1";
    private static final int SERVER_PORT = 8888;
    public static void main(String[] args) {
        Socket clientSocket = null;
        Scanner scanner = new Scanner(System.in);
        try {
            clientSocket = new Socket(SERVER_IP, SERVER_PORT);
            System.out.println("客户端启动" );
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream(), StandardCharsets.UTF_8));
            Writer out = new OutputStreamWriter(
                    clientSocket.getOutputStream(), StandardCharsets.UTF_8);
            Socket finalClientSocket = clientSocket;
            new Thread(() -> {
                String serverMsg;
                try {
                    while ((serverMsg = in.readLine()) != null) {
                        System.out.println(serverMsg);
                        if ("bye".equalsIgnoreCase(serverMsg)) {
                            in.close();
                            out.close();
                            finalClientSocket.close();
                            break;
                        }
                    }
                } catch (IOException e) {
                    if (!finalClientSocket.isClosed()) {
                        System.err.println("接收服务器消息异常：" + e.getMessage());
                    }
                }
            }).start();
            while (true) {
                System.out.print("客户端：");
                String clientMsg = scanner.nextLine().trim();
                if ("bye".equalsIgnoreCase(clientMsg)) {
                    out.write(clientMsg + "\n");
                    out.flush();
                    break;
                }
                if (clientSocket.isClosed()) {
                    System.out.println("错误：已与服务器断开连接，无法发送消息");
                    break;
                }
                out.write(clientMsg + "\n");
                out.flush();
            }
        } catch (IOException e) {
            System.err.println("客户端启动/连接失败：" + e.getMessage());
        } finally {
            scanner.close();
            try {
                if (clientSocket != null && !clientSocket.isClosed()) {
                    clientSocket.close();
                }
            } catch (IOException e) {
                System.err.println("关闭客户端资源异常：" + e.getMessage());
            }
            System.out.println("客户端已关闭");
        }
    }
}