#include <hidboot.h>
#include <usbhub.h>
#include <Keyboard.h>

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
  Serial.print((mod.bmLeftCtrl   == 1) ? "C" : " ");
  Serial.print((mod.bmLeftShift  == 1) ? "S" : " ");
  Serial.print((mod.bmLeftAlt    == 1) ? "A" : " ");
  Serial.print((mod.bmLeftGUI    == 1) ? "G" : " ");

  Serial.print(" >");
  PrintHex<uint8_t>(key, 0x80);
  Serial.print("< ");
  Serial.print(key+136,HEX);
  //Keyboard.write(key+136);

  Serial.print((mod.bmRightCtrl   == 1) ? "C" : " ");
  Serial.print((mod.bmRightShift  == 1) ? "S" : " ");
  Serial.print((mod.bmRightAlt    == 1) ? "A" : " ");
  Serial.println((mod.bmRightGUI    == 1) ? "G" : " ");
};

void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key)
{
  Serial.print("DN ");
  PrintKey(mod, key);
  Keyboard.press(key+136);
  uint8_t c = OemToAscii(mod, key);

  if (c)
    OnKeyPressed(c);
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
      Serial.println("LeftCtrl pressed");
    }
    else
    {
      Keyboard.release(KEY_LEFT_CTRL);
      Serial.println("LeftCtrl released");
    }
  }
  if (beforeMod.bmLeftShift != afterMod.bmLeftShift) {
    LSStatus = !LSStatus;
    if(LSStatus){
      Keyboard.press(KEY_LEFT_SHIFT);
      Serial.println("LeftShift pressed");
    }
    else
    {
      Keyboard.release(KEY_LEFT_SHIFT);
      Serial.println("LeftShift released");
    }
  }
  if (beforeMod.bmLeftAlt != afterMod.bmLeftAlt) {
    LAStatus = !LAStatus;
    if(LAStatus){
      Keyboard.press(KEY_LEFT_ALT);
      Serial.println("LeftAlt pressed");
    }
    else
    {
      Keyboard.release(KEY_LEFT_ALT);
      Serial.println("LeftAlt released");
    }
  }
  if (beforeMod.bmLeftGUI != afterMod.bmLeftGUI) {
    LGStatus = !LGStatus;
    if(LGStatus){
      Keyboard.press(KEY_LEFT_GUI);
      Serial.println("LeftGui pressed");
    }
    else
    {
      Keyboard.release(KEY_LEFT_GUI);
      Serial.println("LeftGui released");
    }
  }

  if (beforeMod.bmRightCtrl != afterMod.bmRightCtrl) {
    RCStatus = !RCStatus;
    if(RCStatus){
      Keyboard.press(KEY_RIGHT_CTRL);
      Serial.println("RightCtrl pressed");
    }
    else
    {
      Keyboard.release(KEY_RIGHT_CTRL);
      Serial.println("RightCtrl released");
    }
  }
  if (beforeMod.bmRightShift != afterMod.bmRightShift) {
    RSStatus = !RSStatus;
    if(RSStatus){
      Keyboard.press(KEY_RIGHT_SHIFT);
      Serial.println("RightShift pressed");
    }
    else
    {
      Keyboard.release(KEY_RIGHT_SHIFT);
      Serial.println("RightShift released");
    }
  }
  if (beforeMod.bmRightAlt != afterMod.bmRightAlt) {
    RAStatus = !RAStatus;
    if(RAStatus){
      Keyboard.press(KEY_RIGHT_ALT);
      Serial.println("RightAlt pressed");
    }
    else
    {
      Keyboard.release(KEY_RIGHT_ALT);
      Serial.println("RightAlt released");
    }
  }
  if (beforeMod.bmRightGUI != afterMod.bmRightGUI) {
    RGStatus = !RGStatus;
    if(RGStatus){
      Keyboard.press(KEY_RIGHT_GUI);
      Serial.println("RightGui pressed");
    }
    else
    {
      Keyboard.release(KEY_RIGHT_GUI);
      Serial.println("RightGui released");
    }
  }

}

void KbdRptParser::OnKeyUp(uint8_t mod, uint8_t key)
{
  Serial.print("UP ");
  PrintKey(mod, key);
  Keyboard.release(key+136);
}

void KbdRptParser::OnKeyPressed(uint8_t key)
{
  Serial.print("ASCII: ");
  Serial.println((char)key);
};

USB     Usb;
//USBHub     Hub(&Usb);
HIDBoot<USB_HID_PROTOCOL_KEYBOARD>    HidKeyboard(&Usb);

uint32_t next_time;

KbdRptParser Prs;

void setup()
{
  Serial.begin( 115200 );
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  Serial.println("Start");

  if (Usb.Init() == -1)
    Serial.println("OSC did not start.");

  delay( 200 );

  next_time = millis() + 5000;

  HidKeyboard.SetReportParser(0, &Prs);
  Keyboard.begin();
}

void loop()
{
  Usb.Task();
}

