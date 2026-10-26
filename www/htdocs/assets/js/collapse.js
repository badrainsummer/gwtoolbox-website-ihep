var elements = document.getElementsByTagName("div");
// collapse all sections
for (var i = 0; i < elements.length; i++) {
  if (elements[i].className == "elementscollapse") {
    elements[i].style.display="none";
  } else if (elements[i].className == "labelcollapse") {
    elements[i].onclick=switchDisplay;
  }
}
//collapse or expand depending on state
function switchDisplay() {
  var parent = this.parentNode;
  var target = parent.getElementsByTagName("div")[1];
  if (target.style.display == "none") {
    target.style.display="block";
  } else {
    target.style.display="none";
  }
  return false;
}

