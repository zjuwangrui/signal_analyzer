<template>
  <div class="controls">
    <h3>Analysis Parameters</h3>
    <div class="control-item">
      <label for="sr">Sample Rate (sr):</label>
      <input id="sr" type="number" v-model.number="params.sr" />
    </div>
    <div class="control-item">
      <label for="n_fft">N_FFT:</label>
      <input id="n_fft" type="number" v-model.number="params.n_fft" />
    </div>
    <div class="control-item">
      <label for="hop_length">Hop Length:</label>
      <input id="hop_length" type="number" v-model.number="params.hop_length" />
    </div>
    <div class="control-item">
      <label for="win_length">Window Length:</label>
      <input id="win_length" type="number" v-model.number="params.win_length" />
    </div>
    <div class="control-item">
      <label for="window">Window:</label>
      <input id="window" type="text" v-model="params.window" />
    </div>
    <div class="control-item">
      <label for="cmap">Colormap:</label>
      <input id="cmap" type="text" v-model="params.cmap" />
    </div>
    <button @click="applyChanges">Apply</button>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue';

const emit = defineEmits(['apply-params']);

const params = reactive({
  sr: 22050,
  n_fft: 2048,
  hop_length: 512,
  win_length: 2048,
  window: 'hann',
  cmap: 'viridis',
});

// Keep win_length in sync with n_fft by default
watch(() => params.n_fft, (newVal) => {
  params.win_length = newVal;
});

const applyChanges = () => {
  emit('apply-params', { ...params });
};
</script>

<style scoped>
.controls {
  color: var(--text-light);
}
h3 {
  color: var(--accent-cyan);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
  margin-top: 0;
}
.control-item {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
label {
  margin-bottom: 5px;
  font-size: 14px;
  color: var(--text-dark);
}
input {
  width: 100%;
  padding: 8px;
  background-color: var(--dark-blue-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  color: var(--text-light);
}
button {
  width: 100%;
  padding: 10px;
  background-color: var(--accent-blue);
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #5cacee;
}
</style>
