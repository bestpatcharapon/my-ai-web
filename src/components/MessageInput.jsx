import { useState, useRef, useEffect } from 'react';
import './MessageInput.css';
import { FiSend, FiImage } from 'react-icons/fi';

function MessageInput({ onSendMessage, isLoading }) {
  const [inputText, setInputText] = useState('');
  const [previewImage, setPreviewImage] = useState(null);
  const [imageData, setImageData] = useState(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // ✅ Auto-resize textarea ตามเนื้อหา
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto'; // รีเซ็ตความสูง
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`; // ขยายตาม content (max 150px)
    }
  }, [inputText]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim() || imageData) {
      onSendMessage(inputText, imageData);
      setInputText('');
      setPreviewImage(null);
      setImageData(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = ''; // Clear the file input
      }
    }
  };

  const handleKeyPress = (e) => {
    // Enter = ส่งข้อความ | Shift+Enter = ขึ้นบรรทัดใหม่
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewImage(URL.createObjectURL(file));
        setImageData(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePaste = (e) => {
    const items = e.clipboardData?.items;
    if (!items) return;

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.startsWith('image/')) {
        e.preventDefault();
        const file = items[i].getAsFile();
        if (file) {
          const reader = new FileReader();
          reader.onloadend = () => {
            setPreviewImage(URL.createObjectURL(file));
            setImageData(reader.result);
          };
          reader.readAsDataURL(file);
        }
        break;
      }
    }
  };

  const handleRemoveImage = () => {
    if (previewImage) {
      URL.revokeObjectURL(previewImage); // Clean up the object URL
    }
    setPreviewImage(null);
    setImageData(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = ''; // Clear the file input
    }
  };

  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      {previewImage && (
        <div className="image-preview">
          <img src={previewImage} alt="Preview" />
          <button
            type="button"
            className="remove-image-btn"
            onClick={() => setImage(null)}
          >
            ×
          </button>
        </div>
      )}
      
      <div className="input-wrapper">
        <label className="image-upload-btn" title="Upload image">
          <FiImage size={20} />
          <input
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            style={{ display: 'none' }}
            ref={fileInputRef}
          />
        </label>
        
        <textarea
          ref={textareaRef}
          className="message-input"
          placeholder="What's in your mind?..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyPress}
          onPaste={handlePaste}
          disabled={isLoading}
        />
        
        <button
          type="submit"
          className="send-btn"
          disabled={isLoading || (!inputText.trim() && !imageData)}
        >
          {isLoading ? (
            <div className="loading-spinner" />
          ) : (
            <FiSend size={20} />
          )}
        </button>
      </div>
    </form>
  );
}

export default MessageInput;
