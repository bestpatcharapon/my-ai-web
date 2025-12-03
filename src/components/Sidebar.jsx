import './Sidebar.css';
import { FiPlus, FiMessageSquare } from 'react-icons/fi';

function Sidebar({ conversations, activeConversation, onNewChat, onSelectConversation, onClearAll }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title gradient-text">Best AI Chatbot</h1>
      </div>
      
      <button className="new-chat-btn" onClick={onNewChat}>
        <FiPlus size={20} />
        <span>New chat</span>
      </button>
      
      <div className="conversations-section">
        <div className="conversations-header">
          <h2>Your conversations</h2>
          {conversations.length > 0 && (
            <button className="clear-all-btn" onClick={onClearAll}>Clear All</button>
          )}
        </div>
        
        <div className="conversations-list">
          {conversations.length === 0 ? (
            <p className="empty-state">No conversations yet</p>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                className={`conversation-item ${activeConversation === conv.id ? 'active' : ''}`}
                onClick={() => onSelectConversation(conv.id)}
              >
                <FiMessageSquare size={18} />
                <span className="conversation-title">{conv.title}</span>
              </button>
            ))
          )}
        </div>
      </div>
      
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="user-avatar">
            <span>U</span>
          </div>
          <div className="user-info">
            <p className="user-name">User</p>
            <p className="user-status">Online</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
