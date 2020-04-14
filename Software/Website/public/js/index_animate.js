setTimeout(function() {
  var elements = document.getElementsByTagName('p')
  for(var i = 0; i < elements.length; i++)
  {
     elements.item(i).style.opacity = "1"
     elements.item(i).style.transform = "translate(0)"
  }
}, 500)
