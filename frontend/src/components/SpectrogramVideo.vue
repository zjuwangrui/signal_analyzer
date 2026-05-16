<template>
  <div class="video-container">
    <h4>Spectrogram Video</h4>
    <video v-if="videoUrl" :src="videoUrl" controls></video>
    <div v-else class="placeholder">No video to display</div>
    <a v-if="videoUrl" :href="videoUrl" download="spectrogram_video.mp4">
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
  border: 1px solid var(--border-color);
  padding: 10px;
  margin-bottom: 10px;
  text-align: center;
  background-color: var(--dark-blue-bg);
  border-radius: 4px;
}
h4 {
  color: var(--text-light);
}
video {
  max-width: 100%;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}
.placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-dark);
  border: 1px dashed var(--border-color);
  border-radius: 4px;
}
button {
  margin-top: 10px;
  padding: 8px 15px;
  background-color: var(--accent-blue);
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #5cacee;
}
</style>
