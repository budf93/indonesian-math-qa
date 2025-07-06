<script setup>
import { ref } from 'vue';
import axios from 'axios'; // Corrected import: 'axios' instead of '{ Axios }'

// Importing KaTeX CSS (already correct)
import 'katex/dist/katex.min.css';
// Import VueKatex to make the <vue-katex> component available in the template
import VueKatex from 'vue3-katex'; // Uncommented this line

// Reactive state variables
const question = ref('');
const answer = ref('');
const isLoading = ref(false); // Initialize as false
const error = ref('');

// Function to handle form submission
const handleSubmit = async () => {
    // Prevent submission if the question is empty or just whitespace
    if (!question.value.trim()) {
        error.value = 'Pertanyaan tidak boleh kosong.';
        return;
    }

    isLoading.value = true;
    answer.value = ''; // Clear previous answer
    error.value = '';   // Clear previous error

    try {
        const response = await axios.post('http://localhost:8000/api/ask', {
            question: question.value,
        });

        // Check if the response contains an error from the backend
        if (response.data.error) {
            error.value = response.data.error;
        } else if (response.data.answer) {
            // Assuming the response data contains a raw LaTeX string in the 'answer' field
            answer.value = response.data.answer;
        } else {
            // Fallback if neither answer nor error is present
            answer.value = 'Tidak ada respons yang valid dari model.';
        }
    } catch (err) {
        // Catch network errors or errors from the axios request itself
        error.value = 'Gagal terhubung ke server. Pastikan server backend dan Ollama sudah berjalan.';
        console.error('Frontend Axios Error:', err);
    } finally {
        isLoading.value = false; // Always set loading to false when done
    }
};
</script>

<template>
    <div class="container">
        <h1>LLM Tanya Jawab Matematika</h1>
        <!-- Updated description to reflect the custom model -->
        <p>Ditenagai model kustom dengan penalaran Bahasa Indonesia</p>

        <form @submit.prevent="handleSubmit">
            <textarea
                v-model="question"
                placeholder="Contoh: Sebuah kerucut memiliki jari-jari alas 7 cm dan tinggi 24 cm. Berapakah volume kerucut tersebut?"
                rows="4"
                :disabled="isLoading"
            ></textarea>
            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Sedang memproses...' : 'Tanya' }}
            </button>
        </form>

        <div v-if="error" class="error-box">
            {{ error }}
        </div>

        <!-- Display answer using VueKatex if available and not loading -->
        <div v-if="answer && !isLoading" class="answer-box">
            <h2>Jawaban:</h2>
            <!-- VueKatex component to render LaTeX. displayMode: true for block equations. -->
            <vue-katex :expression="answer" :options="{ displayMode: true }"/>
        </div>
    </div>
</template>

<style scoped>
/* Base styles for a clean, academic look */
.container {
  font-family: 'KaTeX_Main', 'Times New Roman', serif; /* Consistent academic font */
  max-width: 800px;
  margin: 2rem auto;
  background-color: #ffffff; /* Pure white background */
  padding: 2.5rem 3rem; /* More generous padding */
  border-radius: 12px; /* Slightly more rounded corners for softness */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); /* Softer, more pronounced shadow */
  border: 1px solid #e0e0e0; /* Subtle border for definition */
}

/* Headings */
h1 {
  color: #2c3e50; /* Darker, more professional blue-grey */
  text-align: center;
  font-size: 2.5rem; /* Slightly larger for impact */
  margin-bottom: 0.75rem;
  font-weight: 700; /* Bolder */
}

p {
  text-align: center;
  color: #7f8c8d; /* Muted grey for supporting text */
  font-size: 1.1rem;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

/* Textarea for input */
textarea {
  width: 100%;
  padding: 1rem; /* More padding */
  font-size: 1.1rem; /* Slightly larger font */
  border-radius: 8px; /* Softer corners */
  border: 1px solid #b0bec5; /* Muted, professional border color */
  box-sizing: border-box;
  margin-bottom: 1.5rem;
  resize: vertical; /* Allow vertical resizing */
  min-height: 120px; /* Ensure a decent starting height */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; /* Standard sans-serif for input */
  transition: border-color 0.2s, box-shadow 0.2s; /* Smooth transitions */
}

textarea:focus {
  outline: none;
  border-color: #3498db; /* Highlight border on focus */
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2); /* Soft glow on focus */
}

/* Button */
button {
  display: block;
  width: 100%;
  padding: 1rem; /* More padding */
  font-size: 1.2rem; /* Larger font */
  font-weight: 600; /* Professional weight */
  color: #ffffff;
  background-color: #3498db; /* Professional blue */
  border: none;
  border-radius: 8px; /* Softer corners */
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s; /* Smooth transitions for hover/active */
  letter-spacing: 0.5px; /* Slight letter spacing for professionalism */
}

button:disabled {
  background-color: #bbdefb; /* Lighter, muted blue for disabled state */
  cursor: not-allowed;
  box-shadow: none;
}

button:hover:not(:disabled) {
  background-color: #2980b9; /* Darker blue on hover */
  transform: translateY(-2px); /* Slight lift on hover */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow on hover */
}

button:active:not(:disabled) {
  transform: translateY(0); /* Press effect */
  box-shadow: none;
}

/* Answer and Error Boxes */
.answer-box,
.error-box {
  margin-top: 3rem; /* More space above */
  padding: 2rem; /* More generous padding */
  background-color: #ecf0f1; /* Light grey, soft background */
  border: 1px solid #bdc3c7; /* Muted border */
  border-radius: 8px;
  white-space: pre-wrap;
  text-align: left;
  line-height: 1.8; /* Increased line height for readability */
  font-size: 1.1rem;
  color: #34495e; /* Darker text for readability */
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05); /* Inner shadow for depth */
}

.error-box {
  background-color: #fbecec; /* Soft red for errors */
  color: #c0392b; /* Darker red text */
  border-color: #e74c3c; /* Red border */
  font-weight: 500; /* Slightly bolder for error messages */
}
</style>