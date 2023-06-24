
function printRadioValue() {
    var valA =0;
    var valB = 0;
    event.preventDefault();
  // Get the selected radio button
  var radio = document.querySelector('input[name="rather_be"]:checked');
  
  // Check if a radio button is selected
  if (radio) {
    // Get the value of the selected radio button
    var value = radio.value;
    
    // Print the value to the console
    console.log(value);
    
    // Print the value to the page
    var output = document.getElementById('rather_be');
    output.innerHTML = "The value of Rather Be is: " + value;
  }
  if(value == "A"){
      valA ++;
  }
    else{
        valB ++;
    }
    
    
  var radio2 = document.querySelector('input[name="drink"]:checked');
  
  // Check if a radio button is selected
  if (radio2) {
    // Get the value of the selected radio button
    var value2 = radio2.value;
    
    // Print the value to the console
    console.log(value2);
    
    // Print the value to the page
    var output2 = document.getElementById('drink');
    output2.innerHTML = "The value of Drink is: " + value2;
  }
    
      if(value2 == "A"){
      valA ++;
  }
    else{
        valB ++;
    }
    
    
    
    
    
var radio3 = document.querySelector('input[name="wardrobe"]:checked');
  
  // Check if a radio button is selected
  if (radio3) {
    // Get the value of the selected radio button
    var value3 = radio3.value;
    
    // Print the value to the console
    console.log(value3);
    
    // Print the value to the page
    var output3 = document.getElementById('wardrobe');
    output3.innerHTML = "The value of Drink is: " + value3;
  }
    
      if(value3 == "A"){
      valA ++;
  }
    else{
        valB ++;
    }
    
    

    var radio4 = document.querySelector('input[name="friendship"]:checked');
  
  // Check if a radio button is selected
  if (radio4) {
    // Get the value of the selected radio button
    var value4 = radio4.value;
    
    // Print the value to the console
    console.log(value4);
    
    // Print the value to the page
    var output4 = document.getElementById('friendship');
    output4.innerHTML = "The value of Drink is: " + value4;
  }
    
      if(value4 == "A"){
      valA ++;
  }
    else{
        valB ++;
    }
    
    
  var radio5 = document.querySelector('input[name="enjoy"]:checked');
  
  // Check if a radio button is selected
  if (radio5) {
    // Get the value of the selected radio button
    var value5 = radio5.value;
    
    // Print the value to the console
    console.log(value5);
    
    // Print the value to the page
    var output5 = document.getElementById('enjoy');
    output5.innerHTML = "The value of Drink is: " + value5;
  }
      if(value5 == "A"){
      valA ++;
  }
    else{
        valB ++;
    }
    
   if(valA > valB){
       alert("Based on your answers, you would enjoy the fresh, fruity, and floral fragrances. Click here to view those scents.");
   } 
    else{
        alert("Based on your answers, you would enjoy the woody and warm fragrances. Click here to view those scents.");
    }
}