var chart = d3.select('body').append('div').attr('class', 'chart');

chart.selectAll('div').data(data)
