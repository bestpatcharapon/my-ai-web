import './Message.css';

function Message({ message, isBot }) {
  return (
    <div className={`message ${isBot ? 'bot' : 'user'} animate-slide-in`}>
      <div className="message-avatar">
        {isBot ? '🤖' : '👤'}
      </div>
      <div className="message-content">
        <div className="message-text">{message.text}</div>
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
