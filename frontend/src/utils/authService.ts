import axios from "axios";
import { jwtDecode } from "jwt-decode";

interface TokenResponse {
  access: string;
  refresh: string;
}

// Store tokens and user role
export const storeTokens = (accessToken: string, refreshToken: string, userRole: string) => {
  if (!accessToken || !refreshToken || !userRole) {
    console.error("🚨 Missing tokens or role!", { accessToken, refreshToken, userRole });
    return;
  }

  console.log("✅ Storing tokens and role...");
  sessionStorage.setItem("access_token", accessToken);
  sessionStorage.setItem("refresh_token", refreshToken);
  sessionStorage.setItem("userRole", userRole);
};

// Retrieve tokens
export const getAccessToken = () => sessionStorage.getItem("access_token");
export const getRefreshToken = () => sessionStorage.getItem("refresh_token");
export const getUserRole = () => sessionStorage.getItem("user_role"); //  Retrieve role

// Clear tokens and force logout
export const clearTokens = () => {
  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("refresh_token");
  sessionStorage.removeItem("userRole");
  window.location.href = "/login"; // Redirect to login page
};

// Refresh access token
export const refreshAccessToken = async () => {
  try {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      console.warn("🚨 No refresh token found. Logging out...");
      clearTokens();
      return null;
    }

    console.log("🔄 Refreshing access token...");
    const response = await axios.post<TokenResponse>("http://127.0.0.1:8000/token/refresh/", { 
      refresh: refreshToken 
    });
    
    const newAccessToken = response.data.access;  //  No more TypeScript error
    console.log("✅ New Access Token:", newAccessToken);

    // Decode new access token to get user role
    const decodedToken: any = jwtDecode(newAccessToken);
    console.log("🔹 Decoded Token on Refresh:", decodedToken);

    if (decodedToken.role) {
      console.log("✅ User Role Found (on Refresh):", decodedToken.role);
      storeTokens(newAccessToken, refreshToken, decodedToken.role); // Store new access token and role
    } else {
      console.warn("🚨 Role not found in refreshed token! Keeping existing role.");
      storeTokens(newAccessToken, refreshToken, sessionStorage.getItem("userRole") || "undefined");
    }

    return newAccessToken;
  } catch (error: any) {
    console.error("❌ Error refreshing token:", error.response?.data || error.message);
    clearTokens(); // Logout user if refresh fails
    return null;
  }
};
