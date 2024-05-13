import ApexCharts = require('apexcharts');

const pieChart = document.getElementById('pie-chart');

const dataTarget = pieChart.getAttribute('data-target');
const plantCategory = JSON.parse(dataTarget);

const plantCategoryAmount = plantCategory.map((item: any) => item.amount);
const plantCategoryName = plantCategory.map((item: any) => item.name);

const generateColor = () => {
  return '#' + Math.floor(Math.random() * 16777215).toString(16);
};

const plantVarietyChart = document.getElementById('area-chart');
const plantVarietyData = plantVarietyChart.getAttribute('data-target');
const plantVariety = JSON.parse(plantVarietyData);

const counters = document.querySelectorAll(
  '.counter',
) as NodeListOf<HTMLElement>;
const speed = 400;

counters.forEach(counter => {
  const animate = () => {
    const value = +counter.getAttribute('amount');
    const data = +counter.innerText;

    const time = value / speed;
    if (data < value) {
      counter.innerText = Math.ceil(data + time).toString();
      setTimeout(animate, 1);
    } else {
      counter.innerText = value.toString();
    }
  };

  animate();
});

const getChartOptions = () => {
  return {
    series: plantCategoryAmount,
    colors: plantCategoryAmount.map(() => generateColor()),
    chart: {
      height: 420,
      width: '100%',
      type: 'pie',
    },
    stroke: {
      colors: ['white'],
      lineCap: '',
    },
    plotOptions: {
      pie: {
        labels: {
          show: true,
        },
        size: '100%',
        dataLabels: {
          offset: -25,
        },
      },
    },
    labels: plantCategoryName,
    dataLabels: {
      enabled: true,
      style: {
        fontFamily: 'Inter, sans-serif',
      },
    },
    legend: {
      position: 'bottom',
      fontFamily: 'Inter, sans-serif',
    },
    yaxis: {
      labels: {
        formatter: function (value: string) {
          return value + '%';
        },
      },
    },
    xaxis: {
      labels: {
        formatter: function (value: string) {
          return value + '%';
        },
      },
      axisTicks: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
    },
  };
};

if (document.getElementById('pie-chart') && typeof ApexCharts !== 'undefined') {
  const chart = new ApexCharts(
    document.getElementById('pie-chart'),
    getChartOptions(),
  );
  chart.render();
}

const options = {
  chart: {
    height: '100%',
    maxWidth: '100%',
    type: 'area',
    fontFamily: 'Inter, sans-serif',
    dropShadow: {
      enabled: false,
    },
    toolbar: {
      show: false,
    },
  },
  tooltip: {
    enabled: true,
    x: {
      show: false,
    },
  },
  fill: {
    type: 'gradient',
    gradient: {
      opacityFrom: 0.55,
      opacityTo: 0,
      shade: '#1C64F2',
      gradientToColors: ['#1C64F2'],
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 6,
  },
  grid: {
    show: false,
    strokeDashArray: 4,
    padding: {
      left: 2,
      right: 2,
      top: 0,
    },
  },
  series: [
    {
      name: 'New plants variety',
      data: plantVariety.map((item: any) => item.amount),
      color: '#1A56DB',
    },
  ],
  xaxis: {
    categories: plantVariety.map((item: any) => item.date),
    labels: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  yaxis: {
    show: false,
  },
};

if (
  document.getElementById('area-chart') &&
  typeof ApexCharts !== 'undefined'
) {
  const chart = new ApexCharts(document.getElementById('area-chart'), options);
  chart.render();
}
