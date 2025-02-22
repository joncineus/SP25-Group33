// src/types.d.ts
interface UserData {
    username: string;
    email: string;
    role: string;
    id: number;
  }
  
  interface RegistrationResponse {
    message: string;
    // ... other properties API might return
  }

  interface AuthResponse {  
    role: string;
    // ... other properties returned by API
}