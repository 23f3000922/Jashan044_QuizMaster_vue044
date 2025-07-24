<template>
   <div class="container-fluid min-vh-100">
    <br>
    <h1>Quiz Management</h1>
    <div class="container my-4">
      <div class="mx-auto p-2" style="width: 400px;">
        <form class="d-flex align-items-center" role="search">
          <input class="form-control me-2" v-model="searchQuery" type="search" placeholder="Search Quiz"
            aria-label="Search" /><font-awesome-icon icon="fa-solid fa-magnifying-glass" />
        </form>
      </div>
      <hr>
      <button class="btn  btn-outline-dark bolton mb-3" @click="openQuizModal()"><font-awesome-icon icon="fa-solid fa-plus"  /> Quiz</button>
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      
      <div v-else style="height: 70vh; overflow-y: auto;">
        <transition-group name="fade" tag="div" class="row">
          <div v-for="quiz in filteredQuiz" :key="quiz.id" class="col-md-3 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title fw-bold">{{ quiz.quiz_name }}</h5>
                <div>
                  <button class="btn btn-sm btn-outline-secondary me-2" @click="openQuestionModal(quiz)"><font-awesome-icon icon="fa-solid fa-eye" size="lg" /></button>
                </div>
                <hr>
                <h6 class="card-subtitle mb-2 text-muted">
                  Chapter: {{ quiz.chapter_name }}
                </h6>
                <p class="card-text">
                  <strong>Date:</strong> {{ quiz.date_of_quiz && (new Date(quiz.date_of_quiz)).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) }}<br>
                  <strong>Duration:</strong> {{ quiz.time_duration.split(':')[0] }}hour : {{ quiz.time_duration.split(':')[1] }}minutes<br>
                  <strong>Remarks:</strong> {{ quiz.remarks }}<br>
                  <strong>Questions:</strong> {{ quiz.number_of_questions }}
                </p>
                <div style="margin-top: 10px;">
                  <button class="btn bolton btn-sm btn-outline-dark me-2" @click="openAddQuestionModal(quiz)"><font-awesome-icon icon="fa-solid fa-plus" size="lg" /> Question</button>
                </div>
                <hr>
                <div style="margin-top: 10px;">
                  <button class="btn btn-sm btn-light me-2" @click="openQuizModal(quiz)"><font-awesome-icon icon="fa-solid fa-file-pen" size="lg" /></button>
                  <button class="btn btn-sm btn-danger" @click="openDeleteQuizModal(quiz)"><font-awesome-icon icon="fa-solid fa-trash" size="lg" /></button>
                </div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Quiz Modal (Add/Edit) -->
      <div class="modal fade show" tabindex="-1" style="display:block" v-if="showQuizModal">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="saveQuiz">
              <div class="modal-header">
                <h5 class="modal-title">{{ quizForm.id ? 'Edit Quiz' : 'Add Quiz' }}</h5>
                <button type="button" class="btn-close" @click="closeQuizModal()"></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Quiz Name</label>
                  <input type="text" class="form-control" v-model="quizForm.quiz_name" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Chapter</label>
                  <select class="form-select" v-model="quizForm.chapter_id" required>
                    <option disabled value="">-- Select Chapter --</option>
                    <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                      {{ chapter.name }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label">Date of Quiz</label>
                  <input type="datetime-local" class="form-control" v-model="quizForm.date_of_quiz">
                </div>
                <div class="mb-3">
                  <label class="form-label">Time Duration (HH:MM)</label>
                  <input type="text" class="form-control" v-model="quizForm.time_duration">
                </div>
                <div class="mb-3">
                  <label class="form-label">Remarks</label>
                  <input type="text" class="form-control" v-model="quizForm.remarks">
                </div>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">{{ quizForm.id ? 'Update' : 'Create' }}</button>
                <button type="button" class="btn btn-secondary" @click="closeQuizModal()">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Delete Quiz Modal -->
      <div class="modal fade show" tabindex="-1" style="display:block" v-if="showDeleteQuizModal">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Delete Quiz</h5>
              <button type="button" class="btn-close" @click="showDeleteQuizModal = false"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to delete quiz <strong>{{ quizToDelete.quiz_name }}</strong>?
            </div>
            <div class="modal-footer">
              <button class="btn btn-danger" @click="deleteQuiz">Delete</button>
              <button class="btn btn-secondary" @click="showDeleteQuizModal = false">Cancel</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Show Questions Modal -->
      <div class="modal fade show" tabindex="-1" style="display:block" v-if="showQuestionsModal">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Questions for "{{ currentQuiz.quiz_name }}"</h5>
              <button type="button" class="btn-close" @click="showQuestionsModal = false"></button>
            </div>
            <div class="modal-body">
              <div v-if="questions.length === 0" class="alert alert-info">No questions found.</div>
              <ul class="list-group">
                <li v-for="q in questions" :key="q.id"
                  class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <strong>Q:</strong> {{ q.question_statement }}<br>
                    <span v-for="i in 4" :key="i">
                      <span :class="{ 'fw-bold text-success': q.correct_option === i }">
                        {{ 'Option ' + i + ': ' + q['option' + i] }}
                      </span>
                      <span v-if="i < 4"> | </span>
                    </span>
                  </div>
                  <button class="btn btn-sm btn-danger" @click="deleteQuestion(q)">Delete</button>
                </li>
              </ul>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showQuestionsModal = false">Close</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Question Modal -->
      <div class="modal fade show" tabindex="-1" style="display:block" v-if="showAddQuestionModal">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="saveQuestion">
              <div class="modal-header">
                <h5 class="modal-title">Add Question to "{{ currentQuiz.quiz_name }}"</h5>
                <button type="button" class="btn-close" @click="showAddQuestionModal = false"></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Question Statement</label>
                  <input type="text" class="form-control" v-model="questionForm.question_statement" required>
                </div>
                <div class="mb-3" v-for="i in 4" :key="i">
                  <label class="form-label">Option {{ i }}</label>
                  <input type="text" class="form-control" v-model="questionForm['option' + i]" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Correct Option</label>
                  <select class="form-select" v-model.number="questionForm.correct_option" required>
                    <option v-for="i in 4" :key="i" :value="i">Option {{ i }}</option>
                  </select>
                </div>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Add Question</button>
                <button type="button" class="btn btn-secondary"
                  @click="showAddQuestionModal = false">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>

    </div>
    
  </div>

</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      quizzes: [],
      loading: true,
      chapters: [],
      searchQuery: '',
      showQuizModal: false,
      showDeleteQuizModal: false,
      showQuestionsModal: false,
      showAddQuestionModal: false,
      quizForm: {
        id: null,
        quiz_name: '',
        chapter_id: '',
        date_of_quiz: '',
        time_duration: '',
        remarks: '',
      },
      quizToDelete: {},
      currentQuiz: {},
      questions: [],
      questionForm: {
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: 1,
      },
    };
  },
  computed: {
    filteredQuiz() {
      return this.quizzes.filter(quiz => quiz.quiz_name.toLowerCase().includes(this.searchQuery.toLowerCase()))
    }
  },
  mounted() {
    this.loadChapters();
    this.loadAllQuizzes();
  },
  created() {
    this.loadAllQuizzes();
    
  },
  methods: {
   
    async loadChapters() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/chapter', { params: { subject_id: 1 } }); // You may want to load all chapters for all subjects
        this.chapters = res.data;
      } catch (e) {
        this.chapters = [];
      }
    },
    async loadAllQuizzes() {
  try {
  
    const { data: subjects } = await axios.get('http://127.0.0.1:5000/api/subject');

    // Fetch all chapters in parallel
    const chapterPromises = subjects.map(subj =>
      axios.get('http://127.0.0.1:5000/api/chapter', {
        params: { subject_id: subj.id }
      }).then(res => res.data).catch(() => [])
    );
    const chapterResults = await Promise.all(chapterPromises);
    const allChapters = chapterResults.flat();
    this.chapters = allChapters;

    // Fetch all quizzes in parallel
    const quizPromises = allChapters.map(chapter =>
      axios.get('http://127.0.0.1:5000/api/quiz', {
        params: { chapter_id: chapter.id }
      }).then(res => res.data.map(q => ({
        ...q,
        chapter_id: chapter.id,
        chapter_name: chapter.name
      }))).catch(() => [])
    );
    const quizResults = await Promise.all(quizPromises);
    this.quizzes = quizResults.flat();

  } catch (err) {
    console.error("Error loading all quizzes:", err);
    this.quizzes = [];
  } finally {
    this.loading = false;
  }
},

    openQuizModal(quiz = null) {
      if (quiz) {
        this.quizForm = {
          id: quiz.id,
          quiz_name: quiz.quiz_name,
          chapter_id: quiz.chapter_id,
          date_of_quiz: quiz.date_of_quiz ? quiz.date_of_quiz.replace(' ', 'T') : '',
          time_duration: quiz.time_duration,
          remarks: quiz.remarks,
        };
      } else {
        this.quizForm = {
          id: null,
          quiz_name: '',
          chapter_id: '',
          date_of_quiz: '',
          time_duration: '',
          remarks: '',
        };
      }
      this.showQuizModal = true;
    },
    closeQuizModal() {
      this.showQuizModal = false;
    },
    async saveQuiz() {
      try {
        const payload = {
          chapter_id: this.quizForm.chapter_id,
          quiz_name: this.quizForm.quiz_name,
          date_of_quiz: this.quizForm.date_of_quiz
            ? new Date(this.quizForm.date_of_quiz).toISOString().slice(0, 19).replace('T', ' ')
            : null,
          time_duration: this.quizForm.time_duration,
          remarks: this.quizForm.remarks,
        };
        if (this.quizForm.id) {
          payload.id = this.quizForm.id;
          await axios.put('http://127.0.0.1:5000/api/quiz', payload);
        } else {
          await axios.post('http://127.0.0.1:5000/api/quiz', payload);
        }
        this.showQuizModal = false;
        this.loadAllQuizzes();
      } catch (e) {
        alert('Error saving quiz');
      }
    },
    openDeleteQuizModal(quiz) {
      this.quizToDelete = quiz;
      this.showDeleteQuizModal = true;
    },
    async deleteQuiz() {
      try {
        await axios.delete('http://127.0.0.1:5000/api/quiz', { data: { id: this.quizToDelete.id } });
        this.showDeleteQuizModal = false;
        this.loadAllQuizzes();
      } catch (e) {
        alert('Error deleting quiz');
      }
    },
    openQuestionModal(quiz) {
      this.currentQuiz = quiz;
      this.loadQuestions(quiz.id);
      this.showQuestionsModal = true;
    },
    async loadQuestions(quiz_id) {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/question', { params: { quiz_id } });
        this.questions = res.data;
      } catch (e) {
        this.questions = [];
      }
    },
    async deleteQuestion(question) {
      if (!confirm('Delete this question?')) return;
      try {
        await axios.delete('http://127.0.0.1:5000/api/question', { data: { id: question.id } });
        this.loadQuestions(this.currentQuiz.id);
        this.loadAllQuizzes();
      } catch (e) {
        alert('Error deleting question');
      }
    },
    openAddQuestionModal(quiz) {
      this.currentQuiz = quiz;
      this.questionForm = {
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: 1,
      };
      this.showAddQuestionModal = true;
    },
    async saveQuestion() {
      try {
        const payload = {
          quiz_id: this.currentQuiz.id,
          ...this.questionForm,
        };
        await axios.post('http://127.0.0.1:5000/api/question', payload);
        this.showAddQuestionModal = false;
        this.loadQuestions(this.currentQuiz.id);
        this.loadAllQuizzes();
      } catch (e) {
        alert('Error adding question');
      }
    },
  },
};


</script>

<style scoped>
.sidebar {
  min-height: 100vh;
  border-right: 1px solid #dee2e6;
}

.nav-link.active {
  font-weight: bold;
  color: #0d6efd !important;
}

.card {
  min-height: 350px;
}
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
.modal {
  display: block;
  background: rgba(0, 0, 0, 0.3);
}

.modal-dialog {
  margin-top: 10vh;

}
.bolton {
  background: linear-gradient(90deg, #c4bbf7 );

}
</style>