import { useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';

function App() {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleNewChat = () => {
    const newConvId = Date.now().toString();
    const newConv = {
      id: newConvId,
      title: 'New Conversation',
      messages: []
    };
    
    setConversations([newConv, ...conversations]);
    setActiveConversation(newConvId);
    setMessages([]);
  };

  const handleSelectConversation = (convId) => {
    const conv = conversations.find(c => c.id === convId);
    if (conv) {
      setActiveConversation(convId);
      setMessages(conv.messages);
    }
  };

  const handleSendMessage = async (text, image) => {
    if (!text.trim() && !image) return;

    // Add user message
    const userMessage = {
      role: 'user',
      text: text || '(Image sent)',
      timestamp: new Date().toISOString()
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      // Call backend API
      const response = await fetch('/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: text,
          image: image || null
        }),
      });

      const data = await response.json();

      // Add bot response
      const botMessage = {
        role: 'bot',
        text: data.result || 'Sorry, I could not process your request.',
        timestamp: new Date().toISOString()
      };

      const updatedMessages = [...newMessages, botMessage];
      setMessages(updatedMessages);

      // Update conversation
      if (activeConversation) {
        setConversations(conversations.map(conv => 
          conv.id === activeConversation 
            ? { 
                ...conv, 
                messages: updatedMessages,
                title: text.slice(0, 30) + (text.length > 30 ? '...' : '')
              }
            : conv
        ));
      } else {
        // Create new conversation if none is active
        const newConvId = Date.now().toString();
        const newConv = {
          id: newConvId,
          title: text.slice(0, 30) + (text.length > 30 ? '...' : ''),
          messages: updatedMessages
        };
        setConversations([newConv, ...conversations]);
        setActiveConversation(newConvId);
      }

    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        role: 'bot',
        text: 'Sorry, there was an error processing your request. Please make sure the backend is running.',
        timestamp: new Date().toISOString()
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Sidebar
        conversations={conversations}
        activeConversation={activeConversation}
        onNewChat={handleNewChat}
        onSelectConversation={handleSelectConversation}
      />
      <ChatArea
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
