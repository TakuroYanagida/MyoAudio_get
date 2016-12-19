void setup() {
  Serial.begin(115200);//レート選択 115200 57600 38400
}

int a0;
int a1;

void loop() {
  a0 = analogRead(1); //analog0から読み込み
  //a1 = analogRead(1); //analog0から読み込み
  Serial.print(a0); //シリアル通信でPCへデータ送信
  Serial.print(",");
}
