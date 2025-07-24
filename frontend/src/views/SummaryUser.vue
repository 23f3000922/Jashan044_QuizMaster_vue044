<template>
  <div class="container-fluid">

    <div class="container py-4 position-relative">
      <h2 class="mb-4">Your Quiz & Subject Performance</h2>
      <div v-if="loading" class="loading-overlay">
        <div class="spinner-border text-primary"></div>
        <div class="visually-hidden">Loading...</div>
      </div>
      <div v-else>
        <div class="row g-4">
          <div class="col-md-6">
            <div class="card shadow">
              <div class="card-body">
                <h5 class="card-title">Your Highest Marks in Each Quiz</h5>
                <Bar v-if="barChartData" :data="barChartData" :options="barChartOptions" />
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card shadow">
              <div class="card-body">
                <h5 class="card-title">Your Percentage Marks by Subject</h5>
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
  name: 'UserSummary',
  components: { Bar, Pie },
  props: {
    userId: {
      type: Number,
      required: false
    }
  },
  data() {
    return {
      loading: true,
      quizStats: [],
      subjectStats: [],
      internalUserId: null
    }
  },
  computed: {
    effectiveUserId() {
      // Prefer prop, fallback to internalUserId
      return this.userId || this.internalUserId
    },
    barChartData() {
      if (!this.quizStats.length) return null
      return {
        labels: this.quizStats.map(q => q.quiz_name),
        datasets: [
          {
            label: 'Highest Marks',
            backgroundColor: '#36a2eb',
            data: this.quizStats.map(q => q.highest_mark)
          }
        ]
      }
    },
    barChartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: true, text: 'Your Highest Marks per Quiz' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    },
    pieChartData() {
      if (!this.subjectStats.length) return null
      const baseColors = [ '#42b983', '#ff6384', '#36a2eb', '#ffce56', '#8e44ad', '#e67e22',
        '#1abc9c', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#2ecc71',
        '#34495e', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#f1c40f',
        '#e67e22', '#95a5a6', '#d35400', '#c0392b', '#7f8c8d', '#2c3e50']
      return {
        labels: this.subjectStats.map(s => s.subject_name),
        datasets: [
          {
            label: 'Quizzes Attempted',
            backgroundColor: this.subjectStats.map((_, i) => baseColors[i % baseColors.length]),
            data: this.subjectStats.map(s => s.attempted_count)
          }
        ]
      }
    },
    pieChartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          title: { display: true, text: 'Percentage of Marks by Subject' }
        }
      }
    }
  },
  methods: {
    async fetchStats() {
      this.loading = true
      const userId = this.effectiveUserId
      if (!userId) {
        alert('User ID not found. Please log in again.');
        this.loading = false
        return
      }
      try {

        const response = await fetch(`http://127.0.0.1:5000/api/user-summary?user_id=${userId}`)
        const data = await response.json()
        this.quizStats = data.quiz_stats
        this.subjectStats = data.subject_stats
      } catch (e) {
        alert('Failed to load user summary')
      }
      this.loading = false
    }
  },
  mounted() {
    // Try to get userId from prop, or fallback to localStorage/session
    if (!this.userId) {
      // Example: get user from localStorage after login
      const user = JSON.parse(localStorage.getItem('user'))
      if (user && user.id) {
        this.internalUserId = user.id
      }
    }
    this.fetchStats()
  }
}
</script>

<style scoped>
.main-gradient-bg {
  background: linear-gradient(to right, #f37822, #b076e4);
  min-height: 100vh;
}

.card {
  min-height: 350px;
  border-radius: 1rem;
  background: #fff;
}

.card-title {
  font-weight: 600;
  color: #36a2eb;
}

/* Loading overlay styles */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 1rem;
  min-height: 400px;
  transition: background 0.3s;
}

.spinner {
  border: 6px solid #f3f3f3;
  border-top: 6px solid #36a2eb;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 1.2rem;
  color: #333;
  font-weight: 500;
  letter-spacing: 0.05em;
}
</style>