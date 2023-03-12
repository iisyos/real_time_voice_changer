<script setup lang="ts">
import { ref } from 'vue'
import axios, { AxiosRequestConfig } from "axios";
import { speak } from "./util";

const recognition = new webkitSpeechRecognition()
recognition.lang = 'ja-JP';
recognition.interimResults = true;
recognition.continuous = true;

const inputText = ref('place holder')
recognition.onresult = async (event) => {
  for (let i = event.resultIndex; i < event.results.length; i++) {
    let transcript = event.results[i][0].transcript;
    if (event.results[i].isFinal) {
      inputText.value = ref(transcript)
      await speak(transcript)
    }
  }
}

const called = async () => {
  recognition.start();
}

</script>


<template>
  <button type="button" @click="called()">recode start</button>
  <div>
    {{ inputText }}
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
