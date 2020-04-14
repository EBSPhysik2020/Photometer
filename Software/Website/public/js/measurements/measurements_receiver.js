//connect
var socket = io.connect()
var colors = []
var measurements = []

var chart = new MeasurementChart(document.getElementById('chart'))

var tabContainer = document.getElementById('tabContainer')
var list = document.getElementById('list')
var listHeader = document.getElementById('listHeader')
var noData = document.getElementById('noData')

var popupOverlay = document.getElementById('popupOverlay')
var checkBox = document.getElementById('checkBox')

var selectedColor = 0

var tabTemplate = `
  <div class="tabItem selected" onClick="selectTab(this, {color})">
    <svg width="1rem" height="1rem">
      <circle cx="0.5rem" cy="0.5rem" r="0.5rem" fill="rgb({r}, {g}, {b})" />
    </svg>
    <p>{waveLength} nm</p>
  </div>`

var measurementTemplate = `
  <div class="measurement">
      <p class="measurementIndex">#{index}</p>
      <p class="measurementValue">{intensity} Lux</p>
      <p class="measurementValue">{extinction} </p>
      <p class="measurementValue">{concentration} g/l</p>
      {deleteable}
  </div>`

var deleteableTemplate = `<img src="images/delete.svg" alt="" class="measurementDelete" onClick="requestDeleteMeasurement({index})">`

/*
    Socket Receiver
*/

socket.on('disconnect', function() {
  socket.close()
  openNotification(0, 'Verbindung getrennt.', 0)
})

socket.on('measurement-progress', function(data) {
  openNotification(2, data.type + ' (' + data.progress + '%)', 0)
})

socket.on('colors', function(color) {
  reset()
  color.measurements.forEach((measurement, color) => {
    colors.push(measurement)
    measurements.push([])
    var add = tabTemplate.replace('{color}', color).replace('{r}', measurement.r).replace('{g}', measurement.g).replace('{b}', measurement.b).replace('{waveLength}', measurement.waveLength)
    if (color != 0) {
      add = add.replace(' selected', '')
    }
    tabContainer.innerHTML += add;
    chart.addColor(measurement)
  });
  if (color.notification == true) {
    openNotification(1, 'Leermessung beendet.', 5000)
  }
})

socket.on('reference', function(reference) {
  removeMeasurements()
  reference.measurements.forEach((measurement, color) => {
    measurement.concentration = reference.concentration
    addMeasurement(color, measurement)
  });
  if (reference.notification == true) {
    openNotification(1, 'Referenzmessung beendet.', 5000)
  }
})

socket.on('measurements', function(data) {
  if (data == null) {
    colors.forEach((color, index) => {
      addMeasurement(index, null)
    });
    return
  }
  data.measurements.forEach((measurement, color) => {
    addMeasurement(color, measurement)
  });
  if (data.notification == true) {
    openNotification(1, 'Messung beendet.', 5000)
  }
})

socket.on('delete', function(data) {
  deleteMeasurement(data, false)
  openNotification(3, 'Messung #' + data + ' gelöscht.', 5000)
})

/*
    GUI-Handler
*/

function requestDeleteMeasurement(index) {
  openDeletePopup(index)
}

function removeMeasurements() {
  for (var color = 0; color < measurements.length; color++) {
    measurements[color] = []
  }
  selectedColor = 0
  list.innerHTML = ''
  displayNoData()
  chart.removeMeasurements()
}

function deleteMeasurement(index, fromServer) {
  if (fromServer) {
    socket.emit('delete', index)
  } else {
    for (var color = 0; color < colors.length; color++) {
      list.children[measurements[color].length - index - 1].style.display = "none"
      chart.hideMeasurement(color, measurements[color][index].concentration)
      measurements[color][index] = null
    }
  }
}

function reset() {
  colors = []
  measurements = []
  selectedColor = 0
  tabContainer.innerHTML = ''
  list.innerHTML = ''
  displayNoData()
  chart.reset()
}

function addMeasurement(colorIndex, measurement) {
  var index = measurements[colorIndex].length
  measurements[colorIndex].push(measurement)
  chart.addMeasurement(colorIndex, measurement)
  if (colorIndex == selectedColor) {
    list.innerHTML = getMeasurementHTML(measurement, index) + list.innerHTML
    hideNoData()
  }
}

function selectTab(tabItem, color) {
  if (color == selectedColor) {
    return
  }
  tabContainer.childNodes.forEach((child, i) => {
    if (child.nodeType == Node.ELEMENT_NODE) {
      child.classList.remove('selected')
    }
  });
  selectedColor = color
  showMeasurements(color)
  tabItem.classList.add('selected')
}

function displayNoData() {
  noData.style.display = "block"
  listHeader.style.display = "none"
}

function hideNoData() {
  noData.style.display = "none"
  listHeader.style.display = "flex"
}

function showMeasurements(color) {
  var htmlData = ""
  measurements[color].forEach((measurement, i) => {
      htmlData = getMeasurementHTML(measurement, i) + htmlData
  });
  list.innerHTML = htmlData
  if (htmlData != "") {
    hideNoData()
  } else {
    displayNoData()
  }
}

function getMeasurementHTML(measurement, index) {
  if (measurement == null) {
    return '<div></div>'
  }
  var result = measurementTemplate.replace('{index}', index).replace('{intensity}', measurement.intensity).replace('{extinction}', measurement.extinction).replace('{concentration}', measurement.concentration)
  if (index == 0) {
    result = result.replace('{deleteable}', "")
  } else {
    result = result.replace('{deleteable}', deleteableTemplate.replace('{index}', index))
  }
  return result
}
