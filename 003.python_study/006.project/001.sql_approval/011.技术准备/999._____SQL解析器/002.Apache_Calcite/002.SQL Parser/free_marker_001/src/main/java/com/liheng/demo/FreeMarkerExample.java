package com.liheng.demo;
import freemarker.template.*;

import java.io.*;
import java.util.*;

public class FreeMarkerExample {
    public static void main(String[] args) {
        // ���� FreeMarker
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        
        try {
        	
            // ����ģ���ļ�Ŀ¼
            cfg.setDirectoryForTemplateLoading(new File("E:\\_python\\003.python_study\\006.project\\001.sql_approval\\011.����׼��\\999._____SQL������\\002.Apache_Calcite\\002.SQL Parser\\free_marker_001\\src\\main\\resources\\templates"));  // ȷ�� templates �ļ�������Ŀ��Ŀ¼��

            // ����ģ��
            Template template = cfg.getTemplate("greeting.ftl");  // ���ģ���ļ���
            
            // ��������ģ��
            Map<String, Object> dataModel = new HashMap<>();
            dataModel.put("name", "John");
            
            // ���������
            Writer out = new OutputStreamWriter(System.out);
            
            // �ϲ�ģ�������ģ��
            template.process(dataModel, out);
            
            // �ر������
            out.close();
        } catch (IOException | TemplateException e) {
            e.printStackTrace();
        }
    }
}

