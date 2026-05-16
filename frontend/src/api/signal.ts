import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export interface AnimationParams {
  sr?: number;
  n_fft?: number;
  hop_length?: number;
  cmap?: string;
  frame_nums?: number;
}

export interface AnimationResponse {
  filename: string;
  url: string;
  download_url: string;
}

export const createStftAnimation = async (
  filename: string,
  params: AnimationParams = {},
): Promise<AnimationResponse> => {
  const response = await axios.post<AnimationResponse>(
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
