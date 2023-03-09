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
using System.Diagnostics;

namespace 在线学习状态分析系统家长端
{
    public partial class Form3 : Form
    {
        public Form3()
        {
            InitializeComponent();
        }

        private string parentSex="man";
        private void button1_Click(object sender, EventArgs e)
        {
            Form1 登录 = new Form1();//想要打开的窗体界面
            this.Hide();
            登录.ShowDialog();
            Application.ExitThread();
        }

        private void button2_Click(object sender, EventArgs e)
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

            if (phoneNumber.Text == "")
            {
                MessageBox.Show("手机号不能为空！");
                return;
            }
            else if (passWord1.Text == "")
            {
                MessageBox.Show("密码不能为空!");
                return;
            }
            else if (passWord2.Text == "")
            {
                MessageBox.Show("确认密码不能为空!");
                return;
            }
            else if (passWord1.Text != passWord2.Text)
            {
                MessageBox.Show("确认密码不一致!");
                passWord1.Text = "";
                passWord2.Text = "";
                return;
            }
            try
            {
                string sql0 = string.Format("select * from student_info where student_id='{0}'", studentID.Text);
                MySqlCommand cmd0 = new MySqlCommand(sql0, conn);
                conn.Open();
                if(cmd0.ExecuteScalar()==null)
                {
                    MessageBox.Show("不存在该学生Id!");
                    return;
                }
                conn.Close();
                string sql = string.Format("select * from parent_info where parent_tel='{0}'", phoneNumber.Text);
                MySqlCommand cmd = new MySqlCommand(sql,conn);
                conn.Open();
                StringBuilder strsql = new StringBuilder();
                if (cmd.ExecuteScalar() == null)
                {
                    strsql.Append("insert into parent_info(`parent_id`,`parent_name`,`parent_sex`,`parent_tel`,`parent_email`,`parent_pswd`,`student_id`)");
                    strsql.Append("values(0,");
                    strsql.Append("'" + parentName.Text.Trim().ToString() + "',");
                    strsql.Append("'" + parentSex.Trim().ToString() + "',");
                    strsql.Append("'" + phoneNumber.Text.Trim().ToString() + "',");
                    strsql.Append("'" + parentEmail.Text.Trim().ToString() + "',");
                    strsql.Append("'" + passWord1.Text.Trim().ToString() + "',");
                    strsql.Append("'" + studentID.Text.Trim().ToString() + "'");
                    strsql.Append(")");
                    using (MySqlCommand cmd2 = new MySqlCommand(strsql.ToString(),conn))
                    {
                        cmd2.ExecuteNonQuery();
                    }
                    MessageBox.Show("注册成功！", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
                    this.Close();
                }
                else
                {
                    MessageBox.Show("用户已存在！", "信息提示", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
                    return;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
                Application.Exit();
            }
            finally
            {
                conn.Close();
                conn.Dispose();
                Form1 登录 = new Form1();//想要打开的窗体界面
                this.Hide();
                登录.ShowDialog();
                Application.ExitThread();
            }
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            parentSex = "man";
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            parentSex = "woman";
        }
    }

}
