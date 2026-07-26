import api from "./api";

export async function register(userData) {
  const response = await api.post("/auth/register", userData);
  return response.data;
}

export async function login(credentials) {
  const formData = new URLSearchParams();

  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  const response = await api.post(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
  localStorage.setItem(
    "token",
    response.data.access_token
  );

  return response.data;
  }


export async function getCurrentUser() {
  const response = await api.get("/users/me");
  return response.data;
}

export function logout() {
  localStorage.removeItem("token");
}