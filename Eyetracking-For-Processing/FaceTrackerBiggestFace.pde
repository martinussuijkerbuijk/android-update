import gab.opencv.*; //uses opencv library
import processing.video.*;
import java.awt.*;
import processing.serial.*;

Capture video;
OpenCV opencv;
Serial myPort;  // Create object from Serial class

int newXpos, newYpos;
//These variables hold the x and y location for the middle of the detected face
int midFaceX = 0;
int midFaceY = 0;

void setup() {
  size(640, 480);
  
  String[] devices = Capture.list(); // gathers available webcams
  printArray(devices); // print available webcams
  
  video = new Capture(this, 640/2, 480/2, "name of webcam here if external otherwise deete it");
  opencv = new OpenCV(this, 640/2, 480/2);
  opencv.loadCascade(OpenCV.CASCADE_FRONTALFACE);  
  
  String portName = Serial.list()[1];
  printArray(Serial.list()); // prints available serial ports -> figuring out which arduino to send to
  myPort = new Serial(this, portName, 19200);   //Baud rate is set to 19200 to match the Arduino baud rate.
  
  video.start();
}


void draw() {
  scale(2);
  opencv.loadImage(video);
  
  println(frameCount); //Frame rate is set to 15 fps
  
  image(video, 0, 0 );
  
  noFill();
  stroke(0, 255, 0, 40);
  strokeWeight(3);
  Rectangle[] faces = opencv.detect();
  
  
  // Takes biggest face to track 
  
  int maxValueFace = 0;
  int maxIndex = -1;
  
  
  for (int i = 0; i < faces.length; i++ ) {
    
    if (faces[i].width > maxValueFace) {
      maxIndex = i;
      maxValueFace = faces[i].width;

    }
  }
  // sending a zero to arduino when no faces are detected
  if (maxIndex == -1) {
   println("No faces present");
   newXpos = 0;
   newYpos = 0;
   println(newXpos + "," + newYpos);
  }
  
  else {
      rect(faces[maxIndex].x, faces[maxIndex].y, faces[maxIndex].width, faces[maxIndex].height); //
      midFaceX = faces[maxIndex].x + (faces[maxIndex].width/2); // middle of the face
      midFaceY = faces[maxIndex].y + (faces[maxIndex].height/2); // middle of the face
      float xpos = map(midFaceX, 0, width/2, 150, 30); //maps range of servos L->R
      float ypos = map(midFaceY, 0, height/2, 78, 102); //maps range of servos U->D
      int newXpos = (int)xpos; //converts position X float into integer
      int newYpos = (int)ypos; //converts position Y float into integer
      myPort.write(newXpos+"x"); // send X coordinate to Arduino
      myPort.write(newYpos+"y"); // send Y coordinate to Arduino
      println(newXpos + "," + newYpos);
  }  
  // counting frames to save an image every 6 seconds 
  int resetFrame = 0;
  
  if (frameCount == 90) {
    frameCount = resetFrame;
    saveFrame("/path/to/image.jpg"); //overwrite every saved frame
  }
}


void captureEvent(Capture c) {
  c.read();
}