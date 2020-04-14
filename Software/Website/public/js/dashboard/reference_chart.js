var chartElement = document.getElementById('chart')
var context = chartElement.getContext('2d')
Chart.defaults.global.defaultFontFamily = 'Raleway'

var chart = new Chart(context, {
  type: 'scatter',
  data: {
      datasets: [{
        label: "",
        showLine: true,
        borderColor: 'rgb(0, 0, 0, 1)',
        backgroundColor: 'rgba(0, 0, 0, 0)',
        borderWidth: 0,
        cubicInterpolationMode: "monotone"
      }]
  },
  options: {
      scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Koeffizient',
              padding: 0
            }
          }],
          xAxes: [{
              type: 'linear',
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'Wellenlänge (nm)'
              }
          }]
      }
  }
})

function addData(waveLength, coeffient) {
  chart.data.datasets[0].data.push({
    x: waveLength,
    y: coeffient
  })
  chart.update()
}

function clearChart() {
  chart.data.datasets[0].data = []
  chart.update()
}
