<template>
  <img src="/images/back2.png" class="background-image" alt="...">
  <div class="background-wrapper">
      <div class="signup-container">
        <h2>Signup</h2>
        <form @submit.prevent="signupUser">
          <div class="form-group">

            <input type="email" id="email" placeholder="Email" v-model="email" required />
          </div>
          <div class="form-group">
            <input type="text" id="username" placeholder="Username" v-model="username" required />
          </div>
          <div class="form-group">
            <input type="password" id="password" placeholder="Password" v-model="password" required />
          </div>
          <div class="form-group">
            <input type="text" id="Qualifications" placeholder="qualifications" v-model="qualifications" required />
          </div>
          <div class="form-group">
            <label for="dob">D.O.B</label>
            <input type="date" id="dob" placeholder="Date of Birth" v-model="dob" required />
          </div>
          <button type="submit">Signup</button>
        </form>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      qualifications: '',
      dob: '',
      errorMessage: '',
    };
  },
  methods: {
    async signupUser() {
      console.log('Signup button clicked');
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/signup', {
          username: this.username,
          password: this.password,
          email: this.email,
          qualifications: this.qualifications,
          dob: this.dob,
        });
        console.log(response.data); 
        this.$router.push('/login');
      } catch (error) {
        if (error.response) {
          console.error('Error response:', error.response.data);
          if (error.response.status === 400) {
            this.errorMessage = 'Signup failed, please check your details';
          } else {
            this.errorMessage = 'An error occurred, please try again later';
          }
        } else {
          console.error('Error:', error.message);
          this.errorMessage = 'An error occurred, please try again later';
        }
      }
    },
  },
};
</script>

<style scoped>
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: auto;
  object-fit: cover;
  z-index: -1;
  
}

.background-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  
  display: flex;
  justify-content: center;
  align-items: center;
}


.error-message {
  color: red;
  margin-top: 10px;
}

.signup-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid white;
  border-radius: 5px;
  background-color: rgb(183, 201, 216);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  background-color: #508ddd;
  color: white;
  padding: 14px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 60%;
  font-size: 16px;
  margin-top: 10px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>