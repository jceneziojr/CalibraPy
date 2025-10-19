int analogInputPort = A8; // Port that will be used to acquire data
int analogValue; // A variable to store data from analogInputPort

void setup()
{
  // Initializing serial communication :
  Serial.begin(115200);
}

void loop()
{

  analogValue = analogRead(analogInputPort); // Reading input
  Serial.println(analogValue); // Printing on serial

}