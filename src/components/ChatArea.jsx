import { useEffect, useRef } from 'react';
import './ChatArea.css';
import Message from './Message';
import MessageInput from './MessageInput';

function ChatArea({ messages, onSendMessage, isLoading }) {
  const messagesEndRef = useRef(null);

  console.log('🎨 ChatArea render - messages count:', messages.length);
  console.log('🎨 ChatArea render - messages:', messages);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-area">
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-chat-state">
            <div className="empty-icon">💬</div>
            <h3>Start a conversation</h3>
            <p>Send a message to get started with your AI assistant</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg, index) => (
              <Message
                key={index}
                message={msg}
                isBot={msg.role === 'bot'}
              />
            ))}
            {isLoading && (
              <div className="message bot typing-indicator">
                <div className="message-avatar">
                  <i className="fa-solid fa-robot"></i>
                </div>
                <div className="message-content">
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      <MessageInput onSendMessage={onSendMessage} isLoading={isLoading} />
    </div>
  );
}

export default ChatArea;
