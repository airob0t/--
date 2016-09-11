#include <EEPROM.h>
#define usrl 8 //用于存储标识的字节长度
#define rol 20 //每条数据所占字节长度
int leng = EEPROM.length();
bool x = false;
int length = 10;  //默认密码长度
char c = ' ';
String com = "";
String password = "";
String check_str = "";

int checkpwd()
{
  String pass = "";
//  pass = "";
  while (Serial1.available() > 0 )
  {
    pass += char(Serial1.read());
    delay(3);
  }
  if ( pass == "AIRobot")
  {
    Serial1.println("Login successed.");
    return 1;
  }
  else if ( pass.length() > 0 )
  {
    Serial1.println("Login failed.");
    Serial1.println("Pleas input the password:");
  }
  return 0;
}


void clear()
{
  for ( int i = 0 ; i < leng ; i++ )
    EEPROM.write(i, 0);
  EEPROM.write(leng - 1, 0);
  Serial1.println("Cleared.");
}


int del(String str) 
{
  if ( find(str) < 0 )
  {
    Serial1.println("Not found!");
  }
  else
  {
    int point1 = find(str);
    int address = point1 * rol;
    for(int i =0;i<rol;i++)
    {
      EEPROM.write(address+i,0);
      delay(10);
    }
  }
  return 0;
}

int find(String str)
{
  int num = leng / rol;
  int i;
  for (i = 0; i < num; i++)
  {
    String t = "";
    for ( int a = 0; a < usrl; a++) // "123".length() == 3
    {
      t += (char)EEPROM.read(i * rol + a);
      delay(10);
    }
    if(t.indexOf(str)>=0)
      return i;
  }
  return -1;
}


int save(String str, String pwd)
{
  int point;
  int address;
  for (point = 0; point < leng/rol; point++)
  {
    if(!EEPROM.read(point * rol))
      break;
    delay(10);
  }
  address = point * rol;
  for(int i =0;i<str.length();i++)
  {
    EEPROM.write(address+i,str[i]);
    delay(10);
  }
  for(int i=0;i<pwd.length();i++)
  {
      EEPROM.write(address+usrl+i,pwd[i]);
      delay(10);
  }
  return 0;
}

String generate(int length)
{
  String pwd = "";
  int i;
  for (int ok = 0 ; ok == 0; )
  {
    pwd = "";
    for (i = 0; i < length; i++)
    {
      pwd += char(random(33, 127));   //随机生成字符
    }
//    Serial1.println(pwd);
    int low = 0, up = 0, num = 0, special = 0;
    for (i = 0; i < length; i++)  //确保含有大小写，数字，特殊字符
    {
      if (int(pwd[i]) < 123 && int(pwd[i]) > 96)
        low = 1;
      else if (int(pwd[i]) < 91 && int(pwd[i]) > 64)
        up = 1;
      else if (int(pwd[i]) < 58 && int(pwd[i]) > 47)
        num = 1;
      else if ((int(pwd[i]) < 48 && int(pwd[i]) > 32) || (int(pwd[i]) < 65 && int(pwd[i]) > 57) || (int(pwd[i]) < 97 && int(pwd[i]) > 90) || (int(pwd[i]) < 127 && int(pwd[i]) > 122))
        special = 1;
      if (low == 1 && up == 1 && num == 1 && special == 1)
        ok = 1;
    }
  }
  return pwd;
}

int output()
{
  int value;
  for (int i = 0; i < leng; i++)
  {
    Serial1.print(i);
    Serial1.print(':');
    value = EEPROM.read(i);
    if ( i != leng - 1)
    {
      if (value != 0)
      {
        Serial1.print((char)value);
      }
      else
      {
        Serial1.print(value);
      }
      Serial1.print('\t');
    }
    else
    {
      Serial1.println(value);
    }
    if ((i + 1) % 10 == 0)
    {
      Serial1.println();
    }
  }
}

void getstr()
{
  com = "";
  while ( Serial1.available() <= 0 )
  { }
  while ( Serial1.available() > 0 )
  {
    com += char(Serial1.read());
    delay(3);
  }
  Serial1.println("Rec:"+com);
}

void checklength()
{
  int x = 0 ;
  Serial1.println("Please input the length of password:");
  while (1)
  {
    if ( com.length() == 1 )
    {
      x = (int)com[0] - 48;
    }
    else if ( com.length() == 2 )
    {
      x = ((int)com[0] - 48) * 10 + ((int)com[1] - 48);
    }
    else
    {
      Serial1.println("erro!The length is not right.");
      Serial1.println("Please input the length:");
      continue;
    }
    if ( x >= 3 && x <= (rol - usrl))
    {
      length = x;
      Serial1.print("The length is ");
      Serial1.println(length);
      break;
    }
    else
    {
      Serial1.println("erro!The length is not right.");
      Serial1.println("Please input the length:");
    }
  }
}

String updatecheck()
{
//  String str1;
  String str2;
  Serial1.println("Please input the username(1-8):");
  getstr();
  while ( com.length() < 1 || com.length() >  usrl ) 
  {
    Serial1.println("Please input the username(1-8):");
    getstr();
  }
  check_str = com;
  Serial1.println("Please input the password(3-12):");
  getstr();
  while ( com.length() < 3 || com.length() >  (rol - usrl) )
  {
    Serial1.println("Please input the password(3-12):");
    getstr();
  }
  str2 = com;
  return str2;
}

int update(String str, String pwd)  //长度不足需置0
{
  del(str);
  save(str,pwd);
  return 0;
}


void print()
{
  Serial1.println("****************************");
  Serial1.println("* AIRobot password manager *");
  Serial1.println("****************************");
  Serial1.println("Please input the password:");
}

void setup() {
  Serial1.begin(9600);
  Keyboard.begin();
  /*
  while( !Serial1 )
  { ;}
  */
  print();  //AT
  while (checkpwd() == 0)
  {
    random(33, 127);  //引入时间变量确保下面的随机生成是真随机
  }
}


void loop()
{
  if ( !x )
  {
    Serial1.println("Please input the username(1-8):");
    x = !x;
  }
  getstr();
  if ( com != "" )
  {
    if ( com == "#l" )
    {
      checklength();
    }
    else if ( com == "#u" ) //有问题
    {
//      String str1 = "";
      String str2 = "";
      com = "";
      str2 = updatecheck();
      update(check_str, str2);
      check_str = "";
    }
    else if ( com == "#d" )
    {
      Serial1.println("Please input the username(1-8);");
      getstr();
      del(com);
      Serial1.println("Deleted.");
    }
    else if ( com == "#r" )
    {
       output();
     }
    else if ( com == "#c" )
    {
      Serial1.println("Are you sure?(y/n)");
      getstr();
      if ( com ==  "y")
      {
        clear();
      }
      else
      {
        Serial1.println("Bye.");
      }
    }
    else
    {
//      Serial1.println(com);
      if ( find(com) < 0)
      {
        if (com.length() >= 1 && com.length() <= 8 )
        {
          password = generate(length);
          save(com, password);
//          Serial1.println(password);
        }
        else
        {
          Serial1.println("The length is not right.");
        }
      }
      else
      {
        password = "";
        int point = find(com);
        int address = point * rol;
        for (int i = 0; i < (rol - usrl); i++)
        {
          int t = EEPROM.read(address + usrl + i);
          if( t != 0 )
            password += (char)t;
        }
//        Serial1.println(password);
      }
    }
//    output();
    Keyboard.print(password);
    com = "";
    password = "";
  }
}
