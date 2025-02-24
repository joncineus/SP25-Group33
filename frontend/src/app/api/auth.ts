import axiosInstance from './axiosInstance';

export interface RegisterData {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  password: string;
  role: 'teacher' | 'student';
}

export interface LoginData {
  username: string;
  password: string;
}

export interface AuthResponse {
  role: string;
  refresh: string;
  access: string;
}

export const registerUser = async (data: RegisterData): Promise<AuthResponse> => {
  try {
    const response = await axiosInstance.post<AuthResponse>('auth/register/', data);
    return response.data;
  } catch (error: any) {
    throw error.response?.data || error;
  }
};

export const loginUser = async (data: LoginData): Promise<AuthResponse> => {
  try {
    const response = await axiosInstance.post<AuthResponse>('auth/login/', data);
    return response.data;
  } catch (error: any) {
    throw error.response?.data || error;
  }
};
