import { Plus } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-72 border-r bg-white flex flex-col">

      <div className="p-4">

        <button className="w-full bg-black text-white rounded-xl py-3 flex justify-center items-center gap-2 hover:bg-gray-800">

          <Plus size={18} />

          New Chat

        </button>

      </div>

      <div className="flex-1 overflow-y-auto p-4">

        <h2 className="text-gray-500 text-sm mb-3">
          Recent Chats
        </h2>

        <div className="space-y-2">

          <button className="w-full text-left rounded-lg hover:bg-gray-100 p-3">
            Employment Contract
          </button>

          <button className="w-full text-left rounded-lg hover:bg-gray-100 p-3">
            NDA Agreement
          </button>

          <button className="w-full text-left rounded-lg hover:bg-gray-100 p-3">
            Lease Agreement
          </button>

        </div>

      </div>

    </aside>
  );
}