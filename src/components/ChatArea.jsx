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
      <div className="chat-header">
        <h2 className="chat-title">Best AI Chatbot</h2>
        <p className="chat-subtitle">Ask me anything...</p>
      </div>
      
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
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      <MessageInput onSendMessage={onSendMessage} isLoading={isLoading} />
    </div>
  );
}

export default ChatArea;
