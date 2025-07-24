<template>
    <div class="container-fluid min-vh-100">
        
                <div class="container py-5">
                    <h2 class="mb-4 text-center">Your Quiz Scores</h2>
                    <div v-if="loading" class="text-center my-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>
                    <div v-else>
                        <div v-if="scores.length === 0" class="alert alert-info text-center">
                            You have not attempted any quizzes yet.
                        </div>
                        <div v-else>
                            <div class="row row-cols-1 row-cols-md-2 g-4" style="height: 70vh; overflow-y: auto;">
                                <div class="col" v-for="score in scores" :key="score.quiz_id">
                                    <div class="card shadow-sm border-primary h-60">
                                        <div class="card-body">
                                            <h5 class="card-title text-primary">{{ score.quiz_name }}</h5>
                                            <h6 class="card-subtitle mb-2 text-muted"> 
                                                Attempted on: <span class="fw-normal">{{  score.date_attempted && (new Date( score.date_attempted)).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) || 'N/A'
                                                    }}</span>
                                            </h6>
                                            <ul class="list-group list-group-flush mb-3">
                                                <li
                                                    class="list-group-item d-flex justify-content-between align-items-center">
                                                    <span>Total Questions</span>
                                                    <span class="badge bg-secondary">{{ score.total_questions }}</span>
                                                </li>
                                               
                                                <li
                                                    class="list-group-item d-flex justify-content-between align-items-center">
                                                    <span>Correct</span>
                                                    <span class="badge bg-success">{{ score.right }}</span>
                                                </li>
                                                <li
                                                    class="list-group-item d-flex justify-content-between align-items-center">
                                                    <span>Wrong</span>
                                                    <span class="badge bg-danger">{{ score.wrong }}</span>
                                                </li>
                                                <li
                                                    class="list-group-item d-flex justify-content-between align-items-center">
                                                    <span>Your Score</span>
                                                    <span class="badge bg-primary">{{ score.score }}</span>
                                                </li>
                                            </ul>
                                            <div class="progress mb-2" style="height: 20px;">
                                                <div class="progress-bar bg-success" role="progressbar"
                                                    :style="{ width: ((score.right / score.total_questions) * 100).toFixed(1) + '%' }"
                                                    :aria-valuenow="score.right" :aria-valuemin="0"
                                                    :aria-valuemax="score.total_questions">
                                                    {{ ((score.right / score.total_questions) * 100).toFixed(1) }}%
                                                </div>
                                            </div>
                                            <div class="text-end mb-2">
                                                <span class="badge bg-secondary">Quiz ID: {{ score.quiz_id }}</span>
                                            </div>
                                            <div class="text-center">
                                                <button
                                                    v-if="!score.reattempted"
                                                    class="btn btn-warning btn"
                                                    @click="openPaymentModal(score.quiz_id)"
                                                >
                                                    <font-awesome-icon icon="fa-solid fa-repeat" size="lg" /> Quiz
                                                </button>
                                                <span
                                                    v-else
                                                    class="badge bg-secondary"
                                                    title="You have already used your reattempt"
                                                >
                                                    Reattempted
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Payment Modal -->
                <div class="modal fade" tabindex="-1" :class="{ show: showPaymentModal }" style="display: block;" v-if="showPaymentModal">
                  <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                      <form @submit.prevent="processPayment">
                        <div class="modal-header">
                          <h5 class="modal-title">Quiz Reattempt Payment</h5>
                          <button type="button" class="btn-close" @click="closePaymentModal"></button>
                        </div>
                        <div class="modal-body">
                          <div class="mb-3">
                            <label class="form-label">Card Number</label>
                            <input type="text" class="form-control" v-model="paymentForm.cardNumber" maxlength="16" required>
                          </div>
                          <div class="mb-3">
                            <label class="form-label">Expiry Date</label>
                            <input type="text" class="form-control" v-model="paymentForm.expiry" placeholder="MM/YY" required>
                          </div>
                          <div class="mb-3">
                            <label class="form-label">CVV</label>
                            <input type="password" class="form-control" v-model="paymentForm.cvv" maxlength="4" required>
                          </div>
                          <div class="mb-3">
                            <label class="form-label">Name on Card</label>
                            <input type="text" class="form-control" v-model="paymentForm.name" required>
                          </div>
                          <div class="alert alert-info">
                            <strong>Amount:</strong> ₹50 for reattempting this quiz.
                          </div>
                          <div v-if="paymentError" class="alert alert-danger">
                            {{ paymentError }}
                          </div>
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" @click="closePaymentModal">Cancel</button>
                          <button type="submit" class="btn btn-success" :disabled="processingPayment">
                            <span v-if="processingPayment" class="spinner-border spinner-border-sm"></span>
                            Pay &amp; Reattempt
                          </button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
                <!-- End Payment Modal -->

            
    </div>
</template>
<script>
import axios from 'axios';
export default {
  name: "UserScore",
  data() {
    return {
      scores: [],
      loading: true,
      userId: null,
      showPaymentModal: false,
      paymentForm: {
        cardNumber: '',
        expiry: '',
        cvv: '',
        name: ''
      },
      paymentError: '',
      processingPayment: false,
      pendingQuizId: null,
    };
  },
  async created() {
    let user = sessionStorage.getItem('user')
      ? JSON.parse(sessionStorage.getItem('user'))
      : localStorage.getItem('user')
        ? JSON.parse(localStorage.getItem('user'))
        : null;
    let userId = user ? user.id : null;
    if (!userId) {
      alert('User not logged in!');
      this.loading = false;
      return;
    }
    this.userId = userId;
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/score?user_id=${userId}`);
      
      this.scores = (res.data.scores || []).map(score => ({
        ...score,
        reattempted: score.reattempted || false,
      }));
    } catch (e) {
      this.scores = [];
    }
    this.loading = false;
  },
  methods: {
    openPaymentModal(quizId) {
      this.pendingQuizId = quizId;
      this.showPaymentModal = true;
      this.paymentForm = {
        cardNumber: '',
        expiry: '',
        cvv: '',
        name: ''
      };
      this.paymentError = '';
      this.processingPayment = false;
    },
    closePaymentModal() {
      this.showPaymentModal = false;
      this.pendingQuizId = null;
      this.paymentError = '';
      this.processingPayment = false;
    },
    async processPayment() {
      this.paymentError = '';
      this.processingPayment = true;
      
      if (
        !this.paymentForm.cvv.match(/^\d{3,4}$/) 
       
      ) {
        this.paymentError = "Please fill all payment details correctly.";
        this.processingPayment = false;
        return;
      }
      
      setTimeout(() => {
        this.processingPayment = false;
        this.showPaymentModal = false;
        
        this.$router.push({ name: "QuizAttempt", params: { quizId: this.pendingQuizId } });
      }, 1500);
    },
  },
};
</script>

<style scoped>
.card {
  transition: box-shadow 0.2s;
}
.card:hover {
  box-shadow: 0 0 20px rgba(0,123,255,0.15);
}
.modal {
  display: block;
  background: rgba(0,0,0,0.3);
}
.modal .modal-dialog {
  margin-top: 10vh;
}
</style>