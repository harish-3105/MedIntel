/**
 * ChatPage - Main orchestrator for MedIntel chat interface
 * 
 * BACKEND INTEGRATION POINTS:
 * 1. POST /api/v1/chat - Send message and get AI response
 *    Body: { question, context, model_provider, student_mode, mode }
 *    Response: { summary, answer, risk_level, confidence, emotion, next_steps, citations }
 * 
 * 2. POST /api/v1/upload - Upload and parse files (PDF/image/audio)
 *    FormData: { file }
 *    Response: { id, filename, extractedText, labs, riskAssessment }
 * 
 * 3. GET /api/v1/history - Fetch chat history
 * 4. GET /api/v1/report/{id} - Fetch specific report
 * 
 * DEMO FLOW:
 * Step 1: Click "Upload" → select sample PDF from public/assets/
 * Step 2: Type "Explain my hemoglobin levels"
 * Step 3: Toggle to "Student Mode" and ask "How does HbA1c work?"
 */

import axios from 'axios';
import { useEffect, useMemo, useState } from 'react';
import ChatCenter from '../components/ChatCenter.jsx';
import RightPanel from '../components/RightPanel.jsx';
import Sidebar from '../components/Sidebar.jsx';
import { chatModes } from '../data/dummyData.js';
import useLocalStore from '../hooks/useLocalStore.js';
import useSTT from '../hooks/useSTT.js';
import useTTS from '../hooks/useTTS.js';

// Configure axios to use Vite proxy
axios.defaults.baseURL = '';

function ChatPage() {
  const [activeMode, setActiveMode] = useState('medical');
  const [messages, setMessages] = useState([]);
  const [currentReport, setCurrentReport] = useState(null);
  const [isThinking, setIsThinking] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [rightPanelCollapsed, setRightPanelCollapsed] = useState(false);

  const { speak, cancel, speaking, supported: ttsSupported } = useTTS();
  const {
    transcript,
    interimTranscript,
    listening,
    startListening,
    stopListening,
    resetTranscript,
    supported: sttSupported,
  } = useSTT();

  const {
    chats,
    activeChat,
    setActiveChat,
    saveChat,
    deleteChat,
    renameChat,
    getUserProfile,
    getSessionId,
  } = useLocalStore();

  // Load demo data on mount
  useEffect(() => {
    // Only show chats that exist in localStorage
    // Don't automatically load dummy data
    if (!activeChat && chats.length > 0) {
      const firstChat = chats[0];
      setActiveChat(firstChat);
      setMessages(firstChat.messages || []);
      setActiveMode(firstChat.mode);
    }
  }, [chats, activeChat, setActiveChat]);

  // Compute latest risk level
  const latestRisk = useMemo(() => {
    for (let i = messages.length - 1; i >= 0; i -= 1) {
      if (messages[i].riskLevel) {
        return messages[i].riskLevel;
      }
    }
    return 'Green';
  }, [messages]);

  // Handle sending messages
  const handleSendMessage = async (text, attachments = []) => {
    if (!text?.trim()) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsThinking(true);

    try {
      // Build conversation history for context (last 10 messages)
      const conversationHistory = messages.slice(-10).map(msg => ({
        role: msg.role,
        content: msg.content,
      }));

      // Call backend API
      const response = await axios.post('/api/v1/chat', {
        question: text,
        context: currentReport?.extractedText || '',
        conversation_history: conversationHistory,
        model_provider: activeMode === 'student' ? 'openai' : 'gemini',
        student_mode: activeMode === 'student',
        mode: activeMode,
        session_id: getSessionId(),
        user_profile: getUserProfile(),
      });

      // Handle model response - just show the structured response
      handleModelResponse(response.data);

    } catch (error) {
      console.error('Chat error:', error);
      console.error('Error details:', error.response?.data || error.message);
      
      const fallback = {
        id: crypto.randomUUID(),
        role: 'assistant',
        summary: 'Connection Error',
        content:
          `Unable to connect to the backend. Please ensure the backend server is running on http://127.0.0.1:8000. Error: ${error.message}`,
        emotion: 'neutral',
        riskLevel: 'Green',
        confidence: 'N/A',
        nextSteps: ['Check backend is running', 'Verify API configuration', 'Try again'],
        sources: ['System'],
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, fallback]);
    } finally {
      setIsThinking(false);
    }
  };

  // Handle model response - only show the full structured message (no duplication)
  const handleModelResponse = (resp) => {
    // Create structured message with all metadata
    const structuredMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      summary: resp.summary || '',
      content: resp.answer || resp.content || '',
      emotion: resp.emotion || 'neutral',
      riskLevel: resp.risk_level || 'Green',
      confidence: resp.confidence || 'N/A',
      nextSteps: resp.next_steps || [],
      sources: resp.citations || [],
      analysis: resp.analysis || null,  // Include structured analysis data
      timestamp: new Date().toISOString(),
    };

    // Add the message
    setMessages((prev) => [...prev, structuredMessage]);
    
    // Speak the response
    if (structuredMessage.content) {
      speak(structuredMessage.content);
    }
  };



  // Simulate streaming token-by-token response
  const simulateStreamingResponse = async (question) => {
    const demoResponse = {
      id: crypto.randomUUID(),
      role: 'assistant',
      summary: 'Analysis complete.',
      content: `Based on your question "${question}", here is a comprehensive medical insight. This is a simulated response demonstrating the streaming capability. In production, this would connect to Groq/Gemini/OpenAI for real-time medical analysis with proper citations and risk scoring.`,
      emotion: 'supportive',
      riskLevel: 'Green',
      confidence: '0.85',
      sources: ['Demo Knowledge Base', 'MedIntel Training Data'],
      nextSteps: [
        'Review provided information',
        'Consult with healthcare provider if needed',
        'Track symptoms in MedIntel journal',
      ],
      timestamp: new Date().toISOString(),
    };

    // Create partial message for streaming effect
    const streamingMessage = {
      ...demoResponse,
      content: '',
    };

    setMessages((prev) => [...prev, streamingMessage]);

    const words = demoResponse.content.split(' ');
    for (let i = 0; i < words.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 50));
      setMessages((prev) => {
        const updated = [...prev];
        const lastMessage = updated[updated.length - 1];
        lastMessage.content = words.slice(0, i + 1).join(' ');
        return updated;
      });
    }

    // Finalize message
    setMessages((prev) => {
      const updated = [...prev];
      updated[updated.length - 1] = demoResponse;
      return updated;
    });
  };

  // Handle file uploads
  const handleFileUpload = async (files) => {
    if (!files?.length) return;
    const file = files[0];

    // Validate file type
    const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF, image (JPG/PNG), DOCX, or text file');
      return;
    }

    // Show processing state
    setCurrentReport({
      id: crypto.randomUUID(),
      filename: file.name,
      extractedText: 'Processing upload...',
      labs: [],
      uploadedAt: new Date().toISOString(),
    });

    // Add user message about file upload
    const uploadMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: `📎 Uploaded: ${file.name}`,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, uploadMessage]);

    try {
      // Upload file to backend
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post('/api/v1/analyze/report/file', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Update report with actual data
      const reportData = {
        id: crypto.randomUUID(),
        filename: file.name,
        extractedText: response.data.extracted_text || '',
        labs: response.data.lab_results || [],
        riskAssessment: response.data.risk_assessment || {},
        summary: response.data.summary || '',
        uploadedAt: new Date().toISOString(),
      };
      setCurrentReport(reportData);

      // Add AI response with analysis
      const analysisMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        summary: response.data.summary || 'Medical Report Analysis',
        content: response.data.analysis || 'Report analyzed successfully. You can now ask questions about it.',
        riskLevel: response.data.risk_assessment?.overall_risk || 'Green',
        confidence: 'High',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, analysisMessage]);

      // Speak the analysis
      if (analysisMessage.content) {
        speak(analysisMessage.content);
      }

    } catch (error) {
      console.error('Upload error:', error);
      
      const errorDetail = error.response?.data?.detail || error.message;
      let errorContent = `❌ Failed to analyze file: ${errorDetail}`;
      
      // Provide helpful suggestions based on error
      if (errorDetail.includes('OCR') || errorDetail.includes('Image')) {
        errorContent += '\n\n💡 **Suggestions:**\n- Upload a **PDF** file for best results\n- Ensure images are clear and high quality\n- Try a different file format';
      }
      
      // Add error message
      const errorMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: errorContent,
        riskLevel: 'Red',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      
      setCurrentReport(null);
    }
  };

  // Handle medical imaging (X-ray, CT scan) analysis
  const handleMedicalImaging = async (files) => {
    if (!files?.length) return;
    const file = files[0];

    // Validate file type - must be image
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file (JPG, PNG) for medical imaging analysis');
      return;
    }

    // Add user message about imaging upload
    const uploadMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: `🩻 Analyzing medical image: ${file.name}`,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, uploadMessage]);

    // Add thinking state
    setIsThinking(true);

    try {
      // Upload image to medical imaging endpoint
      const formData = new FormData();
      formData.append('file', file);
      formData.append('image_type', 'xray'); // Default to X-ray

      const response = await axios.post('/api/v1/analyze/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const analysis = response.data.analysis;

      // Format findings as a structured message
      let analysisContent = `**Medical Imaging Analysis Complete**\n\n`;
      analysisContent += `**Image Type:** ${analysis.image_type.toUpperCase()}\n\n`;

      if (analysis.findings && analysis.findings.length > 0) {
        analysisContent += `**Findings:**\n`;
        analysis.findings.forEach((finding, idx) => {
          analysisContent += `${idx + 1}. **${finding.condition}** (Confidence: ${(finding.confidence * 100).toFixed(0)}%)\n`;
          analysisContent += `   ${finding.description}\n\n`;
        });
      }

      if (analysis.full_analysis) {
        analysisContent += `**Detailed Analysis:**\n${analysis.full_analysis}\n\n`;
      }

      if (analysis.recommendations && analysis.recommendations.length > 0) {
        analysisContent += `**Recommendations:**\n`;
        analysis.recommendations.forEach((rec, idx) => {
          analysisContent += `${idx + 1}. ${rec}\n`;
        });
        analysisContent += '\n';
      }

      analysisContent += `\n${analysis.disclaimer || '⚠️ This is an AI-assisted analysis. Always consult with a qualified radiologist or physician.'}`;

      // Add AI response with imaging analysis
      const analysisMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        summary: 'Medical Imaging Analysis',
        content: analysisContent,
        riskLevel: 'Yellow', // Imaging always needs professional review
        confidence: 'High',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, analysisMessage]);

      // Speak summary
      if (analysis.summary) {
        speak(analysis.summary);
      }

    } catch (error) {
      console.error('Medical imaging error:', error);
      
      const errorMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `❌ Failed to analyze medical image: ${error.response?.data?.detail || error.message}\n\n💡 **Tips:**\n- Ensure image is clear and properly oriented\n- Use JPEG or PNG format\n- File should be a medical image (X-ray, CT scan)`,
        riskLevel: 'Red',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleChatSelect = (chat) => {
    setActiveChat(chat);
    setMessages(chat.messages || []);
    setActiveMode(chat.mode || 'medical');
    cancel(); // Stop any ongoing TTS
  };

  const handleDeleteChat = (chatId) => {
    deleteChat(chatId);
    
    // Clear messages if we deleted the active chat
    if (activeChat?.id === chatId) {
      setMessages([]);
      
      // Select the first remaining chat if available
      const remainingChats = chats.filter(c => c.id !== chatId);
      if (remainingChats.length > 0) {
        handleChatSelect(remainingChats[0]);
      }
    }
  };

  const handleNewChat = () => {
    const newChat = {
      id: crypto.randomUUID(),
      title: 'New conversation',
      lastMessage: '',
      timestamp: 'Just now',
      mode: activeMode,
      messages: [],
    };
    setActiveChat(newChat);
    setMessages([]);
    setCurrentReport(null);
  };

  const handlePlayAudio = (text) => {
    if (!ttsSupported || !text) return;
    speak(text);
  };

  return (
    <div className="flex h-full w-full bg-bg-dark text-white">
      <div className="heartbeat-line" aria-hidden="true"></div>

      {/* Left Sidebar */}
      <Sidebar
        chats={chats}
        modes={chatModes}
        activeMode={activeMode}
        onModeChange={setActiveMode}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
        onRenameChat={renameChat}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Center Chat Area */}
      <ChatCenter
        messages={messages}
        isThinking={isThinking}
        activeMode={activeMode}
        onSendMessage={handleSendMessage}
        onFileUpload={handleFileUpload}
        onMedicalImaging={handleMedicalImaging}
        onPlayAudio={handlePlayAudio}
        onStopAudio={cancel}
        speaking={speaking}
        listening={listening}
        onMicToggle={listening ? stopListening : startListening}
        transcript={transcript}
        interimTranscript={interimTranscript}
        onClearTranscript={resetTranscript}
        sttSupported={sttSupported}
        ttsSupported={ttsSupported}
      />

      {/* Right Report Panel */}
      <RightPanel
        report={currentReport}
        riskLevel={latestRisk}
        collapsed={rightPanelCollapsed}
        onToggleCollapse={() => setRightPanelCollapsed(!rightPanelCollapsed)}
      />
    </div>
  );
}

export default ChatPage;
