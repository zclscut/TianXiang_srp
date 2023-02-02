package com.example.studentandroid.database;

public class User {

    public int id;
    public String mail;
    public String password;
    public boolean remember = false;

    public User() {

    }

    public User(String users, String password, boolean remember) {
        this.mail = users;
        this.password = password;
        this.remember = remember;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", users='" + mail + '\'' +
                ", password='" + password + '\'' +
                ", remember=" + remember +
                '}';
    }
}
