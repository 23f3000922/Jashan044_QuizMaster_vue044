<template>
    <div class="container-fluid min-vh-100">
        <br>
        <h1>Quizzes</h1>
        <div class="mx-auto p-2" style="width: 400px;">
            <form class="d-flex align-items-center" role="search">
                <input class="form-control me-2" v-model="searchQuery" type="search" placeholder="Search"
                    aria-label="Search" /><font-awesome-icon icon="fa-solid fa-magnifying-glass" />
            </form>
        </div>
        <hr>
        <div v-if="loading" class="text-center my-5">
            <div class="spinner-border text-primary" role="status"></div>
            <span class="visually-hidden">Loading ...</span>
        </div>
        <div v-else class="mt-4">
            <h2>Available Quizzes</h2>
            <div v-if="filteredAvailableQuizzes.length === 0" class="alert alert-info">No available quizzes.</div>
            <div style="height:auto; overflow-y:auto;">
                <transition-group name="fade" tag="div" class="row">
                    <div class="col-md-6 col-lg-4 mb-4" v-for="quiz in filteredAvailableQuizzes" :key="quiz.id">
                        <div class="card h-auto">
                            <div class="card-body">
                                <h5 class="card-title">{{ quiz.quiz_name }}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">
                                    Subject: {{ quiz.subject_name }}<br>
                                    Chapter: {{ quiz.chapter_name }}
                                </h6>
                                <p class="card-text">
                                    <strong>Content:</strong> {{ quiz.remarks || 'None' }}
                                </p>
                                <div class="d-flex justify-content-between">
                                    <button class="btn btn-outline-dark btn-sm" @click="showDetails(quiz)">
                                        <font-awesome-icon :icon="['fas', 'play']" size="lg" /> Start 
                                    </button>
                                    <button class="btn btn-outline-secondary btn-sm" @click="showDetails(quiz)">
                                        <font-awesome-icon :icon="['fas', 'info']" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition-group>
            </div>
            <!-- Quiz Details Modal -->
            <div class="modal fade show" tabindex="-1" style="display: block;" v-if="showModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{{ selectedQuiz.quiz_name }} Details</h5>
                            <button type="button" class="btn-close" @click="showModal = false"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>Subject:</strong> {{ selectedQuiz.subject_name }}</p>
                            <p><strong>Chapter:</strong> {{ selectedQuiz.chapter_name }}</p>
                            <p><strong>Date:</strong> {{ selectedQuiz.date_of_quiz && (new Date(selectedQuiz.date_of_quiz)).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) }}</p>
                            <p><strong>Duration:</strong>  {{ selectedQuiz.time_duration.split(':')[0] }} hour : {{ selectedQuiz.time_duration.split(':')[1] }} minutes </p>
                            <p><strong>Questions:</strong> {{ selectedQuiz.number_of_questions }}</p>
                            <p><strong>Remarks:</strong> {{ selectedQuiz.remarks }}</p>
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-primary " @click="startQuiz(selectedQuiz.id)">
                                    <font-awesome-icon :icon="['fas', 'play']" size="lg" /> Start Quiz
                            </button>
                            <button type="button" class="btn btn-secondary" @click="showModal = false">Close</button>
                        </div>
                    </div>
                </div>
            </div>
            <!-- End Modal -->
        </div>
        <div class="mt-4">
            <h2>Completed Quizzes</h2>
            <div v-if="filteredCompletedQuizzes.length === 0" class="alert alert-warning">No completed quizzes.</div>
            <div style="height:auto; overflow-y:auto;">
                <transition-group name="fade" tag="div" class="row">
                    <div class="col-md-6 col-lg-4 mb-4" v-for="quiz in filteredCompletedQuizzes" :key="quiz.id">
                        <div class="card h-100 bg-light-subtle border-success">
                            <div class="card-body">
                                <h5 class="card-title">{{ quiz.quiz_name }}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">
                                    Subject: {{ quiz.subject_name }}<br>
                                    Chapter: {{ quiz.chapter_name }}
                                </h6>
                                <p class="card-text">
                                    <strong>Content:</strong> {{ quiz.remarks || 'None' }}
                                </p>
                                
                            </div>
                        </div>
                    </div>
                </transition-group>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            loading: true,
            availableQuizzes: [],
            completedQuizzes: [],
            showModal: false,
            selectedQuiz: {},
            searchQuery: '',
            subjects: [],
            userId: null,
        };
    },
    computed: {
        filteredAvailableQuizzes() {
            if (!this.searchQuery) return this.availableQuizzes;
            return this.availableQuizzes.filter(quiz =>
                quiz.quiz_name && quiz.quiz_name.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
        filteredCompletedQuizzes() {
            if (!this.searchQuery) return this.completedQuizzes;
            return this.completedQuizzes.filter(quiz =>
                quiz.quiz_name && quiz.quiz_name.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        }
    },
    created() {
        this.fetchQuizzes();
    },
    methods: {
        async fetchQuizzes() {
            this.loading = true;
            try {
                let user = sessionStorage.getItem('user')
                    ? JSON.parse(sessionStorage.getItem('user'))
                    : localStorage.getItem('user')
                        ? JSON.parse(localStorage.getItem('user'))
                        : null;
                var userId = user ? user.id : null;
                if (!userId) {
                    alert('User not logged in!');
                    this.loading = false;
                    return;
                }
                this.userId = userId;
                const response = await axios.get(`http://127.0.0.1:5000/api/quizzes?user_id=${user.id}`);
                this.availableQuizzes = response.data.available_quizzes || [];
                this.completedQuizzes = response.data.completed_quizzes || [];
            } catch (error) {
                console.error('Error fetching quizzes:', error);
                this.availableQuizzes = [];
                this.completedQuizzes = [];
            } finally {
                this.loading = false;
            }
        },
        startQuiz(quizId) {
            this.$router.push({ name: 'QuizAttempt', params: { quizId } });
        },
        showScore(userId) {
            const id = userId || this.userId;
            if (!id) {
                alert('User ID not found!');
                return;
            }
            this.$router.push({ name: 'UserScore', params: { userId: id } });
        },
        showDetails(quiz) {
            this.selectedQuiz = quiz;
            this.showModal = true;
        },
    },
};
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}
</style>