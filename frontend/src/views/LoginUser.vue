<template>
    <img src="/images/back2.png" class="background-image" alt="...">
    <div class="background-wrapper">
      <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="loginUser">
          <div class="form-group">
            <input type="text" placeholder="Username" id="username" v-model="username" required />
          </div>
          <div class="form-group">
            
            <input type="password" id="password" placeholder="Password" v-model="password" required />
          </div>
          <button class="btn btn-secondary" type="submit">Login</button>
        </form>
        <hr>
        <div>
          <p class="text-body-emphasis" >Don't have an account?<a class="link-primary" href="/signup">Signup</a>
          </p> 
          
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  
  .background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: auto;
    object-fit:cover;
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
  
  .login-container {
    background-color: #B197FC; 
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1; 
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .error-message {
    color: red;
    margin-top: 10px;
  }
  </style>

<script>

import axios from 'axios';

export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: '', 
        };
    },
    methods: {
        async loginUser() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/api/login', {
                    username: this.username,
                    password: this.password,
                });
                const {access_token, user } = response.data
                this.$store.dispatch('login',{token:access_token, user});


                localStorage.setItem('token', access_token);
                localStorage.setItem('user', JSON.stringify(user));
                
                if (user.role === 'admin') {
                    this.$router.push('/admin-dashboard'); 
                } else {
                    this.$router.push('/user-dashboard');
                 } 
            } catch (error) {
                if  (error.response && error.response.status === 401) {
                    this.errorMessage = 'Invalid username or password';
                } else {
                    this.errorMessage = 'An error occurred, please try again later';
                }
               }
            }
        }



}


</script>

<style scoped>
.login-container {
    width: 300px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid white;
    border-radius: 5px ;
    
    background-color:rgb(183, 201, 216);
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




</style>