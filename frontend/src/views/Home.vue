<template>
    <div>
        <!-- Carousel Section -->
        <div id="carouselExampleInterval" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item active" data-bs-interval="2000">
                    <img src="/images/back1.png" class="d-block w-100 " alt="...">
                    <div class="carousel-caption d-flex flex-column align-items-center justify-content-center h-auto">
                        <h5>Welcome to the Quiz Master</h5>
                        <p>Test your knowledge and challenge yourself with our quizzes!</p>
                        <button class="btn btn-secondary btn-lg mt-3" @click="goToQuiz">Get Started</button>
                        <p class="mt-2 text-light">Click "Get Started" to attempt your first quiz.</p>
                    </div>
                </div>
                <div class="carousel-item" data-bs-interval="2000">
                    <img src="/images/backround3.jpg" class="d-block w-100" alt="...">
                    <div class="carousel-caption d-none d-md-block">
                        <h5>Expand Your Knowledge</h5>
                        <p>Explore a variety of topics and improve your skills.</p>
                        <button class="btn btn-secondary mt-3" @click="goToQuiz">Get Started</button>
                    </div>
                </div>
                <div class="carousel-item" data-bs-interval="2000">
                    <img src="/images/backround.jpg" class="d-block w-100" alt="...">
                    <div class="carousel-caption d-none d-md-block">
                        <h5>Compete and Learn</h5>
                        <p>Challenge friends and see how you rank!</p>
                        <button class="btn btn-secondary mt-3" @click="goToQuiz">Get Started</button>
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleInterval"
                data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleInterval"
                data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>

        <!-- About Us Section -->
        <section class="about-us-section mt-5">
            <div class="container">
                <h2>About Us</h2>
                <p>
                    Welcome to our Quiz Master! We are passionate about learning and believe that quizzes are a fun and effective way to test and expand your knowledge. 
                    Our platform offers a wide range of quizzes on various Chapters, designed to challenge and engage users of all ages. 
                    Whether you're preparing for exams, looking to learn something new, or just want to have fun, our quizzes are here to help you grow.
                </p>
                <p>
                    Join us and start your journey of learning and self-improvement today!
                </p>
                <p>
                    Contact us at <a href="mailto:infoquizmaster@gmail.com">infoquizmaster@gmail.com</a> if you have any questions or need further assistance. We're here to help!
                </p>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'HomeNavbar',
    methods: {
        goToQuiz() {
            
            this.$router.push('/login');
        }
    }
}
</script>

<style scoped>
.carousel-caption {
    background: rgba(0, 0, 0, 0.5);
    border-radius: 1rem;
    padding: 2rem;
}

.carousel-caption h5,
.carousel-caption p {
    color: #fff;
}

.about-us-section {
    background: #f8f9fa;
    padding: 2rem 0;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.about-us-section h2 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #343a40;
}

.about-us-section p {
    font-size: 1.1rem;
    color: #555;
}

.btn-primary {
    padding: 0.5rem 1.5rem;
    font-size: 3.1rem;
}

.mt-5 {
    margin-top: 3rem !important;
}
</style>