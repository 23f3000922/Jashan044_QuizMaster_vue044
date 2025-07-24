<template>
  <div class="container py-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
      <span class="ms-2">Loading quiz...</span>
    </div>
    <div v-else-if="quiz && questions.length">
      <div class="card mb-3">
        <div class="card-body">
          <h4 class="card-title">{{ quiz.quiz_name }}</h4>
          <h6 class="card-subtitle mb-2 text-muted">
            Subject: {{ quiz.subject_name }}<br>
            Chapter: {{ quiz.chapter_name }}
          </h6>
          <p class="card-text">
            <strong><font-awesome-icon :icon="['fas', 'clock']" size="lg" /> Time Left:</strong>
            <span class="badge bg-warning text-dark">{{ formattedTime }}</span>
          </p>
        </div>
      </div>
      <div class="card mb-3">
        <div class="card-body mt-4">
          <h5>Question {{ currentIndex + 1 }} of {{ questions.length }}</h5>
          <p>{{ currentQuestion.question_statement }}</p>
          <div class="list-group">
            <label v-for="n in 4" :key="n" class="list-group-item">
              <input type="radio" :name="'option'" :value="n" v-model="userAnswers[currentIndex]" :disabled="submitted"
                class="form-check-input me-2" />
              {{ currentQuestion['option' + n] }}
            </label>
          </div>
        </div>
      </div>
      <div class="d-flex justify-content-between mb-3" style="margin: 20px; margin-left: 200px; margin-right: 200px;">
        <button class="btn btn-secondary" @click="prevQuestion" :disabled="currentIndex === 0 || submitted">
          <font-awesome-icon icon="fa-solid fa-arrow-left" size="lg" />
        </button>
        <button class="btn btn-secondary" @click="nextQuestion"
          :disabled="currentIndex === questions.length - 1 || submitted">
          <font-awesome-icon icon="fa-solid fa-arrow-right" size="lg" />
        </button>
        <button class="btn btn-success" @click="submitQuiz" :disabled="submitted">
          Submit 
        </button>
        <button class="btn btn-danger" @click="exitQuiz" :disabled="submitted">
          Exit 
        </button>
      </div>
      
      <div class="modal fade show" id="scoreModal" tabindex="-1" aria-labelledby="scoreModalLabel" aria-hidden="true"
        ref="scoreModal">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="scoreModalLabel">Quiz Result</h5>
              <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
            </div>
            <div class="modal-body text-center">
              <h4>Your Score: {{ score }} / {{ questions.length }}</h4>
              <p>Thank you for attempting the quiz!</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-primary" @click="closeModal">Close</button>
            </div>
          </div>
        </div>
      </div>
      <!-- End Modal -->
    </div>
    <div v-else class="alert alert-danger">
      Quiz or questions not found.
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "QuizAttempt",
  data() {
    return {
      quiz: null,
      questions: [],
      currentIndex: 0,
      userAnswers: [],
      loading: true,
      submitted: false,
      score: 0,
      timer: null,
      timeLeft: 0, // in second
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex] || {};
    },
    formattedTime() {
      const min = Math.floor(this.timeLeft / 60)
        .toString()
        .padStart(2, "0");
      const sec = (this.timeLeft % 60).toString().padStart(2, "0");
      return `${min}:${sec}`;
    },
  },
  async created() {
    const quizId = this.$route.params.quizId;
    await this.fetchQuiz(quizId);
    await this.fetchQuestions(quizId);
    this.loading = false;
    if (this.quiz && this.quiz.time_duration) {
      // time_duration is "HH:MM"
      const [h, m] = this.quiz.time_duration.split(":").map(Number);
      this.timeLeft = h * 3600 + m * 60;
      this.startTimer();
    } else {
      // Default: 10 minutes
      this.timeLeft = 600;
      this.startTimer();
    }
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  methods: {
    async fetchQuiz(quizId) {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/quizzes`);
        const allQuizzes = [
          ...(res.data.available_quizzes || []),
          ...(res.data.completed_quizzes || [])
        ];
        this.quiz = allQuizzes.find((q) => q.id == quizId);
      } catch (e) {
        this.quiz = null;
      }
    },
    async fetchQuestions(quizId) {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/question?quiz_id=${quizId}`);
        this.questions = res.data;
        this.userAnswers = Array(this.questions.length).fill(null);
      } catch (e) {
        this.questions = [];
      }
    },
    nextQuestion() {
      if (this.currentIndex < this.questions.length - 1) this.currentIndex++;
    },
    prevQuestion() {
      if (this.currentIndex > 0) this.currentIndex--;
    },
    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.timer);
          if (!this.submitted) this.submitQuiz();
        }
      }, 1000);
    },
    async submitQuiz() {
      if (this.submitted) return;
      clearInterval(this.timer);
      
      let score = 0;
      this.questions.forEach((q, idx) => {
        if (this.userAnswers[idx] == q.correct_option) score++;
      });
      this.score = score;
      this.submitted = true;
      
      try {
        
        const user = JSON.parse(localStorage.getItem("user"));
        await axios.post("http://127.0.0.1:5000/api/score", {
          quiz_id: this.quiz.id,
          user_id: user.id,
          total_scored: score,
        });
      } catch (e) {
        alert("Failed to submit quiz.");
        
      }
      
      this.showModal();
    },
    exitQuiz() {
      
      if (!this.submitted && confirm("Are you sure you want to exit the quiz? Your progress will not be saved.")) {
        clearInterval(this.timer);
        this.$router.push({ name: "UserDashboard" }); // Change route name as per your app
      } else if (this.submitted) {
        this.$router.push({ name: "UserDashboard" });
      }
    },
    showModal() {
      
      const modal = this.$refs.scoreModal;
      if (modal) {
        
        const bsModal = window.bootstrap
          ? new window.bootstrap.Modal(modal)
          : null;
        if (bsModal) bsModal.show();
        else modal.style.display = "block"; // fallback
      }
    },
    closeModal() {
      
      const modal = this.$refs.scoreModal;
      if (modal && window.bootstrap) {
        const bsModal = window.bootstrap.Modal.getInstance(modal);
        if (bsModal) bsModal.hide();
      }
      
      this.$router.push({ name: "UserDashboard" }); 
    },
  },
};
</script>


<style scoped>
.card {
  max-width: 700px;
  margin: 0 auto;
}
</style>