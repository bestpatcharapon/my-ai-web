import { useState, useEffect } from 'react';
import './VoiceButton.css';
import { FiMic, FiMicOff } from 'react-icons/fi';

function VoiceButton({ onTranscript, disabled }) {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {
    // ตรวจสอบว่า browser รองรับ Speech Recognition หรือไม่
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false; // หยุดอัตโนมัติเมื่อเงียบ
      recognitionInstance.interimResults = true; // แสดงผลระหว่างพูด
      recognitionInstance.lang = 'th-TH'; // ภาษาไทยเป็นหลัก
      
      recognitionInstance.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        
        console.log('🎤 Voice transcript:', transcript);
        
        if (onTranscript) {
          onTranscript(transcript);
        }
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        
        let errorMessage = 'ไม่สามารถใช้ไมค์ได้';
        if (event.error === 'network') {
          errorMessage = '⚠️ ต้องการ internet connection เพื่อใช้งานไมค์';
        } else if (event.error === 'not-allowed') {
          errorMessage = '⚠️ กรุณาอนุญาตให้ใช้ไมค์ในการตั้งค่า browser';
        }
        
        alert(errorMessage);
        setIsListening(false);
      };
      
      recognitionInstance.onend = () => {
        setIsListening(false);
      };
      
      setRecognition(recognitionInstance);
      setIsSupported(true);
    } else {
      console.warn('Speech Recognition not supported in this browser');
      setIsSupported(false);
    }
  }, [onTranscript]);

  const toggleListening = () => {
    if (!recognition) return;
    
    if (isListening) {
      console.log('🛑 Stopping voice recognition');
      recognition.stop();
      setIsListening(false);
    } else {
      console.log('▶️ Starting voice recognition...');
      try {
        recognition.start();
        setIsListening(true);
      } catch (error) {
        console.error('Failed to start recognition:', error);
      }
    }
  };

  // ถ้า browser ไม่รองรับ ไม่แสดงปุ่ม
  if (!isSupported) {
    return null;
  }

  return (
    <button
      type="button"
      className={`voice-btn ${isListening ? 'listening' : ''}`}
      onClick={toggleListening}
      disabled={disabled}
      title={isListening ? 'หยุดฟัง' : 'พูดเพื่อพิมพ์'}
    >
      {isListening ? <FiMicOff size={22} /> : <FiMic size={22} />}
      {isListening && <span className="pulse-ring"></span>}
    </button>
  );
}

export default VoiceButton;
