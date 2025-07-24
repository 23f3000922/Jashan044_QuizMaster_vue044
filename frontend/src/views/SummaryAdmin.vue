<template>
  <div class="container-fluid">
    
        <div class="py-4">
          <h2 class="text-white mb-4">Quiz Statistics</h2>
          <div v-if="loading" class="text-center text-white">Loading...</div>
          <div v-else>
            <div class="row g-4" >
              <div class="col-md-6">
                <div class="card shadow">
                  <div class="card-body" >
                    <h5 class="card-title">Highest Marks in Each Quiz</h5>
                    <Bar v-if="barChartData" :data="barChartData" :options="barChartOptions" />
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card shadow">
                  <div class="card-body">
                    <h5 class="card-title">Quiz Attempt Distribution</h5>
                    <Pie v-if="pieChartData" :data="pieChartData" :options="pieChartOptions" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      
  </div>
</template>

<script>
import { Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
)

export default {
  name: 'SummaryAdmin',
  components: { Bar, Pie },
  data() {
    return {
      loading: true,
      stats: []
    }
  },
  computed: {
    barChartData() {
      if (!this.stats.length) return null
      return {
        labels: this.stats.map(q => q.quiz_name),
        datasets: [
          {
            label: 'Highest Marks',
            backgroundColor: '#42b983',
            type : 'bar',
            data: this.stats.map(q => q.highest_mark)
          }
        ]
      }
    },
    barChartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: true, text: 'Highest Marks per Quiz' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    },
    pieChartData() {
      if (!this.stats.length) return null
      // Generate enough colors for all quizzes
      const baseColors = ['#42b983', '#ff6384', '#36a2eb', '#ffce56', '#8e44ad', '#e67e22', '#2ecc71', '#f39c12', '#d35400', '#c0392b']
      const colors = []
      for (let i = 0; i < this.stats.length; i++) {
        colors.push(baseColors[i % baseColors.length])
      }
      return {
        labels: this.stats.map(q => q.quiz_name),
        datasets: [
          {
            label: 'Attempts',
            backgroundColor: colors,
            data: this.stats.map(q => q.attempts)
          }
        ]
      }
    },
    pieChartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          title: { display: true, text: 'Quiz Attempt Distribution' }
        }
      }
    }
  },
  methods: {
    async fetchStats() {
      this.loading = true
      try {
        const response = await fetch('http://127.0.0.1:5000/api/quiz-stats')
        this.stats = await response.json()
      } catch (e) {
        alert('Failed to load quiz stats')
      }
      this.loading = false
    }
  },
  mounted() {
    this.fetchStats()
  }
}
</script>

<style scoped>
.sidebar {
  min-height: 100vh;
  border-right: 1px solid #dee2e6;
  background:linear-gradient(to right, #71cddd, #b076e4);
}

.nav-link.active {
  font-weight: bold;
  color: #0d6efd !important;
}

.card {
  min-height: 350px;
}

.modal {
  display: block;
  background: rgba(0, 0, 0, 0.2);
}

.modal-backdrop {
  z-index: 1040;
}

/* Chart card styling */
.card {
  border-radius: 1rem;
  background: #fff;
  height: auto;
}

.card-title {
  font-weight: 600;
  color: #f37822;
}

@media (max-width: 991px) {
  .row.g-4 {
    flex-direction: column;
  }
}
</style>