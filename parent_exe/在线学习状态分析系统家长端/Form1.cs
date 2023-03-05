using MySqlConnector;
using System.Data;
using static 在线学习状态分析系统家长端.globalVariable;

namespace 在线学习状态分析系统家长端
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load_1(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            //获取界面上用户输入信息
            string userName = phoneNumber.Text;
            string userPwd = passWord.Text;
            //数据库字符串
            string conString = "data source=127.0.0.1; Database=online_learning;user id=root; password=123456; charset=utf8";

            MySqlConnection conn = new MySqlConnection(conString);

            conn.Open();
            string sql = "select * from parent_info where parent_tel=@t1 and parent_pswd=@t2 ";
            //通过Connection对象和sql语句，创建Command对象
            MySqlCommand cmd = new MySqlCommand(sql, conn);
            //处理Command对象的参数
            cmd.Parameters.Add("@t1", MySqlDbType.VarChar).Value = userName;
            cmd.Parameters.Add("@t2", MySqlDbType.VarChar).Value = userPwd;
            //执行SQL语句
            if (cmd.ExecuteScalar() !=null)
            {
                MySqlDataReader reader = cmd.ExecuteReader();
                reader.Read();
                loginInfo.parentName = reader["parent_name"].ToString();
                loginInfo.studentId = Convert.ToInt32(reader["student_id"]);
                reader.Close();
                Form2 查询 = new Form2();
                this.Hide();
                userName = phoneNumber.Text;
                userPwd = passWord.Text;
                MessageBox.Show("欢迎进入！", "登陆成功！", MessageBoxButtons.OK, MessageBoxIcon.Information);
                查询.ShowDialog();//登录成功显示的下一个页面
                Application.ExitThread();
                //查到数据的处理逻辑代码
            }
            else
            {
                //没查到数据的处理逻辑代码    
                MessageBox.Show("用户名或者密码错误", "!提示", MessageBoxButtons.OK, MessageBoxIcon.Error);

            }
            //4.关闭数据库连接
            conn.Close();
        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            Form3 注册 = new Form3();
            this.Hide();
            注册.ShowDialog();
            Application.ExitThread();
        }
    }
}