package com.lsy.task6;
import java.util.HashMap;
import java.util.Map;

public class test {
    private int rows;
    private int cols;
    private HashMap<String, Integer> data;

    public test(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
        this.data = new HashMap<>();
    }
    // 设置矩阵元素
    public void set(int row, int col, int value) {
        String key = row + "," + col;
        if (value != 0) {
            data.put(key, value);
        } else {
            data.remove(key);
        }
    }
    // 获取矩阵元素
    public int get(int row, int col) {
        String key = row + "," + col;
        return data.getOrDefault(key, 0);
    }
    // 矩阵乘法
    public static test multiply(test A, test B) {
        test result = new test(A.rows, B.cols);
        // 遍历A的所有非零元素
        for (Map.Entry<String, Integer> entry : A.data.entrySet()) {
            String[] indices = entry.getKey().split(",");
            int i = Integer.parseInt(indices[0]);
            int k = Integer.parseInt(indices[1]);
            int a = entry.getValue();
            // 对于A的每个非零元素a，与B的第k行相乘并累加到结果的第i行
            for (int j = 0; j < B.cols; j++) {
                int b= B.get(k, j);
                if (b != 0) {
                    String resultKey = i + "," + j;
                    int currentValue = result.data.getOrDefault(resultKey, 0);
                    result.data.put(resultKey, currentValue + a* b);
                }
            }
        }
        return result;
    }

    // 打印矩阵
    public void print() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print(get(i, j) + "\t");
            }
            System.out.println();
        }
    }
    // 获取行数
    public int getRows() {
        return rows;
    }
    // 获取列数
    public int getCols() {
        return cols;
    }
    // 测试代码
    public static void main(String[] args) {
        // 创建矩阵
        test A = new test(2, 3);
        A.set(0, 0, 1);
        A.set(0, 1, 0);
        A.set(0, 2, 3);
        A.set(1, 0, 0);
        A.set(1, 1, 0);
        A.set(1, 2, 0);
        test B = new test(3, 2);
        B.set(0, 0, 7);
        B.set(0, 1, 0);
        B.set(1, 0, 0);
        B.set(1, 1, 0);
        B.set(2, 0, 11);
        B.set(2, 1, 0);
        // 计算矩阵乘法
        test C = multiply(A, B);
        C.print();
    }
}