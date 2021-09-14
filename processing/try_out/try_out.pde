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
public class pupila{
  private float x;
  private float y;
  private float faceW;
  private float faceH;
  private float facex;
  private float facey;
}
Eyes eye1 = new Eyes();
Eyes eye2 = new Eyes();
pupila pupila1 = new pupila();
pupila pupila2 = new pupila();

Client myClient; 
String dataIn = "0.4375,0.328125_1.2666666666666666,0.9333333333333333_1.030701754385965,0.49580711788601345#1.030701754385965,0.49580711788601345"; 
int data;
int g = 0;
int add = 0;
int Eyes_sp = 43;
float Expand = 1.75;
float Grid = 400.0;
public void setup(){
  size(800,800);
  eye1.x = (float) width / 2 - Eyes_sp;
  eye1.y = (float) height / 3;
  eye1.rad = (float) 50;
  eye2.x = (float) width / 2 + Eyes_sp;
  eye2.y = (float) height / 3;
  eye2.rad = (float) 50;
  myClient = new Client(this, "127.0.0.1", 5000);
  noLoop();
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
  myClient = new Client(this, "127.0.0.1", 5000);

  String[] features =dataIn.split("_");
  Float[] face_proportion = new Float[] {stringToTuple(features[0])[0],stringToTuple(features[0])[1]};
  Float[] face_coords = new Float[] {stringToTuple(features[1])[0],stringToTuple(features[1])[1]};
  String[] eyes = features[2].split("#");
  Float[][] eyes_coords = new Float[][] { stringToTuple(eyes[0]), stringToTuple(eyes[1]) } ;
  pupila1.x = (float) eyes_coords[0][0]+.3;
  pupila1.y = (float) eyes_coords[0][1]+.1;
  pupila1.faceW = (float) face_proportion[0];
  pupila1.faceH = (float) face_proportion[1];
  pupila2.x = (float) eyes_coords[1][0]+.3;
  pupila2.y = (float) eyes_coords[1][1]+.1;
  pupila2.faceW = (float) face_proportion[0];
  pupila2.faceH = (float) face_proportion[1];
  pupila1.facex = (float) face_coords[0];
  pupila1.facey = (float) face_coords[1];
  pupila2.facex = (float) face_coords[0];
  pupila2.facey = (float) face_coords[1];
 
  /* punto  */

   /* Face Shape */
  fill(160,100,50);
  ellipse(pupila1.facex*Grid, pupila1.facey*Grid, pupila1.faceW*Grid ,pupila1.faceH*Grid);
  /* retina 1  */
  fill(255);
  ellipse(pupila1.facex*Grid-Eyes_sp, pupila1.facey*Grid -abs(eye1.y-eye1.y+20), (0.5)*Grid*pupila1.faceW, (0.5)*Grid*pupila1.faceH);
  
  /* pupila 1  */
  fill(0);
  ellipse((pupila1.facex*Grid-Eyes_sp-(0.5)*Grid*pupila1.faceW)+((0.2)*Grid*pupila1.faceW)*pupila1.x,(pupila1.facey*Grid -abs(eye1.y-eye1.y+20)-(0.3)*Grid*pupila1.faceH)+((0.5)*Grid*pupila1.faceH*pupila1.y), (0.071)*Grid*pupila1.faceW,0.071*Grid*pupila1.faceH);
  
 
 
  /* Retina 2  */
  fill(255);
  ellipse(pupila1.facex*Grid+Eyes_sp, pupila1.facey*Grid -abs(eye1.y-eye1.y+20), (0.5)*Grid*pupila1.faceW, (0.5)*Grid*pupila1.faceH);
  
  /* pupila 2  */
  fill(0);
  ellipse((pupila2.facex*Grid+Eyes_sp-(0.5)*Grid*pupila2.faceW)+((0.2)*Grid*pupila2.faceW)*pupila1.x,(pupila2.facey*Grid -abs(eye1.y-eye1.y+20)-(0.3)*Grid*pupila1.faceH)+((0.5)*Grid*pupila1.faceH*pupila1.y), (0.071)*Grid*pupila1.faceW,0.071*Grid*pupila1.faceH);
  
  
  /* Boca inferior arc(width/2+16, 200, 230, 50, 0, 3.1416);*/
    
  fill(240,0,150);
  arc(pupila1.facex*Grid,pupila1.facey*Grid+abs(eye1.y+20-eye1.y+100), (150/350)*Grid*pupila1.faceW, (80/350)*Grid*pupila1.faceW, 0,PI, CHORD );

 
}

void clientEvent(Client someClient) {
  print("Server Says:  ");
  dataIn = someClient.readString();
  print(dataIn);
  redraw();
}
