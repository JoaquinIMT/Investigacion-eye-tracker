import processing.net.*;

import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;


public class Eyes {
  private Float x;
  private Float y;
  private Float rad;
}
public class Raton{
  private float x;
  private float y;
}
Eyes eye1 = new Eyes();
Eyes eye2 = new Eyes();
Raton mouse = new Raton();

Client myClient; 
String dataIn; 
int data;
int g = 0;
int add = 0;
int Eyes_sp = 43;
float Expand = 1.75;
public void setup(){
  size(800,800);
  eye1.x = (float) width / 2 - Eyes_sp;
  eye1.y = (float) height / 3;
  eye1.rad = (float) 50;
  eye2.x = (float) width / 2 + Eyes_sp;
  eye2.y = (float) height / 3;
  eye2.rad = (float) 50;
  mouse.x = (float) mouseX;
  mouse.y = (float) mouseY;
  myClient = new Client(this, "127.0.0.1", 5000);
}

//Should be named s
public Float[] stringToTuple(String str){
   String[] tp = str.split(",");
   Float n1 = Float.parseFloat(tp[0]);
   Float n2 = Float.parseFloat(tp[1]);
   Float[] array = new Float[] {n1, n2};
   return(array);
}

public void draw(){
  background(220);
  Float ang = atan2(mouse.y - eye1.y, mouse.x - eye1.x);
  
  while(myClient.available() > 0) {
    
    dataIn = myClient.readString();
    
    println(dataIn);
     
  }
  
  String[] features =dataIn.split("_");
  Float[] face_proportion = stringToTuple(features[0]);
  Float[] face_coords = stringToTuple(features[1]);
  String[] eyes = features[2].split("#");
  Float[][] eyes_coords = new Float[][] { stringToTuple(eyes[0]), stringToTuple(eyes[1]) } ;
  

  myClient = new Client(this, "127.0.0.1", 5000);
  println(features);
}
