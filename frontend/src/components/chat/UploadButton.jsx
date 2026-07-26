import { useRef } from "react";
import { Paperclip } from "lucide-react";

export default function UploadButton({ onFileSelect }) {
  const inputRef = useRef(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    onFileSelect(file);

    // Reset the input so the same file can be selected again
    e.target.value = "";
  };

  return (
    <>
      <button
        type="button"
        onClick={handleClick}
        className="mr-3 p-2 rounded-full hover:bg-gray-100 transition"
      >
        <Paperclip size={20} />
      </button>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        hidden
        onChange={handleFileChange}
      />
    </>
  );
}