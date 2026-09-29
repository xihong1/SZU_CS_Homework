package com.lsy.task8;


import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

public class test {
    private static final String URL="https://ieeexplore.ieee.org/xpl/topAccessedArticles.jsp?punumber=9670";
    private static final Pattern PATTERN=Pattern.compile("<[^>]+>");
    private static final Pattern CHAR= Pattern.compile("[^a-zA-Z]");
    public static void main(String[] args) throws IOException, InterruptedException {
        HttpClient httpclient=HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
        HttpRequest request=HttpRequest.newBuilder()
                .uri(URI.create(URL))
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                .header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
                .timeout(java.time.Duration.ofSeconds(30)) // 设置超时时间
                .GET()
                .build();
        HttpResponse<String> response= httpclient.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode()!=200) {
            System.err.println(response.statusCode());
            return;
        }
        String body=response.body();
        String notagtext=PATTERN.matcher(body).replaceAll(" ");
        String readtext=CHAR.matcher(notagtext).replaceAll(" ").toLowerCase().replaceAll("\\s+"," ").trim();
        Map<String,Integer> map=new HashMap<>();
        String[] words=readtext.split(" ");
        for (String word:words) {
            if(word.length() < 2) {
                continue;
            }
            map.put(word,map.getOrDefault(word,0)+1);
        }
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.printf("%-15s %d%n", entry.getKey(), entry.getValue());
        }
    }
}
