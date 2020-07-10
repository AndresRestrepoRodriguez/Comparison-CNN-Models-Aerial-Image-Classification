function download_image(canvasId,extension){
  var canvas = document.getElementById(canvasId);
  image = canvas.toDataURL("image/"+extension)
  var link = document.createElement('a');
  link.download = "my-image."+extension;
  link.href = image;
  link.click();
}





// This code is collected but useful, click below to jsfiddle link.
