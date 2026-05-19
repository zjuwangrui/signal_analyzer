import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export interface AnimationParams {
  sr?: number;
  n_fft?: number;
  hop_length?: number;
  cmap?: string;
  frame_nums?: number;
  render_fps?: number;
  max_video_frames?: number;
}

export interface StftAnimationResponse {
  task_id: string;
}

export const createStftAnimation = async (
  filename: string,
  params: AnimationParams = {},
): Promise<StftAnimationResponse> => {
  const response = await axios.post<StftAnimationResponse>(
    `${API_BASE_URL}/animate/${filename}`,
    null,
    { params },
  );
  return response.data;
};

export const toAbsoluteApiUrl = (path: string): string => {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
};
