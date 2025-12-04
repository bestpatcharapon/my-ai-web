import './Message.css';
import { FiCopy, FiCheck, FiVolume2, FiVolumeX } from 'react-icons/fi';
import { useState } from 'react';

function Message({ message, isBot }) {
  const [copied, setCopied] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSpeak = () => {
    // ถ้ากำลังพูดอยู่ ให้หยุด
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    // สร้าง speech synthesis
    const utterance = new SpeechSynthesisUtterance(message.text);
    utterance.lang = 'th-TH'; // ภาษาไทย
    utterance.rate = 1.0; // ความเร็ว
    utterance.pitch = 1.0; // ระดับเสียง
    
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className={`message ${isBot ? 'bot' : 'user'} animate-slide-in`}>
      <div className="message-avatar">
        {isBot ? <i className="fa-solid fa-robot"></i> : <i className="fa-solid fa-user"></i>}
      </div>
      <div className="message-content">
        {message.image && (
          <div className="message-image">
            <img src={message.image} alt="Uploaded" />
          </div>
        )}
        <div className="message-text">{message.text}</div>
        
        {isBot && (
          <div className="message-actions">
            <button 
              className="icon-btn" 
              onClick={handleSpeak}
              title={isSpeaking ? "หยุดพูด" : "อ่านข้อความ"}
            >
              {isSpeaking ? <FiVolumeX size={16} /> : <FiVolume2 size={16} />}
            </button>
            <button 
              className="icon-btn" 
              onClick={handleCopy}
              title={copied ? "Copied!" : "Copy message"}
            >
              {copied ? <FiCheck size={16} /> : <FiCopy size={16} />}
            </button>
          </div>
        )}
        
        {message.timestamp && (
          <div className="message-timestamp">
            {new Date(message.timestamp).toLocaleTimeString('th-TH', { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
