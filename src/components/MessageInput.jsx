import { useState } from 'react';
import './MessageInput.css';
import { FiSend, FiImage } from 'react-icons/fi';

function MessageInput({ onSendMessage, isLoading }) {
  const [message, setMessage] = useState('');
  const [image, setImage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() || image) {
      onSendMessage(message, image);
      setMessage('');
      setImage(null);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      {image && (
        <div className="image-preview">
          <img src={image} alt="Preview" />
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
          />
        </label>
        
        <textarea
          className="message-input"
          placeholder="What's in your mind?..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          rows={1}
        />
        
        <button
          type="submit"
          className="send-btn"
          disabled={isLoading || (!message.trim() && !image)}
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
