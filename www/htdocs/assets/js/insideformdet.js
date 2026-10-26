function chooseDet(that){
  if(that.value < 0){
    document.getElementById("ifYesDet").style.display = "block";
  } else {
    document.getElementById("ifYesDet").style.display = "none";
  }
}
