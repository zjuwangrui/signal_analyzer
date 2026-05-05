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
      <label for="cmap">Colormap:</label>
      <input id="cmap" type="text" v-model="params.cmap" />
    </div>
    <button @click="applyChanges">Apply</button>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';

const emit = defineEmits(['apply-params']);

const params = reactive({
  sr: 22050,
  n_fft: 2048,
  hop_length: 512,
  cmap: 'viridis',
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
