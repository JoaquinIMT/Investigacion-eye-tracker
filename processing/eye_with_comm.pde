mport processing.net.*;

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

public Float[] tupleToString(String str){
   String tp = str.split(",");
   Float n1 = Float.parseFloat(tp[0]);
   Float n2 = Float.parseFloat(tp[1]);
   Float[] array = new float[] {n1, n2};
   
}

public void draw(){
  background(220);
  Float ang = atan2(mouse.y - eye1.y, mouse.x - eye1.x);
  
  while(myClient.available() > 0) {
    
    dataIn = myClient.readString();
    
    println(dataIn);
     
  }
  
  String[] features =dataIn.split("_");
  Float[] face_proportion = features[0]
  Float[] face_coords = features[1]
  Array[Float[]] eyes_coords = features[2]
  
  face_proportion

  myClient = new Client(this, "127.0.0.1", 5000);
  if(g==0){
    mouse.x = Float.parseFloat(dataIn);
    add = 1;
  }
  if(g==1){
    mouse.y = Float.parseFloat(dataIn);
    add = -1;
  }
  /* punto  */
  fill(255);
  ellipse(mouse.x, mouse.y, 12, 12);
   /* Face Shape */
  fill(160,100,50);
  ellipse(eye1.x+Eyes_sp, eye1.y+20, 350, 350);
  /* retina 1  */
  fill(255);
  ellipse(eye1.x, eye1.y, eye1.rad*Expand, eye1.rad*Expand);
  
  /* pupila 1  */
  fill(0);
  ellipse(eye1.x + (eye1.rad / 4) * cos(ang), eye1.y + (eye1.rad / 4) * sin(ang), eye1.rad / 4,12);
  
  ang = atan2(mouse.y - eye2.y, mouse.x - eye2.x);
  
  /* Retina 2  */
  fill(255);
  ellipse(eye2.x, eye2.y, eye1.rad*Expand, eye1.rad*Expand);
  
  /* pupila 2  */
  fill(0);
  ellipse(eye2.x + (eye2.rad / 4) * cos(ang), eye2.y + (eye2.rad / 4) * sin(ang), eye2.rad / 4, 12);
  
  /* Boca inferior arc(width/2+16, 200, 230, 50, 0, 3.1416);*/
    
  fill(240,0,150);
  arc(eye1.x+Eyes_sp, eye1.y+100, 150, 80, 0,PI, CHORD );

  g = g + add;
}
