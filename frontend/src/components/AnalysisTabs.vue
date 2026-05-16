<template>
  <div class="analysis-tabs">
    <div class="tab-nav">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.name }}
      </button>
    </div>
    <div class="tab-content">
      <div v-if="activeTab === 'waveform'">
        <WaveformPlot :plotUrl="analysisResults.waveform" />
      </div>
      <div v-if="activeTab === 'spectrum'">
        <SpectrumPlot :plotUrl="analysisResults.spectrum" />
      </div>
      <div v-if="activeTab === 'spectrogram'">
        <SpectrogramPlot :plotUrl="analysisResults.spectrogram" />
      </div>
      <div v-if="activeTab === 'spectrogramVideo'">
        <SpectrogramVideo :videoUrl="analysisResults.spectrogramVideo" />
      </div>
      <div v-if="activeTab === 'spectrumVideo'">
        <SpectrumVideo :videoUrl="analysisResults.spectrumVideo" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import WaveformPlot from './WaveformPlot.vue';
import SpectrumPlot from './SpectrumPlot.vue';
import SpectrogramPlot from './SpectrogramPlot.vue';
import SpectrogramVideo from './SpectrogramVideo.vue';
import SpectrumVideo from './SpectrumVideo.vue';

defineProps<{
  analysisResults: {
    waveform: string;
    spectrum: string;
    spectrogram: string;
    spectrogramVideo: string;
    spectrumVideo: string;
  };
}>();

const activeTab = ref('waveform');

const tabs = [
  { id: 'waveform', name: 'Time-Domain Waveform' },
  { id: 'spectrum', name: 'Spectrum Plot' },
  { id: 'spectrogram', name: 'Spectrogram Plot' },
  { id: 'spectrogramVideo', name: 'Spectrogram Video' },
  { id: 'spectrumVideo', name: 'Spectrum Video' },
];
</script>

<style scoped>
.tab-nav {
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 10px;
}
.tab-nav button {
  padding: 10px 15px;
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 16px;
  color: var(--text-dark);
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}
.tab-nav button:hover {
  color: var(--accent-cyan);
}
.tab-nav button.active {
  border-bottom-color: var(--accent-cyan);
  color: var(--accent-cyan);
}
.tab-content {
  padding: 10px;
}
</style>
