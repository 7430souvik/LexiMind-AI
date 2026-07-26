import Navbar from "../components/layout/Navbar";
import Sidebar from "../components/layout/Sidebar";

export default function MainLayout({ children }) {
  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <main className="flex-1 overflow-hidden">
          {children}
        </main>
      </div>
    </div>
  );
}