class Table {
  int rowCount;
  int columnCount;
  String[][] data;
  
  
  Table(String filename, String delimiter) {
    String[] rows = loadStrings(filename);
    data = new String[rows.length][];
    
    for (int i = 0; i < rows.length; i++) {
      if (trim(rows[i]).length() == 0) {
        continue; // skip empty rows
      }
      if (rows[i].startsWith("#")) {
        continue;  // skip comment lines
      }
      
      // split the row on the tabs
      String[] pieces = split(rows[i], delimiter);
      // copy to the table array
      data[rowCount] = pieces;
      rowCount++;
      columnCount = pieces.length;
      // this could be done in one fell swoop via:
      //data[rowCount++] = split(rows[i], TAB);
    }
     //<>//
    // resize the 'data' array as necessary
    data = (String[][]) subset(data, 0, rowCount);
  }
  
  
  int getRowCount() {
    return rowCount;
  }
  
  int getColumnCount(){
    return columnCount;
  }
  // find a row by its name, returns -1 if no row found
  int getRowIndex(String name) {
    for (int i = 0; i < rowCount; i++) {
      if (data[i][0].equals(name)) {
        return i;
      }
    }
    println("No row named '" + name + "' was found");
    return -1;
  }
  
  
  String getRowName(int row) {
    return getString(row, 0);
  }


  String getString(int rowIndex, int column) {
    return data[rowIndex][column];
  }

  
  String getString(String rowName, int column) {
    return getString(getRowIndex(rowName), column);
  }

  
  int getInt(String rowName, int column) {
    return parseInt(getString(rowName, column));
  }

  
  int getInt(int rowIndex, int column) {
    return parseInt(getString(rowIndex, column));
  }

  
  float getFloat(String rowName, int column) {
    return parseFloat(getString(rowName, column));
  }

  
  float getFloat(int rowIndex, int column) {
    return parseFloat(getString(rowIndex, column));
  }  
}


Table data;
int columns;
int scalar;
int offset;
int rows;
float color_scalar;
float blue_scale, green_scale;
float red_scale;
int radius;
int big_x = 0;
int big_y = 0;
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
  ellipse(width/2, height/2, 5,5);
  scalar = 10;
  radius = scalar/2;
  offset = scalar/2;
  color_scalar = 3;
  red_scale = 1.25;
  blue_scale = 1.5;
  green_scale = 1.5;
  textSize(text_size);
  //data = loadTable("data_step50.csv");
  data = new Table("../../../../_downloads/data_step50.csv", ",");
  columns = data.getColumnCount();
  rows = data.getRowCount();
  size(rows * scalar, columns * scalar);
  rectMode(CORNER);
  print("Ending Setup");
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
  //if(big_x != 0){
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

    big_x = 0;
    big_y = 0;
  //}
  
  if(keyPressed){
    if(key == 'b'){
       fill(255, 255, 255, 100);
       ellipse(biggest_x, biggest_y, 50, 50);
       stroke(255);
       strokeWeight(2 );
      line(0, biggest_y, width, biggest_y);
      line(biggest_x, 0, biggest_x, height);
       fill(255);
       String big_output = String.format("<%s, %s> \n(%s Mbits/sec)", biggest_x_index,
            biggest_y_index, biggest_tput);
       float big_offset = textWidth(big_output)/2;
      text(big_output, width/2 - big_offset, biggest_y);
    }
  }
noLoop();
}// end draw
