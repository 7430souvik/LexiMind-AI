import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../services/authService";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      await register(form);

      navigate("/login");
    } catch (err) {
    const detail = err.response?.data?.detail;

    if (Array.isArray(detail)) {
        setError(detail[0].msg);
    } else {
        setError(detail || "Registration failed.");
    }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md"
      >
        <h1 className="text-3xl font-bold mb-6 text-center">
          Register
        </h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <input
          name="full_name"
          placeholder="Full Name"
          value={form.full_name}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4"
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4"
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-6"
          required
        />

        <button
          disabled={loading}
          className="w-full bg-black text-white py-3 rounded-lg hover:bg-gray-800"
        >
          {loading ? "Creating Account..." : "Register"}
        </button>

        <p className="text-center mt-5">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-blue-600"
          >
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}