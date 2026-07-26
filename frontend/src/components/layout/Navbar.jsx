export default function Navbar() {
  return (
    <header className="h-16 border-b bg-white px-6 flex items-center justify-between">

      <h1 className="text-xl font-bold">
        LexiMind AI
      </h1>

      <div className="flex items-center gap-4">

        <button className="px-4 py-2 rounded-lg border hover:bg-gray-100">
          Search
        </button>

        <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
          S
        </div>

      </div>

    </header>
  );
}