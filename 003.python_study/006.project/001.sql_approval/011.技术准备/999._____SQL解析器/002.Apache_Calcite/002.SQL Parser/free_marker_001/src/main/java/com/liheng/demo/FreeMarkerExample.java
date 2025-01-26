package com.liheng.demo;
import freemarker.template.*;

import java.io.*;
import java.util.*;

public class FreeMarkerExample {
    public static void main(String[] args) {
        // 配置 FreeMarker
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        
        try {
        	
            // 设置模板文件目录
            cfg.setDirectoryForTemplateLoading(new File("E:\\_python\\003.python_study\\006.project\\001.sql_approval\\011.技术准备\\999._____SQL解析器\\002.Apache_Calcite\\002.SQL Parser\\free_marker_001\\src\\main\\resources\\templates"));  // 确保 templates 文件夹在项目根目录下

            // 加载模板
            Template template = cfg.getTemplate("greeting.ftl");  // 你的模板文件名
            
            // 创建数据模型
            Map<String, Object> dataModel = new HashMap<>();
            dataModel.put("name", "John");
            
            // 创建输出流
            Writer out = new OutputStreamWriter(System.out);
            
            // 合并模板和数据模型
            template.process(dataModel, out);
            
            // 关闭输出流
            out.close();
        } catch (IOException | TemplateException e) {
            e.printStackTrace();
        }
    }
}

