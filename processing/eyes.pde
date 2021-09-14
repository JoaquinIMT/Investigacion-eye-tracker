import processing.net.*;

import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;


public class Eye {
  private Float x;
  private Float y;
  private Float rad;
}

Eye eye1 = new Eye();
Eye eye2 = new Eye();

Client myClient; 
String dataIn; 
int data;
int g = 0;
public void setup(){
  size(400,400);
  eye1.x = (float) width / 2 - 16;
  eye1.y = (float) height / 2;
  eye1.rad = (float) 32;
  eye2.x = (float) width / 2 + 16;
  eye2.y = (float) height / 2;
  eye2.rad = (float) 32;
  myClient = new Client(this, "127.0.0.1", 5000);
}


public void draw(){
  background(220);
  Float ang = atan2(mouseY - eye1.y, mouseX - eye1.x);
  
  if(myClient.available() > 0) {
    
    dataIn = myClient.readString();
    myClient.ip(); 
    println(dataIn);
     
    
  }
  myClient = new Client(this, "127.0.0.1", 5000);
  /*if(g==0){
    eye1.x = dataIn;
    g = 1;
  }
  if(g==1){
    eye1.x = dataIn;
    g = 1;
  }*/

 
 
  
  fill(255);
  ellipse(eye1.x, eye1.y, eye1.rad, 20);
  fill(0);
  ellipse(eye1.x + (eye1.rad / 4) * cos(ang), eye1.y + (eye1.rad / 4) * sin(ang), eye1.rad / 4,eye1.rad*2);
  
  ang = atan2(mouseY - eye2.y, mouseX - eye2.x);
  
  fill(255);
  ellipse(eye2.x, eye2.y, eye2.rad, 20);
  fill(0);
  ellipse(eye2.x + (eye2.rad / 4) * cos(ang), eye2.y + (eye2.rad / 4) * sin(ang), eye2.rad / 4, eye1.rad*2);
}
