<template>
  <div id="app">
    
    <nav class="navbar navbar-expand-lg " > 
      <div class="container-fluid" >
        <a class="navbar-brand" href="/">Quiz Master <font-awesome-icon icon="fa-solid fa-graduation-cap" bounce style="color: #B197FC;" /></a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <template v-if="isAuthenticated">
              <template v-if="userRole == 'admin'">
                <li class="nav-item">
                  <router-link class="nav-link" aria-current="page" to="/admin-dashboard"><font-awesome-icon icon="fa-solid fa-house" size='l' /></router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/admin-summary">Summary <font-awesome-icon icon="fa-solid fa-chart-simple" size='l' /></router-link>
                </li>
              </template>
              <template v-if="userRole == 'user'">
                <li class="nav-item">
                  <router-link class="nav-link" aria-current="page" to="/user-dashboard"><font-awesome-icon :icon="['fas', 'house-user']" size='l' /></router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link" to="/user-summary">Summary <font-awesome-icon icon="fa-solid fa-chart-simple" size='l' /></router-link>
                </li>
              </template>
              <li class="nav-item">
                <button class="btn btn-link nav-link" @click="logout">Logout</button>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <a class="nav-link" href="https://mail.google.com/mail/?view=cm&fs=1&to=jashantiwari044@gmail.com" target="_blank" style="font-size: medium;" >
                  <font-awesome-icon icon="fa-solid fa-envelope" size="xl" style="color: #B197FC;" />
                  Contact
                </a>
              </li>
              <li class="nav-item">
                <router-link to="/login" class="btn btn-secondary">Get Started</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Sidebar for admin -->
    <div class="container-fluid g-0">
      <div class="row g-0">
        <template v-if="isAuthenticated && userRole === 'admin'">
          <nav class="col-md-2 d-none d-md-block sidebar vh-auto">
            <div class="position-sticky pt-3 ">
              <ul class="nav flex-column rounded-3 p-3 text-primary-emphasis bg-light rounded-3 " style="margin-left: 15px; margin-right: 15px;">
                <li class="nav-item">
                  <router-link class="nav-link link-dark icon-link txt-dark icon-link-hover"
                    aria-current="page"
                    to="/subject">
                    <i class="bi bi-book"></i> Subjects
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16" aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link link-dark icon-link icon-link-hover"
                    aria-current="page"
                    to="/admin-dashboard">
                    <i class="bi bi-book"></i> Chapters
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16" aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link link-dark icon-link icon-link-hover"
                    to="/quiz-management">
                    <i class="bi bi-question-circle"></i> Quiz
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16" aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link link-dark icon-link icon-link-hover"
                    to="/users">
                    <i class="bi bi-people"></i> Users
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16" aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </router-link>
                </li>
                <!-- Add more nav items as needed -->
              </ul>
            </div>
          </nav>
        </template>

        <!-- Sidebar for user -->
        <template v-else-if="isAuthenticated && userRole === 'user'">
          <nav class="col-md-2 d-none d-md-block  sidebar h-auto" >
            <div class="position-sticky pt-3">
              <ul class="nav flex-column rounded-3 p-3 text-primary-emphasis bg-light border rounded-3"  style="margin-left: 15px; margin-right: 15px;" >
                <li class="nav-item">
                  <router-link class="nav-link link-dark icon-link icon-link-hover"
                    aria-current="page"
                    to="/user-dashboard">
                    <i class="bi bi-book"></i> Quiz
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16"
                      aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </router-link>
                </li>
                <li class="nav-item" >
                  <!-- Only render if userId is available -->
                  <button
                    class="nav-link link-dark icon-link icon-link-hover "
                    :class="{'router-link-exact-active': isScoreActive}"
                    @click.prevent="showScore(userId)">
                    <i class="bi bi-book"></i> Score
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16"
                      aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </button>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link link-dark icon-link icon-link-hover"
                    aria-current="page"
                    to="/user-summary">
                    <i class="bi bi-book"></i>Summary
                    <svg xmlns="http://www.w3.org/2000/svg" class="bi" viewBox="0 0 16 16"
                      aria-hidden="true">
                      <path
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
                    </svg>
                  </router-link>
                </li>
                <!-- Add more nav items as needed -->
              </ul>
            </div>
          </nav>
        </template>

        <!-- Main content area -->
        <main :class="isAuthenticated ? 'col-md-10 ms-sm-auto' : 'col-12'" :style="isAuthenticated ? 'background:linear-gradient(to right,#F8F8FF); background-repeat: no-repeat;' : ''">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'App',
  data() {
    return {
      userId: null,
    };
  },
  async created() {
    try {
      // Get user data from storage with proper null checking
      const sessionUser = sessionStorage.getItem('user');
      const localUser = localStorage.getItem('user');
      
      let user = null;
      
      if (sessionUser) {
        user = JSON.parse(sessionUser);
      } else if (localUser) {
        user = JSON.parse(localUser);
      }
      
      // Only set userId if user exists and has an id property
      if (user && user.id) {
        this.userId = user.id;
      } else {
        console.warn('No valid user data found in storage');
        this.userId = null;
      }
    } catch (error) {
      console.error('Error parsing user data from storage:', error);
      this.userId = null;
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole']),
    isScoreActive() {
      return (
        this.$route.name === 'UserScore' &&
        this.$route.params.userId &&
        String(this.$route.params.userId) === String(this.userId)
      );
    },
  },
  methods: {
    ...mapActions(['logout']),
    showScore(userId) {
      if (!userId) {
        console.error('User ID not available');
        // Optionally redirect to login or show a more user-friendly message
        this.$router.push('/login');
        return;
      }
      this.$router.push({ name: 'UserScore', params: { userId } });
    },
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&family=Playwrite+AU+SA:wght@100..400&display=swap');
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.navbar {
  padding: 15px;
  background-color: #E6E6FA;
}

.nav-link {
  font-weight: bold;
  color: #2c3e50;
}

.nav-link.router-link-exact-active,
.sidebar .nav-link.router-link-exact-active,
.sidebar .nav-link.router-link-exact-active:focus,
.sidebar .nav-link.router-link-exact-active:active {
  background-color: #E6E6FA;
  color: #8674eb !important;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
}

/* For Score button active state */
.sidebar .nav-link.router-link-exact-active {
  background-color: #E6E6FA;
  color: #8674eb !important;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
}

/* Sidebar styles */
.sidebar {
  min-height: 100vh;
  background: linear-gradient(to right, #B0C4DE, #c4bbf7);
  background-repeat: no-repeat;
  box-shadow: 2px 0 16px 0 rgba(44, 62, 80, 0.15), 0 1.5px 4px rgba(44, 62, 80, 0.10);
  border-bottom-right-radius: 18px;
  border-right: 1px solid #d1d5db;
  z-index: 10;
}
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500&family=Luckiest+Guy&display=swap');
.nav-item {
  font-family: "Barlow Condensed", sans-serif;
  font-weight: 500;
  font-style: oblique;
  font-size: large;
  font-stretch: expanded;
}

/* Sidebar nav-link enhancements */
.sidebar .nav-link {
  transition: background 0.2s, box-shadow 0.2s;
  border-radius: 8px;
  margin-bottom: 6px;
}

.sidebar .nav-link:hover {
  background-color: #E6E6FA;
  color: #8674eb !important;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
}
h1 {
  font-family: 'Segoe UI', Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: 2.8rem;
  font-weight: 900;
  font-style: normal;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #4B3FE4; /* A modern, bold color */
  background: linear-gradient(90deg, #B197 0%, #332e52 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
  
}
h2{
  font-family: 'Segoe UI', Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: 2.8rem;
  font-weight: 900;
  font-style: normal;
  
  color: #4B3FE4; /* A modern, bold color */
  background: linear-gradient(90deg, #B197 0%, #332e52 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);

}
h3{
  font-family: 'Segoe UI', Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: 2.8rem;
  font-weight: 900;
  font-style: normal;
  
  color: #4B3FE4; /* A modern, bold color */
  background: linear-gradient(90deg, #B197 0%, #332e52 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
}
p {
 font-family:"Oswald", sans-serif;


}
@import url('https://fonts.googleapis.com/css2?family=Michroma&display=swap');
span{
   font-family:"Oswald", sans-serif;
   font-size: large;

  font-weight: 400;
  font-style: normal;
}
h6{
    font-family: 'Segoe UI', Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: 2.8rem;
  font-weight: 900;
  font-style: normal;
  
  color: #4B3FE4; /* A modern, bold color */
  background: linear-gradient(90deg, #B197 0%, #332e52 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);

}
h5{
   font-family: "Michroma", sans-serif;
  font-weight:500;
  font-style: normal;
}
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500&display=swap');
table{
    font-family: "Barlow Condensed", sans-serif;
  font-weight: 500;
  font-style: normal;
  font-size: medium;
  font-stretch: expanded;

}
table th{
  font-weight: 300;
  font-size:larger;
}
.navbar-brand{
  font-size: 1.8rem;
  font-weight: 750;
  font-style: normal;
  
  background: linear-gradient(90deg, #B197 0%, #332e52 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);



}


</style>
