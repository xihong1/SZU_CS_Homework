package com.lsy.task1;

import java.io.*;

public class test {
    private static final String INPUT_PATH="D:\\code\\java\\Java_task\\src\\com\\lsy\\task1\\input.txt";
    private static final String OUTPUT_PATH="D:\\code\\java\\Java_task\\src\\com\\lsy\\task1\\output.txt";
    public static void main(String[] args) throws IOException {
        BufferedReader reader=new BufferedReader(new FileReader(INPUT_PATH));
        BufferedWriter writer=new BufferedWriter(new FileWriter(OUTPUT_PATH));
        String line;
        while ((line=reader.readLine())!=null){
            line=line.trim();
            String reverseline=new StringBuffer(line).reverse().toString();
            writer.write(reverseline);
            writer.newLine();
        }
        reader.close();
        writer.close();
    }

}
