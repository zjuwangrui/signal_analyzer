<template>
  <div id="app">
    <h1>Signal Analyzer</h1>
    <div class="main-layout">
      <div class="controls-panel">
        <FileUpload @upload-success="onUploadSuccess" />
        <Controls @apply-params="onApplyParams" />
      </div>
      <div class="plots-panel">
        <div v-if="isLoading" class="loading-overlay">
          <p>Analyzing...</p>
        </div>
        <AnalysisTabs v-if="analysisCompleted" :analysisResults="analysisResults" />
        <div v-else-if="!isLoading" class="placeholder-text">
          Please upload a file to begin analysis.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import axios from 'axios';
import FileUpload from './components/FileUpload.vue';
import Controls from './components/Controls.vue';
import AnalysisTabs from './components/AnalysisTabs.vue';

const uploadedFilename = ref<string | null>(null);
const analysisParams = ref({});
const analysisResults = reactive({
  waveform: '',
  spectrogram: '',
  spectrum: '',
  spectrogramVideo: '',
  spectrumVideo: '',
});
const isLoading = ref(false);
const analysisCompleted = ref(false);

const onUploadSuccess = (filename: string) => {
  uploadedFilename.value = filename;
  analysisCompleted.value = false; // Reset on new upload
  analyzeSignal();
};

const onApplyParams = (params: any) => {
  analysisParams.value = params;
  if (uploadedFilename.value) {
    analyzeSignal();
  } else {
    alert('Please upload a file first.');
  }
};

const analyzeSignal = async () => {
  if (!uploadedFilename.value) return;

  isLoading.value = true;
  analysisCompleted.value = false;

  try {
    // For now, we only fetch images. Video endpoints will be added later.
    const response = await axios.get(`http://localhost:5000/analyze/${uploadedFilename.value}`, {
      params: analysisParams.value,
    });

    const { waveform, spectrogram, spectrum } = response.data;
    analysisResults.waveform = `data:image/png;base64,${waveform}`;
    analysisResults.spectrogram = `data:image/png;base64,${spectrogram}`;
    analysisResults.spectrum = `data:image/png;base64,${spectrum}`;
    
    // Placeholder for video URLs - will be updated when backend supports it
    analysisResults.spectrogramVideo = ''; // e.g., 'http://localhost:5000/videos/spectrogram.mp4'
    analysisResults.spectrumVideo = '';    // e.g., 'http://localhost:5000/videos/spectrum.mp4'

    analysisCompleted.value = true;
  } catch (error) {
    console.error('Error analyzing signal:', error);
    alert('Error analyzing signal.');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style>
:root {
  --dark-blue-bg: #0a192f;
  --light-blue-panel: #112240;
  --accent-blue: #42a5f5;
  --accent-cyan: #64ffda;
  --text-light: #ccd6f6;
  --text-dark: #8892b0;
  --border-color: #233554;
}

body {
  background-color: var(--dark-blue-bg);
  color: var(--text-light);
}

#app {
  font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 40px;
}

h1 {
  color: var(--accent-cyan);
  font-weight: 600;
  letter-spacing: 1.5px;
}

.main-layout {
  display: flex;
  flex-direction: row;
  gap: 20px;
  padding: 20px;
}

.controls-panel {
  flex: 1;
  max-width: 300px;
  background-color: var(--light-blue-panel);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.plots-panel {
  flex: 3;
  position: relative;
  min-height: 400px; /* Ensure it has some height */
  background-color: var(--light-blue-panel);
  padding: 10px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(10, 25, 47, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5em;
  z-index: 10;
  color: var(--accent-cyan);
  border-radius: 8px;
}

.placeholder-text {
  color: var(--text-dark);
  font-size: 1.2em;
  margin-top: 50px;
}
</style>


