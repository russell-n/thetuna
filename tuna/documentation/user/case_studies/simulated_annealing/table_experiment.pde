
Table data;
int columns;
int scalar;
int offset;
int rows;
float color_scalar;
float blue_scale, green_scale;
float red_scale;
int radius;
Integer big_x = null;
Integer big_y = null;
int big_x_index;
int big_y_index;
float big_r;
float big_g ;
float big_b;
float big_tput;
int text_size = 25;
int biggest_x;
int biggest_x_index;
int biggest_y;
int biggest_y_index;
float biggest_tput = 0;
float biggest_r;
float biggest_b;
float biggest_g;

void setup(){
  scalar = 10;
  radius = scalar/2;
  offset = scalar/2;
  color_scalar = 3;
  red_scale = 1.25;
  blue_scale = 1.5;
  green_scale = 1.5;
  textSize(text_size);
  data = loadTable("data_step50.csv");
  columns = data.getColumnCount();
  rows = data.getRowCount();
  size(rows * scalar, columns * scalar);
  rectMode(CORNER);
}

void draw(){
  for(int row=0; row < rows; row++){
   for(int column=0; column < columns; column++){
     float value = data.getFloat(row, column);
     float scaled_value = (value * color_scalar) % 255;
     
     float r = (scaled_value * red_scale) % 255;
     float g = (scaled_value * green_scale) % 255;
     float b = (scaled_value * blue_scale) % 255;
     fill(r, g, b);
     int x = row * scalar;
     int y = (column)* scalar;
     
     if(value > biggest_tput){
       biggest_tput = value;
       biggest_x = x;
       biggest_x_index = row;
       biggest_y = y;
       biggest_y_index = column;
       biggest_r = r;
       biggest_g = g;
       biggest_b = b;
       
     }
     if(mouseX > x && mouseX < x+scalar && mouseY > y && mouseY < y+scalar){
       big_x = x;
       big_y = y;
       big_r = r;
       big_g = g;
       big_b = b;
       big_x_index = row;
       big_y_index = column;
       big_tput = value;
       //ellipse(x,y,50,50);
     }
     stroke(0);
     strokeWeight(1);
            rect(x, y,  //<>//
             scalar, scalar);
   } //end column traversal
   
  }// end row traversal
  if(big_x != null){
    ellipseMode(CENTER);
    rectMode(CORNER);
    fill(big_r, big_g, big_b);
    ellipse(big_x, big_y, 50, 50);
  
    //textSize(radius);
    String output = String.format("<%s, %s> \n(%s Mbits/sec)", big_x_index,
            big_y_index, big_tput);
    
    //textSize(text_size * 1.1);
    float offset = textWidth(output )/2;
    fill(255);
    text(output, width/2 - offset, height/2);

    big_x = null;
    big_y = null;
  }
  
  if(keyPressed){
    if(key == 'b'){
       fill(255, 255, 255, 100);
       ellipse(biggest_x, biggest_y, 50, 50);
       stroke(255);
       strokeWeight(2 );
      line(0, biggest_y, width, biggest_y);
      line(biggest_x, 0, biggest_x, height);
       fill(255);
       String output = String.format("<%s, %s> \n(%s Mbits/sec)", biggest_x_index,
            biggest_y_index, biggest_tput);
       float offset = textWidth(output)/2;
      text(output, width/2 - offset, biggest_y);
    }
  }
}// end draw
