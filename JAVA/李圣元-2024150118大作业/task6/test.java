package com.lsy.task6;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

//定义学生类，包含姓名和成绩
class srddent implements Comparable<srddent>{
    public String name;
    public int score;
    public srddent(String name, int score) {
        this.name = name;
        this.score = score;
    }
    @Override
    public int compareTo(srddent o) {
        return this.score - o.score;
    }
    @Override
    public String toString() {
        return "srddent{" + "name=" + name + ", score=" + score + '}';
    }
}
//主类，包含主方法
public class test {
    public static void main(String[] args) throws IOException {
        //读取文件
        String inputpath="D:\\code\\java\\Java_task\\src\\com\\lsy\\task6\\score.txt";
        String outputpath="D:\\code\\java\\Java_task\\src\\com\\lsy\\task6\\result.txt";
        List<srddent> students = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(inputpath));
        String line;
        br.readLine();
        while ((line = br.readLine()) != null) {
            String[] parts = line.split(",");
            String name = parts[0];
            int score = Integer.parseInt(parts[1]);
            students.add(new srddent(name, score));
        }
        br.close();
        //计算成绩统计信息
        double totalscore = 0;
        double maxscore = 0;
        double minscore = Double.MAX_VALUE;
        double average ;
        int count = 0;
        for (srddent student : students) {
            totalscore += student.score;
            maxscore = Math.max(maxscore, student.score);
            minscore = Math.min(minscore, student.score);
            if(student.score >= 60){
                count++;
            }
        }
        average = totalscore /students.size();
        //排序
        students.sort((a, b) -> b.score - a.score);
        List<srddent> students1 = new ArrayList<>();
        for(int i = 0; i < 5; i++){
            students1.add(students.get(i));
        }
        //写入文件
        BufferedWriter bw = new BufferedWriter(new FileWriter(outputpath));
        StringBuilder sb = new StringBuilder();
        sb.append("总分为：").append(totalscore).append("\n");
        sb.append("最高分：").append(maxscore).append("\n");
        sb.append("最低分：").append(minscore).append("\n");
        sb.append("平均分：").append(average).append("\n");
        sb.append("及格人数：").append(count).append("\n");
        for(int i = 0; i < students1.size(); i++){
            sb.append("第").append(i+1).append("名的姓名为：").append(students1.get(i).name).append("，成绩为：").append(students1.get(i).score).append("\n");
        }
        bw.write(sb.toString());
        bw.close();
    }
}