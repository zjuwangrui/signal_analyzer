<template>
  <div class="plot-container">
    <h4>Spectrogram</h4>
    <img v-if="plotUrl" :src="plotUrl" alt="Spectrogram" />
    <div v-else class="placeholder">No data to display</div>
    <button v-if="plotUrl" @click="saveImage">Save Image</button>
  </div>
</template>

<script setup lang="ts">

const props = defineProps<{
  plotUrl: string;
}>();

const saveImage = () => {
  if (!props.plotUrl) return;
  const a = document.createElement('a');
  a.href = props.plotUrl;
  a.download = 'spectrogram.png';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};
</script>

<style scoped>
.plot-container {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  text-align: center;
}
img {
  max-width: 100%;
}
.placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  border: 1px dashed #ccc;
}
</style>
