var checked = false
var popupOverlay = document.getElementById('popupOverlay')
var checkboxTick = document.getElementById('checkBoxTick')
var popupText = document.getElementById('popupText')
var toDelete = -1

var titleTemplate = 'Bist du dir sicher, dass die Messung #{index} gelöscht werden soll?'

function openDeletePopup(index) {
  toDelete = index
  checkBox.setAttribute("onClick", "toggleCheckbox()")
  checked = false
  checkboxTick.style.visibility = "hidden"
  popupOverlay.style.display = "flex"
  popupText.innerHTML = titleTemplate.replace('{index}', index)
}

function toggleCheckbox() {
  checked = !checked
  if (checked) {
    checkboxTick.style.visibility = "visible"
  } else {
    checkboxTick.style.visibility = "hidden"
  }
}

function confirmDeletion() {
  deleteMeasurement(toDelete, checked)
  popupOverlay.style.display = "none"
}

function cancel() {
  popupOverlay.style.display = "none"
}
