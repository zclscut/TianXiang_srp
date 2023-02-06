package com.example.utils;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class ConnectMySQL {
// MySQL 8.0 以下版本 - JDBC 驱动名及数据库 URL
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
    // static final String DB_URL = "jdbc:mysql://localhost:3306/RUNOOB";

    // MySQL 8.0 以上版本 - JDBC 驱动名及数据库 URL
//    static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    //本机ip192.168.1.7,192.168.145.4
    //服务器101.33.198.88
    static final String DB_URL = "jdbc:mysql://101.33.198.88:3306/online_learning?characterEncoding=utf-8&useSSL=false&serverTimezone=UTC";

    // 数据库的用户名与密码，需要根据自己的设置
    static final String USER = "root";
    static final String PASS = "123456";

    public static List<HashMap<String,String>> table=new ArrayList<>();

    public void doSql(String sql,int count,String[] paramStr,String option){
        if(table.size()>=0){
            table.clear();
        }
        //count是待定的参数数量,即问号？数量；paramStr是待插入sql语句中参数数量；option是操作类型，即query和others
        Connection conn = null;
        Statement stmt = null;
        try{
            // 注册 JDBC 驱动
            Class.forName(JDBC_DRIVER);

            // 打开链接
            System.out.println("连接数据库...");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);

            // 执行查询
            System.out.println(" 实例化Statement对象...");
            stmt = conn.createStatement();
            if(option.equals("query")){//进行数据查询，将表中每一条记录以HashMap形式存放在List中
                PreparedStatement ps=conn.prepareStatement(sql);
                for(int i=1;i<=count;i++){//index从1开始，将待定参数插入到sql语句中
                    ps.setString(i,paramStr[i-1]);
                }
                ResultSet rs = ps.executeQuery();
                int cnt = rs.getMetaData().getColumnCount();
                // 展开结果集数据库
                while(rs.next()){
                    HashMap<String,String> map=new HashMap<>();
                    // 通过字段检索
                    for (int i = 1; i <= cnt;i++) {
                        String field = rs.getMetaData().getColumnName(i);
                        map.put(field, rs.getString(field));
                    }
                    table.add(map);
                }
                rs.close();
            }
            else if(option.equals("query1")){
                Statement st = conn.createStatement();
                ResultSet res = st.executeQuery(sql);
                int cnt = res.getMetaData().getColumnCount();
                // 展开结果集数据库
                while (res.next()) {
                    HashMap<String, String> map = new HashMap<>();
                    // 通过字段检索
                    for (int i = 1; i <= cnt; i++) {
                        String field = res.getMetaData().getColumnName(i);
                        map.put(field, res.getString(field));
                    }
                    table.add(map);
                }
                res.close();
            }
            else if(option.equals("others1")){
                Statement st = conn.createStatement();
                st.execute(sql);
                st.close();
                table=null;
            }
            else{//进行更新、修改、删除
                PreparedStatement ps=conn.prepareStatement(sql);
                for(int i=1;i<=count;i++){
                    ps.setString(i,paramStr[i-1]);
                }
                ps.executeUpdate();
            }
            // 完成后关闭
            stmt.close();
            conn.close();
        }catch(SQLException se){
            // 处理 JDBC 错误
            se.printStackTrace();
        }catch(Exception e){
            // 处理 Class.forName 错误
            e.printStackTrace();
        }finally{
            // 关闭资源
            try{
                if(stmt!=null) stmt.close();
            }catch(SQLException se2){
            }// 什么都不做
            try{
                if(conn!=null) conn.close();
            }catch(SQLException se){
                se.printStackTrace();
            }
        }
        System.out.println("Goodbye!");
    }
//    public static void main(String[] args){
//        //查询
//        String sql="select * from parent_info where parent_id>=?";
//        new ConnectMySQL().doSql(sql,1,new String[]{"1"},"query");
//        System.out.println(ConnectMySQL.table.toString());
        //        //修改
//        String sql="update parent_info set parent_name=? where parent_id=1";
//        new ConnectMySQL().doSql(sql,1,new String[]{"Gussy"},"others");
//        //插入数据
//        String sql="insert into student_info values(?,?,?,?)";
//        new ConnectMySQL().doSql(sql,4,new String[]{"2","Gudday","man","123456"},"others");
////        删除数据
//        String sql="delete from student_info where student_id=?";
//        new ConnectMySQL().doSql(sql,1,new String[]{"2"},"others");
//    }
}
