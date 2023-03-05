﻿using MySqlConnector;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;
using static 在线学习状态分析系统家长端.globalVariable;

namespace 在线学习状态分析系统家长端
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();
            parName.Text = loginInfo.parentName;
            stuId.Text = loginInfo.studentId.ToString();
            int emocount;
            int faticount;
            int poscount;
            int foccount;
        }

        private MySqlConnection conn = new MySqlConnection("data source=127.0.0.1; Database=online_learning;user id=root; password=123456; charset=utf8");

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            int emocount = 0;
            int faticount = 0;
            int poscount = 0;
            int foccount = 0;
            string Label;
            string sql0 = string.Format("select * from study_state where student_id='{0}'", loginInfo.studentId);
            MySqlCommand cmd0 = new MySqlCommand(sql0, conn);
            conn.Open();
            MySqlDataReader reader = cmd0.ExecuteReader();
            while (reader.Read())
            {
                if (dateTime1.Value <= Convert.ToDateTime(reader["record_time"]))
                {
                    if (dateTime2.Value >= Convert.ToDateTime(reader["record_time"]))
                    {
                        switch (reader["state_key"])
                        {
                            case "1":
                                if (emotion.Checked)
                                {
                                    emocount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            Label = "情绪 积极 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "2":
                                            Label = "情绪 中性 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "3":
                                            Label = "情绪 消极 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                    }
                                }
                                break;
                            case "2":
                                if (fatigue.Checked)
                                {
                                    faticount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            Label = "清醒 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "2":
                                            Label = "临界状态 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "3":
                                            Label = "轻度疲劳 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "4":
                                            Label = "中度疲劳 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "5":
                                            Label = "重度疲劳 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                    }
                                }
                                break;
                            case "3":
                                if (posture.Checked)
                                {
                                    poscount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            Label = "坐姿正常 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "2":
                                            Label = "脸部朝前的颈部前倾 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "3":
                                            Label = "脸部朝下的颈部前倾 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "4":
                                            Label = "脊椎左右倾斜 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                    }
                                }
                                break;
                            case "4":
                                if (focus.Checked)
                                {
                                    foccount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            Label = "极其专注 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "2":
                                            Label = "专注 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "3":
                                            Label = "不专注 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                        case "4":
                                            Label = "极不专注 于" + reader["record_time"].ToString() + "\r\n";
                                            result.AppendText(Label);
                                            break;
                                    }
                                }
                                break;
                        }
                    }
                }
            }
            result.AppendText("查询结束\r\n");
            conn.Close();
        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }
    }
}
