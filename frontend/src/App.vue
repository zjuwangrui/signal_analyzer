<template>
  <div id="app">
    <h1>Signal Analyzer</h1>
    <div class="main-layout">
      <div class="controls-panel">
        <FileUpload @upload-success="onUploadSuccess" />
        <Controls @apply-params="onApplyParams" />
      </div>
      <div class="plots-panel">
        <WaveformPlot :plotUrl="plotUrls.waveform" />
        <SpectrogramPlot :plotUrl="plotUrls.spectrogram" />
        <SpectrumPlot :plotUrl="plotUrls.spectrum" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import axios from 'axios';
import FileUpload from './components/FileUpload.vue';
import Controls from './components/Controls.vue';
import WaveformPlot from './components/WaveformPlot.vue';
import SpectrogramPlot from './components/SpectrogramPlot.vue';
import SpectrumPlot from './components/SpectrumPlot.vue';

const uploadedFilename = ref<string | null>(null);
const analysisParams = ref({});
const plotUrls = reactive({
  waveform: '',
  spectrogram: '',
  spectrum: '',
});

const onUploadSuccess = (filename: string) => {
  uploadedFilename.value = filename;
  // Automatically analyze with default params after upload
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

  try {
    const response = await axios.get(`http://localhost:5000/analyze/${uploadedFilename.value}`, {
      params: analysisParams.value,
    });

    const { waveform, spectrogram, spectrum } = response.data;
    plotUrls.waveform = `data:image/png;base64,${waveform}`;
    plotUrls.spectrogram = `data:image/png;base64,${spectrogram}`;
    plotUrls.spectrum = `data:image/png;base64,${spectrum}`;

  } catch (error) {
    console.error('Error analyzing signal:', error);
    alert('Error analyzing signal.');
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
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
}

.plots-panel {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
</style>

