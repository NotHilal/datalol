import { Component, Input, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnInit {
  @ViewChild('chartCanvas', { static: true }) chartCanvas!: ElementRef<HTMLCanvasElement>;
  @Input() type: ChartType = 'bar';
  @Input() data: any;
  @Input() options: any = {};
  @Input() title: string = '';

  private chart: Chart | null = null;

  ngOnInit() {
    this.createChart();
  }

  ngOnChanges() {
    if (this.chart) {
      this.updateChart();
    }
  }

  private createChart() {
    if (!this.chartCanvas || !this.data) return;

    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    if (!ctx) return;

    const config: ChartConfiguration = {
      type: this.type,
      data: this.data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              color: '#f0e6d2',
              font: {
                size: 12
              }
            }
          },
          title: {
            display: !!this.title,
            text: this.title,
            color: '#f0e6d2',
            font: {
              size: 16,
              weight: 'bold'
            }
          },
          tooltip: {
            backgroundColor: 'rgba(30, 35, 40, 0.95)',
            titleColor: '#f0e6d2',
            bodyColor: '#a09b8c',
            borderColor: '#3c3c41',
            borderWidth: 1,
            padding: 12,
            displayColors: true
          }
        },
        scales: this.type !== 'pie' && this.type !== 'doughnut' ? {
          x: {
            ticks: {
              color: '#a09b8c'
            },
            grid: {
              color: 'rgba(60, 60, 65, 0.3)'
            }
          },
          y: {
            ticks: {
              color: '#a09b8c'
            },
            grid: {
              color: 'rgba(60, 60, 65, 0.3)'
            }
          }
        } : undefined,
        ...this.options
      }
    };

    this.chart = new Chart(ctx, config);
  }

  private updateChart() {
    if (!this.chart) return;

    this.chart.data = this.data;
    this.chart.update();
  }

  ngOnDestroy() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
}
