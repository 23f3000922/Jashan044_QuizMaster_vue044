<template>
  <div class="container-fluid">
    <br>

        <div class="subject-management">
          <h1>Subject Management</h1>
          <hr>
          <h3>Subjects</h3>
          <button type="submit" class="btn btn-secondary" @click="openAddSubjectModal"> <font-awesome-icon icon="fa-solid fa-square-plus" /> Subject</button>
           <div v-if="loading" class="text-center my-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-else  style="height: 70vh; overflow-y: auto;">
          <div style="max-width: 900px; margin: 0 auto; margin-top: 24px;" v-if="subjects.length > 0" class="table-responsive">
            <table class="table table-bordered table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Subject Name</th>
                  <th>Subject Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="subject in subjects" :key="subject.id">
                  <td>{{ subject.id }}</td>
                  <td>
                    <input type="text" class="form-control" v-model="subject.name" :disabled="subject.id !== editSubjectId" />
                  </td>
                  <td>
                    <input type="text" class="form-control" v-model="subject.description" :disabled="subject.id !== editSubjectId" />
                  </td>
                  <td>
                    <button class="btn btn-outline-secondary btn-sm me-2" v-if="subject.id !== editSubjectId" @click="startEditing(subject)"><font-awesome-icon :icon="['fas', 'pen-to-square']" size="xl"  /></button>
                    <button class="btn btn-outline-success btn-sm me-2" v-else @click="saveEditing(subject)"><font-awesome-icon icon="fa-solid fa-floppy-disk" size="xl"/></button>
                    <button class="btn btn-outline-danger btn-sm" @click="deleteSubject(subject)"> <font-awesome-icon :icon="['fas', 'trash']"  size="xl" /></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          </div>
          <br>
          <div >
            <div>
              <div v-if="showSubjectModal">
                <!-- Modal Backdrop -->
                <div class="modal-backdrop fade show" @click="closeAddSubjectModal"></div>
                <!-- Modal Dialog -->
                <div class="modal fade show d-block" tabindex="-1" style="background:rgba(0,0,0,0.1)">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title">Add Subject</h5>
                        <button type="button" class="btn-close" @click="closeAddSubjectModal"
                          aria-label="Close"></button>
                      </div>
                      <form @submit.prevent="addSubject">
                        <div class="modal-body">
                          <input type="text" id="subject-name" v-model="newSubjectName" class="form-control mb-2"
                            required placeholder="Subject Name" />
                          <input type="text" id="subject-description" v-model="newSubjectDescription"
                            class="form-control mb-2" required placeholder="Subject Description" />
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" @click="closeAddSubjectModal">Close</button>
                          <button type="submit" class="btn btn-primary">Add Subject</button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
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
      newSubjectName: '',
      loading:true,
      newSubjectDescription: '',
      subjects: [],
      editSubjectId: null,
      showSubjectModal: false,
    };
  },

  mounted() {
    this.loadSubjects();
  },

  methods: {
    async loadSubjects() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/subject');
        this.subjects = response.data;
        this.loading = false;
      } catch (error) {
        console.error('Error loading subjects:', error);
      }
    },

    async addSubject() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/subject', {
          name: this.newSubjectName,
          description: this.newSubjectDescription,
        });
        console.log(response.data);
        this.newSubjectName = '';
        this.newSubjectDescription = '';
        this.loadSubjects(); 
        this.closeAddSubjectModal(); 
      } catch (error) {
        console.error('Error adding subject:', error);
      }
    },
    openAddSubjectModal() {
      this.showSubjectModal = true;
    },
    closeAddSubjectModal() {
      this.showSubjectModal = false;
    },

    async deleteSubject(subject) {
      try {
        const response = await axios.delete('http://127.0.0.1:5000/api/subject', { data: { id: subject.id } });
        console.log(response.data);
        this.loadSubjects(); 
      } catch (error) {
        console.error('Error deleting subject:', error);
      }
    },

    async saveEditing(subject) {
      try {
        const response = await axios.put('http://127.0.0.1:5000/api/subject', {
          id: subject.id,
          name: subject.name,
          description: subject.description,
        });
        console.log(response.data);
        this.loadSubjects(); 
        this.editSubjectId = null; 
      } catch (error) {
        console.error('Error saving editing subject:', error);
      }
    },

    startEditing(subject) {
      this.editSubjectId = subject.id;
    },
  },
};
</script>

<style>

</style>