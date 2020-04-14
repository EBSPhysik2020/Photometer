//connect
var socket = io.connect()

var notificationContainer = document.getElementById('notificationContainer')
var colorList = document.getElementById('colorList')
var referenceList = document.getElementById('referenceList')
var inputSubstance = document.getElementById('substanceName')

var noColor = document.getElementById('noColor')
var colorHeader = document.getElementById('colorHeader')
var concentrationBox = document.getElementById('concentrationBox')
var concentration = document.getElementById('concentration')
var noReference = document.getElementById('noReference')
var referenceHeader = document.getElementById('referenceHeader')

var colors = []

var colorTemplate = `
  <div class="color">
    <div class="waveLength">
      <svg width="1rem" height="1rem" class="colorCircle">
        <circle cx="0.5rem" cy="0.5rem" r="0.5rem" fill="rgb({r}, {g}, {b})" />
      </svg>
      <p>{waveLength} nm</p>
    </div>
    <p class="measurementValue">{intensity} Lux</p>
  </div>`

var referenceTemplate = `
<div class="reference">
  <div class="waveLength">
    <svg width="1rem" height="1rem" class="colorCircle">
      <circle cx="0.5rem" cy="0.5rem" r="0.5rem" fill="rgb({r}, {g}, {b})" />
    </svg>
    <p>{waveLength} nm</p>
  </div>
  <p class="measurementValue">{intensity} Lux</p>
  <p class="measurementValue">{coefficient}</p>
</div>`

socket.on('colors', function(colorMeasurements) {
  colors = colorMeasurements.measurements
  noColor.style.display = "none"
  colorHeader.style.display = "flex"
  noReference.style.display = "flex"
  referenceHeader.style.display = "none"
  concentrationBox.style.display = "none"
  colorList.innerHTML = ""
  referenceList.innerHTML = ""
  clearChart()
  colors.forEach(color => {
    colorList.innerHTML += colorTemplate.replace('{r}', color.r).replace('{g}', color.g).replace('{b}', color.b).replace('{waveLength}', color.waveLength).replace('{intensity}', color.intensity)
  });
  if (colorMeasurements.notification == true) {
    openNotification(1, 'Leermessung beendet.', 5000)
  }
})

socket.on('measurement-progress', function(data) {
  openNotification(2, data.type + ' (' + data.progress + '%)', 0)
})

socket.on('reference', function(reference) {
  noReference.style.display = "none"
  referenceHeader.style.display = "flex"
  concentrationBox.style.display = "flex"
  concentration.innerHTML = reference.concentration + ' mol/l'
  referenceList.innerHTML = ""
  clearChart()
  reference.measurements.forEach((measurement, color) => {
    var color = colors[color]
    referenceList.innerHTML += referenceTemplate.replace('{r}', color.r).replace('{g}', color.g).replace('{b}', color.b).replace('{waveLength}', color.waveLength).replace('{intensity}', measurement.intensity).replace('{coefficient}', measurement.coefficient)
    addData(color.waveLength, measurement.coefficient)
  });
  if (reference.notification == true) {
    openNotification(1, 'Referenzmessung beendet.', 5000)
  }
})

socket.on('measurements', function(data) {
  if (data != null && data.notification == true) {
    openNotification(1, 'Messung beendet.', 5000)
  }
})

socket.on('delete', function(index) {
  openNotification(2, 'Messung #' + index + ' gelöscht.', 5000)
})

socket.on('disconnect', function() {
  socket.close()
  openNotification(0, 'Verbindung getrennt.', 0)
})
