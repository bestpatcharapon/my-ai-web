import { useState, useRef, useEffect } from 'react';
import './MessageInput.css';
import { FiSend, FiPlus } from 'react-icons/fi';
import VoiceButton from './VoiceButton';

function MessageInput({ onSendMessage, isLoading }) {
  const [inputText, setInputText] = useState('');
  const [previewImage, setPreviewImage] = useState(null);
  const [imageData, setImageData] = useState(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Handler สำหรับรับข้อความจาก Voice
  const handleVoiceTranscript = (transcript) => {
    console.log('📝 Setting input text:', transcript);
    setInputText(transcript);
  };

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
            onClick={handleRemoveImage}
          >
            ×
          </button>
        </div>
      )}
      
      <div className="input-wrapper">
        <textarea
          ref={textareaRef}
          className="message-input"
          placeholder="ส่งข้อความถึง Best Bot"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyPress}
          onPaste={handlePaste}
          rows={1}
          disabled={isLoading}
        />
                <div className="button-row">
            <div className="left-buttons">
              <label className="image-upload-btn" title="Upload image">
                <FiPlus size={22} />
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  style={{ display: 'none' }}
                  ref={fileInputRef}
                />
              </label>
              
              <VoiceButton 
                onTranscript={handleVoiceTranscript}
                disabled={isLoading}
              />
            </div>
          
          <button 
            type="submit"
            className="send-btn" 
            disabled={isLoading || (!inputText.trim() && !imageData)}
            >
            {isLoading ? (
              <div className="loading-spinner"></div>
            ) : (
              <FiSend size={18} />
            )}
          </button>
        </div>
      </div>
    </form>
  );
}

export default MessageInput;
