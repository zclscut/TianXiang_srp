package com.example.studentandroid.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;
import java.util.List;

public class UserSqliteDBHelper extends SQLiteOpenHelper {
    private static final String DB_NAME = "user.db";
    private static final String TABLE_NAME = "user_info";
    private static final int DB_VERSION =1;
    private  static UserSqliteDBHelper mHelper = null;
    private SQLiteDatabase mRDB = null;
    private SQLiteDatabase mWDB = null;


    private UserSqliteDBHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    public static UserSqliteDBHelper getInstance(Context context) {
        if(mHelper == null) {
            mHelper = new UserSqliteDBHelper(context);
        }
        return mHelper;
    }

    //打开数据库读连接
    public SQLiteDatabase openReadLink() {
        if (mRDB == null || !mRDB.isOpen()) {
            mRDB = mHelper.getReadableDatabase();
        }
        return mRDB;
    }

    //打开数据库写连接
    public SQLiteDatabase openWriteLink() {
        if (mWDB == null || !mWDB.isOpen()) {
            mWDB = mHelper.getWritableDatabase();
        }
        return mWDB;
    }

    //关闭数据库连接
    public void closelink() {
        if(mRDB != null && mRDB.isOpen()) {
            mRDB.close();
            mRDB = null;
        }
        if(mWDB != null && mWDB.isOpen()) {
            mWDB.close();
            mWDB = null;
        }
    }


    //创建数据库
    @Override
    public void onCreate(SQLiteDatabase db) {
        String sql = "CREATE TABLE IF NOT EXISTS "+TABLE_NAME+" ("+
                "_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," +
                " mail VARCHAR NOT NULL," +
                " password VARCHAR NOT NULL," +
                " remember INTEGER NOT NULL);";
        db.execSQL(sql);

    }

    //数据库升级
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }
    public void save(User user) {
        //存在的话先删除再添加
        try{
            mWDB.beginTransaction();
            delete(user);
            insert(user);
            mWDB.setTransactionSuccessful();
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            mWDB.endTransaction();
        }
    }
    //删除
    public long delete(User user) {
        return mWDB.delete(TABLE_NAME, "mail=?", new String[]{user.mail});
    }


    //插入
    public long insert(User user) {
        ContentValues values = new ContentValues();
        values.put("mail", user.mail);
        values.put("password", user.password);
        values.put("remember", user.remember);
        return mWDB.insert(TABLE_NAME, null, values);
    }

    //查询出最后输入的账号密码
    public User queryTop() {
        User user = null;
        //String sql = "select * from "+TABLE_NAME + " where remember = 1 ORDER BY _id DESC limit 1";
        String sql = "select * from "+TABLE_NAME + " ORDER BY _id DESC limit 1";
        Cursor cursor = mRDB.rawQuery(sql, null);
        if (cursor.moveToNext()) {
            user = new User();
            user.id = cursor.getInt(0);
            user.mail = cursor.getString(1);
            user.password = cursor.getString(2);
            user.remember = (cursor.getInt(3) == 0) ? false : true;
        }
        return user;
    }

    //
    public User queryByMail(String mail) {
        User user = null;
        Cursor cursor = mRDB.query(TABLE_NAME, null, "mail=? and remember = 1",
                new String[]{mail}, null, null, null);
        if (cursor.moveToNext()) {
            user = new User();
            user.id = cursor.getInt(0);
            user.mail = cursor.getString(1);
            user.password = cursor.getString(2);
            user.remember = (cursor.getInt(3) == 0) ? false : true;
        }
        return user;

    }


//    //删除所有
//    public void deleteAll() {
//        mWDB.delete(TABLE_NAME, "1=1", null);
//    }
//
//    //根据邮箱删除
//    public long deleteByMail(String mail) {
//        return mWDB.delete(TABLE_NAME, "mail=?", new String[]{mail});
//    }
//
//    //根据邮箱修改
//    public long update(User user) {
//        ContentValues values = new ContentValues();
//        values.put("mail", user.mail);
//        values.put("password", user.password);
//        values.put("remember", user.remember);
//        return mWDB.update(TABLE_NAME, values, "mail=?", new String[]{user.mail});
//    }
//
//    //查询所有
//    public List<User> queryAll() {
//        List<User> list = new ArrayList<>();
//        Cursor cursor = mRDB.query(TABLE_NAME, null, null,
//                null, null, null, null);
//        while (cursor.moveToNext()) {
//            User user = new User();
//            user.id = cursor.getInt(0);
//            user.mail = cursor.getString(1);
//            user.password = cursor.getString(2);
//            user.remember = (cursor.getInt(3 )== 0) ? false : true;
//            list.add(user);
//        }
//        return list;
//    }
//
//    public List<User> queryByMail(String mail) {
//        List<User> list = new ArrayList<>();
//        Cursor cursor = mRDB.query(TABLE_NAME, null, "mail=?",
//                new String[]{mail}, null, null, null);
//        while (cursor.moveToNext()) {
//            User user = new User();
//            user.id = cursor.getInt(0);
//            user.mail = cursor.getString(1);
//            user.password = cursor.getString(2);
//            user.remember = (cursor.getInt(3 )== 0) ? false : true;
//            list.add(user);
//        }
//        return list;
//    }

}

