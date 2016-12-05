void setup() {
  Serial.begin(115200);//レート選択 115200 57600 38400
}

int a;

void loop() {
  a1 = analogRead(1); //analog1から読み込み
  Serial.print(a1); //シリアル通信でPCへデータ送信
}
