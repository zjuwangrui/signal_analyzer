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
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 5px;
}
.control-item {
  margin-bottom: 10px;
}
label {
  margin-right: 10px;
}
</style>
