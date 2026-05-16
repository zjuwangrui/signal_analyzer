<template>
  <div class="video-container">
    <h4>Spectrum Video</h4>
    <video v-if="videoUrl" :src="videoUrl" controls></video>
    <div v-else class="placeholder">No video to display</div>
    <a v-if="videoUrl" :href="videoUrl" download="spectrum_video.mp4">
      <button>Download Video</button>
    </a>
  </div>
</template>

<script setup lang="ts">

defineProps<{
  videoUrl: string;
}>();
</script>

<style scoped>
.video-container {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  text-align: center;
}
video {
  max-width: 100%;
  border: 1px solid #ccc;
}
.placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  border: 1px dashed #ccc;
}
button {
  margin-top: 10px;
}
</style>
