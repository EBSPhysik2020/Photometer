var notificationContainer = document.getElementById('notificationContainer')
var notificationMessage = document.getElementById('notificationMessage')
var notificationOverlay = document.getElementById('notificationOverlay')

var cancelHide = false

var types = [{
  icon: document.getElementById('notificationError'),
  fill: "255, 200, 200",
  border: "255, 0, 0"
}, {
  icon: document.getElementById('notificationSuccess'),
  fill: "200, 255, 200",
  border: "0, 255, 0"
}, {
  icon: document.getElementById('notificationSynchronize'),
  fill: "200, 200, 255",
  border: "0, 0, 255"
}, {
  icon: document.getElementById('notificationDelete'),
  fill: "200, 255, 200",
  border: "0, 255, 0"
}]

function closeNotification() {
  if (cancelHide) {
    cancelHide = false
    return
  }
  notificationContainer.style.transform = "translateY(0.5rem)"
  notificationContainer.style.opacity = "0"
  setTimeout(function() {
    notificationOverlay.style.display = "none"
  }, 200)
}

function hideIcons() {
  types.forEach((type, i) => {
    type.icon.style.display = "none"
  });
}

function openNotification(typeIndex, message, time) {
  var type = types[typeIndex]
  notificationOverlay.style.display = "block"
  notificationContainer.style.backgroundColor = "rgba(" + type.fill + ", 0.9)"
  notificationContainer.style.border = "2px solid rgb(" + type.border + ")"
  notificationContainer.style.transform = "translateY(0)"
  notificationContainer.style.opacity = "1"
  notificationMessage.innerHTML = message

  hideIcons()
  type.icon.style.display = "block"

  if (time > 0) {
    cancelHide = false
    setTimeout(function() {closeNotification()}, time)
  } else {
    cancelHide = true
  }
}
