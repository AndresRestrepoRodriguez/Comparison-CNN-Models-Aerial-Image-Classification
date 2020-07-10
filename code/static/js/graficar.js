function graficarPalabrasRepetidas(canvas,data,labels){
  var barChart = new Chart(canvas, {
    type: 'horizontalBar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Palabras',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)'
        ]
      }]
    },
    options: {
        title: {
            display: true,
            text: 'Palabras más Repetidas'
        },
        scales: {
          xAxes: [{
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'Frecuencia'
              }
          }],
          yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Palabras'
              }
          }]

        }


    }
  });
  return barChart;
}

function graficarPalabrasRepetidasPie(canvas,data,labels){
  var barChart = new Chart(canvas, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Palabras',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)'
        ]
      }]
    },
    options: {
        title: {
            display: true,
            text: 'Palabras más Repetidas'

        }


    }
  });
  return barChart;
}

function graficarHashtagRepetidos(canvas,data,labels){
  var barChart = new Chart(canvas, {
    type: 'horizontalBar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Hashtag',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)'
        ]
      }]
    },
    options: {
        title: {
            display: true,
            text: 'Hashtag más Repetidos'
        },
        scales: {
          xAxes: [{
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'Frecuencia'
              }
          }],
          yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Hashtag'
              }
          }]

        }
    }
  });
  return barChart;
}

function graficarHashtagRepetidosPie(canvas,data,labels){
  var barChart = new Chart(canvas, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Hashtag',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)'
        ]
      }]
    },
    options: {
        title: {
            display: true,
            text: 'Hashtag más Repetidos'
        }
    }
  });
  return barChart;
}

function graficarHashtagPopularidad(canvas,data,labels,type){
  var barChart = new Chart(canvas, {
    type: type,
    data: {
      labels: labels,
      datasets: [{
        label: 'Popularidad Hashtag',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)'
        ]
      }]
    },
    options: {
        title: {
            display: true,
            text: 'Tweets con más de 500 RT'
        }
    }
  });
  return barChart;
}

function graficaScatter(canvas,data) {
  var scatterChart = new Chart(canvas, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Relación Hashtag vs RT',
            data: data,
            backgroundColor: [
              'rgba(72, 142, 61, 0.8)'
            ]
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                  display: true,
                  labelString: 'Número de Hashtag'
                }
            }],
            yAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: 'Número de Retweets'
                }
            }],

        },
        title: {
            display: true,
            text: 'Relación Cantidad Hashtag y cantidad RT'
        }

    }
  });
  return scatterChart;
}
