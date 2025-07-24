<template>
  <div class="container-fluid " >

    
      <br>
        <h1>Chapter Management</h1>
         
        
        <br>
        <div class="mx-auto p-2" style="width: 400px;">
          <form class="d-flex align-items-center" role="search">
            <input class="form-control me-2" v-model="searchQuery" type="search" placeholder="Search"
              aria-label="Search" /><font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </form>
        </div>
        <hr>
        <h3>Chapters</h3>
         <div v-if="loading" class="text-center my-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        
        <div v-else class="container mt-4 "  style="height: 70vh; overflow-y: auto;">
          <div class=" row">
            <transition-group name="fade" tag="div" class="row">
            <div v-for="subject in filteredSubjects" :key="subject.id" class="col-md-3 mb-3">
              <div class="card h-auto">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <span class="fw-bold">{{ subject.name }}</span>
                  <button class="btn btn-sm btn-dark" @click="openAddChapterModal(subject)">
                    <font-awesome-icon icon="fa-solid fa-square-plus" /> Chapter
                  </button>
                </div>
                <ul class="list-group list-group-flush">
                  <li v-for="chapter in subject.chapters" :key="chapter.id"
                    class="list-group-item d-flex justify-content-between align-items-center">
                    <div style="margin: auto;">
                      <span class="fw-semibold ">{{ chapter.name }}</span>
                      <div class="text-muted small">{{ chapter.description }}</div>

                      <button class="btn btn-sm btn-outline-secondary me-2"
                        @click="openEditChapterModal(subject, chapter)">
                        <font-awesome-icon :icon="['fas', 'pen-to-square']" size="xl"  />
                      </button>
                      <button class="btn btn-sm btn-outline-danger" @click="deleteChapter(chapter.id, subject)">
                        <font-awesome-icon :icon="['fas', 'trash']"  size="xl" />
                      </button>
                        


                    </div>


                  </li>
                  <li v-if="!subject.chapters.length" class="list-group-item text-muted">
                    No chapters yet.
                  </li>
                </ul>
              </div>
            </div>
            </transition-group>
          </div>

          
          <div v-if="showChapterModal">
            <div class="modal fade show d-block" tabindex="-1">
              <div class="modal-dialog">
                <div class="modal-content">
                  <form @submit.prevent="submitChapterForm">
                    <div class="modal-header">
                      <h5 class="modal-title">{{ isEditMode ? 'Edit Chapter' : 'Add Chapter' }}</h5>
                      <button type="button" class="btn-close" @click="closeChapterModal"></button>
                    </div>
                    <div class="modal-body">
                      <div class="mb-3">
                        <label class="form-label">Chapter Name</label>
                        <input type="text" class="form-control" v-model="chapterForm.name" required />
                      </div>
                      <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea class="form-control" v-model="chapterForm.description" rows="2"></textarea>
                      </div>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="closeChapterModal">
                        Cancel
                      </button>
                      <button type="submit" class="btn btn-primary">
                        {{ isEditMode ? 'Update' : 'Add' }}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
            <div class="modal-backdrop fade show"></div>
          </div>
        </div>

  </div>



</template>
<script>

export default {
  name: "AdminDashboard",
  data() {
    return {
      subjects: [],
      showChapterModal: false,
      loading:true,
      isEditMode: false,
      searchQuery: '',
      chapterForm: {
        id: null,
        name: "",
        description: "",
        subject_id: null,
      },
      currentSubject: null,
    };
  },
  computed: {
    filteredSubjects() {
      const query = this.searchQuery.toLowerCase();
      return this.subjects.filter(subject => {
        // Check subject name
        if (subject.name.toLowerCase().includes(query)) {
          return true;
        }
        // Check chapters (if any)
        if (subject.chapters && Array.isArray(subject.chapters)) {
          return subject.chapters.some(
            chapter => chapter.name && chapter.name.toLowerCase().includes(query)
          );
        }
        return false;
      });
    }
  },
  created() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      
      const res = await fetch("http://127.0.0.1:5000/api/subject");

      const subjects = await res.json();

      
      for (const subject of subjects) {
        const chapRes = await fetch(` http://127.0.0.1:5000/api/chapter?subject_id=${subject.id}`);
        if (chapRes.ok) {
          subject.chapters = await chapRes.json();
        } else {
          subject.chapters = [];
        }
      }
      this.loading = false;
      this.subjects = subjects;
    },

    openAddChapterModal(subject) {
      this.isEditMode = false;
      this.chapterForm = {
        id: null,
        name: "",
        description: "",
        subject_id: subject.id,
      };
      this.currentSubject = subject;
      this.showChapterModal = true;
    },
    openEditChapterModal(subject, chapter) {
      this.isEditMode = true;
      this.chapterForm = {
        id: chapter.id,
        name: chapter.name,
        description: chapter.description,
        subject_id: subject.id,
      };
      this.currentSubject = subject;
      this.showChapterModal = true;
    },
    closeChapterModal() {
      this.showChapterModal = false;
      this.chapterForm = {
        id: null,
        name: "",
        description: "",
        subject_id: null,
      };
      this.currentSubject = null;
    },
    async submitChapterForm() {
      try {
        if (this.isEditMode) {
          
          const res = await fetch("http://127.0.0.1:5000/api/chapter", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              id: this.chapterForm.id,
              name: this.chapterForm.name,
              description: this.chapterForm.description,
            }),
          });
          if (!res.ok) {
            const data = await res.json();
            alert(data.message || "Failed to update chapter.");
            return;
          }
        } else {
          
          const res = await fetch(" http://127.0.0.1:5000/api/chapter", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              subject_id: this.chapterForm.subject_id,
              name: this.chapterForm.name,
              description: this.chapterForm.description,
            }),
          });
          if (!res.ok) {
            const data = await res.json();
            alert(data.message || "Failed to add chapter.");
            return;
          }
        }
        await this.fetchSubjects();
        this.closeChapterModal();
      } catch (err) {
        alert("Failed to save chapter.");
      }
    },
    async deleteChapter(chapterId) {
      if (!confirm("Are you sure you want to delete this chapter?")) return;
      try {
        
        const res = await fetch(" http://127.0.0.1:5000/api/chapter", {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: chapterId }),
        });
        if (!res.ok) {
          const data = await res.json();
          alert(data.message || "Failed to delete chapter.");
          return;
        }
        await this.fetchSubjects();
      } catch (err) {
        alert("Failed to delete chapter.");
      }
    },
  },
  mounted() {
    this.fetchSubjects();
  },
};

</script>


<style scoped>


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
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

</style>
