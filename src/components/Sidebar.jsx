import './Sidebar.css';
import { FiPlus, FiMessageSquare } from 'react-icons/fi';

function Sidebar({ conversations, activeConversation, onNewChat, onSelectConversation, onClearAll }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-title-wrapper">
          <img src="/gg.png" alt="Logo" className="sidebar-logo" />
          <h1 className="sidebar-title gradient-text">Best AI Chatbot</h1>
        </div>
      </div>
      
      <div className="sidebar-content">
        {/* New chat as list item */}
        <button className="sidebar-item new-chat-item" onClick={onNewChat}>
          <FiPlus size={18} />
          <span>New chat</span>
        </button>

        {/* Conversations section */}
        <div className="conversations-section">
          {conversations.length > 0 && (
            <h2 className="section-label">Your chats</h2>
          )}
          
          <div className="conversations-list">
            {conversations.map((conv) => (
              <button
                key={conv.id}
                className={`sidebar-item conversation-item ${activeConversation === conv.id ? 'active' : ''}`}
                onClick={() => onSelectConversation(conv.id)}
              >
                <FiMessageSquare size={16} />
                <span className="conversation-title">{conv.title}</span>
              </button>
            ))}
          </div>
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
