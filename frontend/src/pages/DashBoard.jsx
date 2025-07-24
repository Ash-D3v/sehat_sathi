import React, { useState } from 'react';
import ChatMessage from '../components/ChatMessage';
import SymptomChecker from '../utils/symptomChecker';
import { 
  Heart, 
  Plus, 
  MessageSquare, 
  AlertTriangle, 
  MapPin, 
  Lightbulb, 
  Settings, 
  Menu,
  Mic,
  Send,
  Globe
} from 'lucide-react';

const Dashboard = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI health assistant. Please describe your symptoms and I'll help analyze them.",
      isBot: true,
      timestamp: new Date()
    }
  ]);
  const [isAnalysisExpanded, setIsAnalysisExpanded] = useState(false);
  const [selectedSymptom, setSelectedSymptom] = useState('');
  const [inputText, setInputText] = useState('');
  const [activeNavItem, setActiveNavItem] = useState('consultation');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState(null);

  // Initialize symptom checker
  const symptomChecker = new SymptomChecker();

  React.useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
      if (window.innerWidth <= 768) {
        setIsSidebarCollapsed(true);
      }
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const quickSymptoms = [
    'I have a severe headache',
    'I feel chest pain and shortness of breath',
    'I have stomach pain and nausea',
    'I have fever and cough',
    'I feel dizzy and confused',
    'I have body ache and fatigue'
  ];

  const handleSendMessage = () => {
    if (!inputText.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: inputText,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Simulate typing delay and process symptoms
    setTimeout(() => {
      const analysis = symptomChecker.processSymptoms(inputText);
      
      const botMessage = {
        id: messages.length + 2,
        text: analysis.hasSymptoms ? analysis : analysis.message,
        isBot: true,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
      
      if (analysis.hasSymptoms) {
        setCurrentAnalysis(analysis);
        setIsAnalysisExpanded(true);
      }
    }, 1500);
  };

  const handleQuickSymptom = (symptom) => {
    setInputText(symptom);
    setSelectedSymptom(symptom);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const sidebarItems = [
    { 
      id: 'consultation',
      icon: Plus, 
      label: 'New Consultation', 
      active: activeNavItem === 'consultation',
      badge: null,
      description: 'Start a new health consultation'
    },
    { 
      id: 'history',
      icon: MessageSquare, 
      label: 'Chat History', 
      active: activeNavItem === 'history',
      description: 'View your consultation history'
    },
    { 
      id: 'emergency',
      icon: AlertTriangle, 
      label: 'Emergency', 
      active: activeNavItem === 'emergency',
      badge: null,
      description: 'Emergency medical assistance'
    },
    { 
      id: 'hospitals',
      icon: MapPin, 
      label: 'Nearby Hospitals', 
      active: activeNavItem === 'hospitals',
      badge: null,
      description: 'Find hospitals near you'
    },
    { 
      id: 'tips',
      icon: Lightbulb, 
      label: 'Health Tips', 
      active: activeNavItem === 'tips',
      description: 'Daily health tips and advice'
    },
    { 
      id: 'settings',
      icon: Settings, 
      label: 'Settings', 
      active: activeNavItem === 'settings',
      badge: null,
      description: 'App settings and preferences'
    }
  ];

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <div className={`sidebar ${isSidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="logo">
          <Heart className="logoIcon" />
          {!isSidebarCollapsed && <span className="logoText">SehatSathi</span>}
          <Menu 
            className="menuIcon" 
            onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          />
        </div>

        <nav className="navigation">
          {sidebarItems.map((item, index) => (
            <div 
              key={index} 
              className={`navItem ${item.active ? 'active' : ''}`}
              onClick={() => setActiveNavItem(item.id)}
              title={isSidebarCollapsed ? item.description : ''}
            >
              <div className="navIconContainer">
                <item.icon className="navIcon" />
                {item.badge && (
                  <span className={`badge ${typeof item.badge === 'number' ? 'number' : 'text'}`}>
                    {item.badge}
                  </span>
                )}
              </div>
              {!isSidebarCollapsed && (
                <>
                  <span className="navLabel">{item.label}</span>
                  {item.badge && (
                    <span className={`badge ${typeof item.badge === 'number' ? 'number' : 'text'}`}>
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </div>
          ))}
        </nav>

        <div className="sidebarFooter">
          <div className="userProfile">
            <div className="userAvatar">
              <span>U</span>
            </div>
            {!isSidebarCollapsed && (
              <div className="userInfo">
                <span className="userName">User</span>
                <span className="userStatus">Online</span>
              </div>
            )}
          </div>
          
          <div 
            className="emergencyButton"
            onClick={() => setActiveNavItem('emergency')}
          >
            <AlertTriangle className="emergencyIcon" />
            {!isSidebarCollapsed && <span>Emergency</span>}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mainContent">
        <div className="header">
          <h1 className="title">Health Consultation</h1>
          <div className="languageSelector">
            <Globe className="globeIcon" />
            <span>EN</span>
          </div>
        </div>

        <div className="chatArea">
          <div className="messagesContainer">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message.text}
                isBot={message.isBot}
              />
            ))}
            
            {isTyping && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-100 text-gray-800 rounded-lg rounded-bl-sm px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-sm text-gray-500">Analyzing symptoms...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="symptomButtons">
            <h4 className="quickSymptomsTitle">Quick Symptom Examples:</h4>
            {quickSymptoms.map((symptom, index) => (
              <button
                key={index}
                className={`symptomButton ${selectedSymptom === symptom ? 'selected' : ''}`}
                onClick={() => handleQuickSymptom(symptom)}
              >
                {symptom}
              </button>
            ))}
          </div>

          <div className="inputArea">
            <div className="inputContainer">
              <input
                type="text"
                placeholder="Describe your symptoms..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                className="textInput"
              />
              <button className="micButton">
                <Mic className="micIcon" />
              </button>
              <button 
                className="sendButton"
                onClick={handleSendMessage}
                disabled={!inputText.trim() || isTyping}
              >
                <Send className="sendIcon" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Health Analysis Panel */}
      <div className={`analysisPanel ${isAnalysisExpanded ? 'expanded' : ''}`}>
        <div className="analysisHeader" onClick={() => setIsAnalysisExpanded(!isAnalysisExpanded)}>
          <h3>Health Analysis</h3>
          <span className="analysisStatus">
            {currentAnalysis ? currentAnalysis.topDisease?.name.toUpperCase() : 'NO DATA'}
          </span>
        </div>
        <div className="analysisContent">
          {currentAnalysis ? (
            <AnalysisPanel analysis={currentAnalysis} />
          ) : (
            <p className="noDataText">No analysis data yet. Start by describing your symptoms.</p>
          )}
        </div>
      </div>

      <style jsx>{`
        .dashboard {
          display: flex;
          height: 100vh;
          background: #1a1a1a;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          color: white;
        }

        .sidebar {
          width: 280px;
          background: #2d2d2d;
          padding: 20px 0;
          display: flex;
          flex-direction: column;
          border-right: 1px solid #404040;
          transition: width 0.3s ease;
          position: relative;
          z-index: 1000;
        }

        .sidebar.collapsed {
          width: 80px;
        }

        .logo {
          display: flex;
          align-items: center;
          padding: 0 20px 30px;
          border-bottom: 1px solid #404040;
          margin-bottom: 20px;
          justify-content: space-between;
        }

        .sidebar.collapsed .logo {
          justify-content: center;
          padding: 0 10px 30px;
        }

        .logoIcon {
          width: 24px;
          height: 24px;
          color: #00d4ff;
          margin-right: 12px;
        }

        .sidebar.collapsed .logoIcon {
          margin-right: 0;
        }

        .logoText {
          font-size: 18px;
          font-weight: 600;
          color: #00d4ff;
          flex: 1;
          transition: opacity 0.3s ease;
        }

        .sidebar.collapsed .logoText {
          display: none;
        }

        .menuIcon {
          width: 20px;
          height: 20px;
          color: #888;
          cursor: pointer;
          transition: color 0.2s;
        }

        .menuIcon:hover {
          color: #00d4ff;
        }

        .navigation {
          flex: 1;
          padding: 0 20px;
        }

        .sidebar.collapsed .navigation {
          padding: 0 10px;
        }

        .navItem {
          display: flex;
          align-items: center;
          padding: 12px 0;
          cursor: pointer;
          border-radius: 8px;
          margin-bottom: 4px;
          transition: all 0.2s;
          position: relative;
        }

        .sidebar.collapsed .navItem {
          justify-content: center;
          padding: 12px;
        }

        .navItem:hover {
          background: #404040;
          transform: translateX(2px);
        }

        .navItem.active {
          background: #00d4ff20;
          color: #00d4ff;
          box-shadow: 0 2px 8px rgba(0, 212, 255, 0.2);
        }

        .navItem.active::before {
          content: '';
          position: absolute;
          left: -20px;
          top: 50%;
          transform: translateY(-50%);
          width: 3px;
          height: 24px;
          background: #00d4ff;
          border-radius: 0 2px 2px 0;
        }

        .sidebar.collapsed .navItem.active::before {
          left: -10px;
        }

        .navIconContainer {
          position: relative;
          display: flex;
          align-items: center;
        }

        .navIcon {
          width: 20px;
          height: 20px;
          margin-right: 12px;
          color: #888;
          transition: color 0.2s;
        }

        .sidebar.collapsed .navIcon {
          margin-right: 0;
        }

        .navItem.active .navIcon {
          color: #00d4ff;
        }

        .navItem:hover .navIcon {
          color: #00d4ff;
        }

        .navLabel {
          font-size: 14px;
          flex: 1;
          transition: opacity 0.3s ease;
        }

        .sidebar.collapsed .navLabel {
          display: none;
        }

        .badge {
          border-radius: 10px;
          font-size: 10px;
          font-weight: 600;
          padding: 2px 6px;
          margin-left: auto;
        }

        .badge.number {
          background: #ff4444;
          color: white;
          min-width: 18px;
          text-align: center;
        }

        .badge.text {
          background: #00ff88;
          color: #003d1a;
        }

        .sidebar.collapsed .badge {
          position: absolute;
          top: -2px;
          right: -2px;
          margin-left: 0;
        }

        .sidebarFooter {
          padding: 0 20px;
          margin-top: auto;
        }

        .sidebar.collapsed .sidebarFooter {
          padding: 0 10px;
        }

        .userProfile {
          display: flex;
          align-items: center;
          padding: 12px 0;
          margin-bottom: 16px;
          border-top: 1px solid #404040;
          padding-top: 16px;
        }

        .sidebar.collapsed .userProfile {
          justify-content: center;
        }

        .userAvatar {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: #00d4ff;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: 600;
          font-size: 14px;
          margin-right: 12px;
          flex-shrink: 0;
        }

        .sidebar.collapsed .userAvatar {
          margin-right: 0;
        }

        .userInfo {
          display: flex;
          flex-direction: column;
          flex: 1;
        }

        .userName {
          font-size: 14px;
          font-weight: 500;
          color: white;
        }

        .userStatus {
          font-size: 12px;
          color: #00ff88;
        }

        .emergencyButton {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          background: #ff4444;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
          justify-content: center;
        }

        .sidebar.collapsed .emergencyButton {
          padding: 12px;
        }

        .emergencyButton:hover {
          background: #ff6666;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3);
        }

        .emergencyIcon {
          width: 20px;
          height: 20px;
          margin-right: 12px;
        }

        .sidebar.collapsed .emergencyIcon {
          margin-right: 0;
        }

        .mainContent {
          flex: 1;
          display: flex;
          flex-direction: column;
          background: #f8f9fa;
          color: #333;
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 30px;
          background: white;
          border-bottom: 1px solid #e0e0e0;
        }

        .title {
          font-size: 24px;
          font-weight: 600;
          margin: 0;
          color: #333;
        }

        .languageSelector {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 12px;
          border: 1px solid #e0e0e0;
          border-radius: 6px;
          cursor: pointer;
        }

        .globeIcon {
          width: 16px;
          height: 16px;
          color: #666;
        }

        .chatArea {
          flex: 1;
          display: flex;
          flex-direction: column;
          padding: 20px 30px;
        }

        .messagesContainer {
          flex: 1;
          overflow-y: auto;
          margin-bottom: 20px;
          padding-right: 10px;
        }

        .messagesContainer::-webkit-scrollbar {
          width: 6px;
        }

        .messagesContainer::-webkit-scrollbar-track {
          background: #f1f1f1;
          border-radius: 3px;
        }

        .messagesContainer::-webkit-scrollbar-thumb {
          background: #c1c1c1;
          border-radius: 3px;
        }

        .messagesContainer::-webkit-scrollbar-thumb:hover {
          background: #a8a8a8;
        }

        .symptomButtons {
          display: flex;
          gap: 12px;
          margin-bottom: 20px;
          flex-wrap: wrap;
        }

        .quickSymptomsTitle {
          width: 100%;
          font-size: 14px;
          font-weight: 600;
          color: #666;
          margin-bottom: 10px;
        }

        .symptomButton {
          padding: 10px 16px;
          border: 1px solid #e0e0e0;
          border-radius: 20px;
          background: white;
          color: #666;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }

        .symptomButton:hover {
          border-color: #00d4ff;
          color: #00d4ff;
        }

        .symptomButton.selected {
          background: #00d4ff;
          border-color: #00d4ff;
          color: white;
        }

        .inputArea {
          margin-top: auto;
        }

        .inputContainer {
          display: flex;
          align-items: center;
          background: white;
          border: 1px solid #e0e0e0;
          border-radius: 25px;
          padding: 8px 12px;
          gap: 8px;
        }

        .textInput {
          flex: 1;
          border: none;
          outline: none;
          padding: 8px 12px;
          font-size: 14px;
          background: transparent;
        }

        .textInput::placeholder {
          color: #999;
        }

        .micButton, .sendButton {
          width: 36px;
          height: 36px;
          border: none;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .micButton {
          background: #f0f0f0;
        }

        .micButton:hover {
          background: #e0e0e0;
        }

        .sendButton {
          background: #00d4ff;
        }

        .sendButton:hover {
          background: #00b8e6;
        }

        .micIcon {
          width: 16px;
          height: 16px;
          color: #666;
        }

        .sendIcon {
          width: 16px;
          height: 16px;
          color: white;
        }

        .sendButton:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        .analysisPanel {
          width: 320px;
          background: white;
          border-left: 1px solid #e0e0e0;
          display: flex;
          flex-direction: column;
          transition: width 0.3s ease;
        }

        .analysisPanel.expanded {
          width: 400px;
        }

        .analysisHeader {
          padding: 20px;
          border-bottom: 1px solid #e0e0e0;
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .analysisHeader h3 {
          margin: 0;
          font-size: 16px;
          color: #333;
        }

        .analysisStatus {
          font-size: 12px;
          color: #999;
          font-weight: 500;
          letter-spacing: 0.5px;
        }

        .analysisContent {
          padding: 20px;
          flex: 1;
        }

        .noDataText {
          color: #999;
          font-size: 14px;
          margin: 0;
        }

        .analysisStatus {
          font-size: 10px;
          color: #999;
          font-weight: 500;
          letter-spacing: 0.5px;
          max-width: 120px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        @media (max-width: 1024px) {
          .sidebar.collapsed {
            width: 80px;
          }
          
          .analysisPanel {
            width: 280px;
          }
          
          .analysisPanel.expanded {
            width: 320px;
          }
        }

        @media (max-width: 768px) {
          .dashboard {
            position: relative;
          }
          
          .sidebar {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            z-index: 1000;
            transform: translateX(-100%);
            transition: transform 0.3s ease;
          }
          
          .sidebar:not(.collapsed) {
            transform: translateX(0);
          }
          
          .sidebar.collapsed {
            width: 60px;
            transform: translateX(0);
          }
          
          .mainContent {
            margin-left: 60px;
          }
          
          .analysisPanel {
            position: fixed;
            top: 0;
            right: 0;
            height: 100vh;
            width: 100%;
            max-width: 320px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 999;
          }
          
          .analysisPanel.expanded {
            transform: translateX(0);
            width: 100%;
            max-width: 400px;
          }
          
          .header {
            padding: 15px 20px;
          }
          
          .chatArea {
            padding: 15px 20px;
          }
          
          .symptomButtons {
            flex-direction: column;
            align-items: stretch;
          }
          
          .symptomButton {
            text-align: center;
            margin-bottom: 8px;
          }
        }

        @media (max-width: 480px) {
          .mainContent {
            margin-left: 50px;
          }
          
          .sidebar.collapsed {
            width: 50px;
          }
          
          .sidebar.collapsed .logo {
            padding: 0 5px 20px;
          }
          
          .sidebar.collapsed .navigation {
            padding: 0 5px;
          }
          
          .sidebar.collapsed .sidebarFooter {
            padding: 0 5px;
          }
          
          .sidebar.collapsed .navItem {
            padding: 8px;
          }
          
          .sidebar.collapsed .userAvatar {
            width: 28px;
            height: 28px;
            font-size: 12px;
          }
          
          .header {
            padding: 12px 15px;
          }
          
          .chatArea {
            padding: 10px 15px;
          }
          
          .inputContainer {
            padding: 6px 10px;
          }
          
          .micButton, .sendButton {
            width: 32px;
            height: 32px;
          }
        }
      `}</style>
    </div>
  );
};

// Analysis Panel Component
const AnalysisPanel = ({ analysis }) => {
  const { topDisease, recommendations, severity, confidence, detectedSymptoms } = analysis;

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'low': return '#22c55e';
      case 'medium': return '#eab308';
      case 'high': return '#f97316';
      case 'critical': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="analysisDetails">
      <div className="severityIndicator" style={{ borderColor: getSeverityColor(severity) }}>
        <h4>Severity: <span style={{ color: getSeverityColor(severity) }}>{severity.toUpperCase()}</span></h4>
        <p>Confidence: {Math.round(confidence)}%</p>
      </div>

      <div className="symptomsDetected">
        <h5>Detected Symptoms:</h5>
        <div className="symptomTags">
          {detectedSymptoms.map((symptom, index) => (
            <span key={index} className="symptomTag">{symptom}</span>
          ))}
        </div>
      </div>

      <div className="diseaseInfo">
        <h5>Possible Condition:</h5>
        <p className="diseaseName">{topDisease.name}</p>
        <p className="diseaseDesc">{topDisease.description}</p>
      </div>

      <div className="actionRequired">
        <h5>Recommended Action:</h5>
        <p className="actionText" style={{ color: getSeverityColor(severity) }}>
          {recommendations.action}
        </p>
      </div>

      <style jsx>{`
        .analysisDetails {
          font-size: 12px;
          line-height: 1.4;
        }

        .severityIndicator {
          border-left: 4px solid;
          padding-left: 12px;
          margin-bottom: 16px;
        }

        .severityIndicator h4 {
          margin: 0 0 4px 0;
          font-size: 13px;
          font-weight: 600;
        }

        .severityIndicator p {
          margin: 0;
          color: #666;
          font-size: 11px;
        }

        .symptomsDetected,
        .diseaseInfo,
        .actionRequired {
          margin-bottom: 16px;
        }

        .symptomsDetected h5,
        .diseaseInfo h5,
        .actionRequired h5 {
          margin: 0 0 8px 0;
          font-size: 12px;
          font-weight: 600;
          color: #333;
        }

        .symptomTags {
          display: flex;
          flex-wrap: wrap;
          gap: 4px;
        }

        .symptomTag {
          background: #e0f2fe;
          color: #0277bd;
          padding: 2px 6px;
          border-radius: 10px;
          font-size: 10px;
          font-weight: 500;
        }

        .diseaseName {
          margin: 0 0 4px 0;
          font-weight: 600;
          color: #333;
          text-transform: capitalize;
        }

        .diseaseDesc {
          margin: 0;
          color: #666;
          font-size: 11px;
        }

        .actionText {
          margin: 0;
          font-weight: 600;
          font-size: 12px;
        }
      `}</style>
    </div>
  );
};

export default Dashboard;