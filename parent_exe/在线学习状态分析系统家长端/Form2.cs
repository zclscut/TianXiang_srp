using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using MySqlConnector;
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
using System.Diagnostics;

namespace 在线学习状态分析系统家长端
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();
            toolStripStatusLabel1.Text = "家长姓名："+loginInfo.parentName;
            toolStripStatusLabel2.Text = "学生ID："+loginInfo.studentId.ToString();
            int emocount;
            int faticount;
            int poscount;
            int foccount;
            this.ControlBox = true;
            this.MaximizeBox = false;
        }


        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string pyexePath = "database.exe";
            Process p = new Process();
            p.StartInfo.FileName = pyexePath;//需要执行的文件路径
            p.StartInfo.UseShellExecute = false; //必需
            p.StartInfo.RedirectStandardOutput = true;//输出参数设定
            p.StartInfo.RedirectStandardInput = true;//传入参数设定
            p.StartInfo.CreateNoWindow = true;
            p.StartInfo.Arguments = "";//参数以空格分隔，如果某个参数为空，可以传入””
            p.Start();
            string connstring = p.StandardOutput.ReadToEnd();
            p.WaitForExit();//关键，等待外部程序退出后才能往下执行}
            p.Close();

            MySqlConnection conn = new MySqlConnection(connstring);
            int emocount = 0;
            int faticount = 0;
            int poscount = 0;
            int foccount = 0;
            string Label;
            string sql0 = string.Format("select * from study_state where student_id='{0}'", loginInfo.studentId);
            MySqlCommand cmd0 = new MySqlCommand(sql0, conn);
            conn.Open();
            MySqlDataReader reader = cmd0.ExecuteReader();
            dataGridView1.Rows.Clear();
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
                                    int index = this.dataGridView1.Rows.Add();
                                    this.dataGridView1.Rows[index].Cells[0].Value = "情绪分析";
                                    emocount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "积极";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "2":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "中性";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "3":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "消极";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                    }
                                }
                                break;
                            case "2":
                                if (fatigue.Checked)
                                {
                                    int index = this.dataGridView1.Rows.Add();
                                    this.dataGridView1.Rows[index].Cells[0].Value = "疲劳度分析";
                                    faticount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "清醒";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "2":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "临界状态";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "3":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "轻度疲劳";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "4":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "中度疲劳";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "5":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "重度疲劳";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                    }
                                }
                                break;
                            case "3":
                                if (posture.Checked)
                                {
                                    int index = this.dataGridView1.Rows.Add();
                                    this.dataGridView1.Rows[index].Cells[0].Value = "坐姿分析";
                                    poscount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "坐姿正常";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "2":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "脸部朝前的颈部前倾";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "3":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "脸部朝下的颈部前倾";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "4":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "脊椎左右倾斜";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                    }
                                }
                                break;
                            case "4":
                                if (focus.Checked)
                                {
                                    int index = this.dataGridView1.Rows.Add();
                                    this.dataGridView1.Rows[index].Cells[0].Value = "专注度分析";
                                    foccount++;
                                    switch (reader["state_value"])
                                    {
                                        case "1":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "极其专注";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "2":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "专注";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "3":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "不专注";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                        case "4":
                                            this.dataGridView1.Rows[index].Cells[1].Value = "极不专注";
                                            this.dataGridView1.Rows[index].Cells[2].Value = reader["record_time"].ToString();
                                            break;
                                    }
                                }
                                break;
                        }
                    }
                }
            }
            conn.Close();
        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}
