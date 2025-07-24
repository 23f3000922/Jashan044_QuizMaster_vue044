<template>
  <div class="container-fluid">
    <br>
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else class="container mt-4">
      <h2>User's List</h2>
      <div class="table-responsive" style="max-width: 900px; margin: 0 auto; margin-top: 24px;">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Email</th>
              <th>Qualification</th>
              <th>Date of Birth</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, idx) in users" :key="user.id">
              <td>{{ idx + 1 }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.qualification }}</td>
              <td>{{ user.dob }}</td>
              <td>{{ user.role }}</td>
              <td>
                <button class="btn btn-dark btn-sm" @click="showScores(user)">
                  <font-awesome-icon icon="fa-solid fa-eye"/> Score Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mb-4">
        <button class="btn btn-primary btn-sm"
                :disabled="csvExporting"
                @click="csvExport">
          <span v-if="csvExporting" class="spinner-border spinner-border-sm me-1"></span>
          <font-awesome-icon icon="fa-solid fa-download"/> Download User Details
        </button>
      </div>

      <!-- Modal for Score Details -->
      <div v-if="showScoreModal">
        <div class="modal-backdrop fade show" @click="closeModal"></div>
        <div class="modal fade show d-block" tabindex="-1" style="background:rgba(0,0,0,0.1)">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">
                  Score Details for {{ selectedUser ? selectedUser.username : '' }}
                </h5>
                <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div v-if="loadingScores" class="text-center">
                  <div class="spinner-border" role="status"></div>
                </div>
                <div v-else>
                  <div v-if="userScores.length === 0" class="alert alert-info">
                    No quiz attempts found for this user.
                  </div>
                  <table v-else class="table table-striped">
                    <thead>
                      <tr>
                        <th>Quiz Name</th>
                        <th>Subject</th>
                        <th>Chapter</th>
                        <th>Date of Quiz</th>
                        <th>Score</th>
                        <th>Reattempted</th>
                        <th>Attempted On</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="score in userScores" :key="score.quiz_id">
                        <td>{{ score.quiz_name }}</td>
                        <td>{{ score.subject_name }}</td>
                        <td>{{ score.chapter_name }}</td>
                        <td>{{ score.date_of_quiz }}</td>
                        <td>{{ score.score }}</td>
                        <td>
                          <span v-if="score.reattempted"
                                class="badge bg-warning text-dark">Yes</span>
                          <span v-else class="badge bg-success">No</span>
                        </td>
                        <td>{{ score.attempted_on }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Modal End -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDetails',
  data() {
    return {
      users: [],
      selectedUser: null,
      loading: true,
      userScores: [],
      loadingScores: false,
      showScoreModal: false,
      csvExporting: false
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('http://127.0.0.1:5000/api/users')
        .then(res => {
          this.users = res.data.filter(user => user.role !== 'admin');
          this.loading = false;
        })
        .catch(() => {
          this.users = [];
          this.loading = false;
        });
    },
    showScores(user) {
      this.selectedUser = user;
      this.userScores = [];
      this.loadingScores = true;
      this.showScoreModal = true;
      axios.get(`http://127.0.0.1:5000/api/user-scores?user_id=${user.id}`)
        .then(res => {
          this.userScores = res.data;
        })
        .catch(() => {
          this.userScores = [];
        })
        .finally(() => {
          this.loadingScores = false;
        });
    },
    closeModal() {
      this.showScoreModal = false;
      this.selectedUser = null;
      this.userScores = [];
      this.loadingScores = false;
    },
    csvExport() {
      // Async CSV Export Process
      this.csvExporting = true;
      fetch('http://127.0.0.1:5000/api/export_users_csv', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
          if (data.task_id) {
            this.pollCsvResult(data.task_id, 0);
          } else {
            this.csvExporting = false;
            alert('Could not start the export.');
          }
        })
        .catch(err => {
          this.csvExporting = false;
          alert('Export error: ' + err);
        });
    },
    pollCsvResult(taskId, attempts) {
      // Poll for CSV readiness; 1s interval, max 30 tries
      const pollUrl = `http://127.0.0.1:5000/api/csv_result/${taskId}`;
      fetch(pollUrl)
        .then(async res => {
          // CSV file will have content-type 'text/csv'
          if (res.headers.get('content-type') && res.headers.get('content-type').includes('text/csv')) {
            // File is ready! Download:
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            // Try to extract filename from response header, falls back to a default:
            const disposition = res.headers.get('Content-Disposition');
            let filename = 'users_export.csv';
            if (disposition && disposition.indexOf('filename=') !== -1) {
              filename = disposition.split('filename=')[1].replace(/["']/g, '');
            }
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            link.remove();
            URL.revokeObjectURL(url);
            this.csvExporting = false;
          } else {
            // Still a JSON (not ready yet)
            const data = await res.json();
            if (data.status === 'Processing') {
              if (attempts < 30) {
                setTimeout(() => this.pollCsvResult(taskId, attempts + 1), 1000);
              } else {
                this.csvExporting = false;
                alert('Export timed out after 30 seconds.');
              }
            } else {
              this.csvExporting = false;
              alert('Export failed: ' + (data.error || 'Unknown error'));
            }
          }
        })
        .catch(e => {
          this.csvExporting = false;
          alert('Export error: ' + e);
        });
    }
  }
}
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}
.modal.fade.show.d-block {
  z-index: 1050;
}
</style>