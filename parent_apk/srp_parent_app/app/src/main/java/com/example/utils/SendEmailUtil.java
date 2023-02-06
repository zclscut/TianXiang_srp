package com.example.utils;

import java.util.Properties;
import java.util.Random;

import javax.mail.Authenticator;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMessage.RecipientType;

public class SendEmailUtil {
    private final static String sender="2759496411@qq.com";//发送邮件者，属于整个类不允许修改
    private String receiver="";//接收邮件者
    private String verifyCode="";//验证码
    private String emailTitle="邮箱验证码";//邮件标题
    private String emailContent=" 这是APP登录测试的邮箱验证码,请不要告诉其他人";

    //每个对象的验证码都相同，不能将产生验证码的方法设置为static
    private String creatVerifyCode(){
        int num=6;//设置6位数的验证码
        //生成num位数的随机数验证码
        Random random=new Random();
        for(int i=0;i<num;i++){
            this.verifyCode=this.verifyCode+random.nextInt(10);//this指向当前的对象
        }
        return this.verifyCode;
    }

    //开放为public供其他类访问
    public String getVerifyCode(){
        return creatVerifyCode();
    }

    //类的方法,为类所有,使用static
    public static void sendEmail(String receiver,String emailTitle,String emailContent) throws AddressException,MessagingException {
        // 创建Properties 类用于记录邮箱的一些属性
        Properties props = new Properties();
        // 表示SMTP发送邮件，必须进行身份验证
        props.put("mail.smtp.auth", "true");
        //此处填写SMTP服务器
        props.put("mail.smtp.host", "smtp.qq.com");
        //端口号，QQ邮箱端口587
        props.put("mail.smtp.port", "587");
        // 此处填写，写信人的账号
        props.put("mail.user", SendEmailUtil.sender);//发信人的账号固定，为整个类所有
        // 此处填写16位STMP口令
        props.put("mail.password", "xmmbiimddfnqdfeb");

        // 构建授权信息，用于进行SMTP进行身份验证
        Authenticator authenticator = new Authenticator() {

            protected PasswordAuthentication getPasswordAuthentication() {
                // 用户名、密码
                String userName = props.getProperty("mail.user");
                String password = props.getProperty("mail.password");
                return new PasswordAuthentication(userName, password);
            }
        };
        // 使用环境属性和授权信息，创建邮件会话
        Session mailSession = Session.getInstance(props, authenticator);
        // 创建邮件消息
        MimeMessage message = new MimeMessage(mailSession);
        // 设置发件人
        InternetAddress form = new InternetAddress(props.getProperty("mail.user"));
        message.setFrom(form);

        // 设置收件人的邮箱
        InternetAddress to = new InternetAddress(receiver);
        message.setRecipient(RecipientType.TO, to);

        // 设置邮件标题
        message.setSubject(emailTitle);

        // 设置邮件的内容体
        message.setContent(emailContent, "text/html;charset=UTF-8");

        // 最后当然就是发送邮件啦
        Transport.send(message);
    }
    public static void main(String[] args){
            try{
                String addInfo="这是APP的验证码,请不要告诉其他人";
                SendEmailUtil.sendEmail("fancilia20@gmail.com","验证码",new SendEmailUtil().getVerifyCode()+" "+addInfo);
            }catch(Exception e){
                System.out.println("发送出错");
            }
        }
}


