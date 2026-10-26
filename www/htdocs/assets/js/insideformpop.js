function choosePop(caller, targetID){
  obj = document.getElementById(targetID)
  if(obj.style.display == "none"){
    obj.style.display = "block";
  } else {
    obj.style.display = "none";
  }
}

