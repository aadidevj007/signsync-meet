import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Mic, 
  MicOff, 
  Video, 
  VideoOff, 
  Phone, 
  Settings, 
  Users,
  MessageSquare,
  Globe,
  Eye,
  EyeOff,
  Volume2,
  VolumeX
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import JitsiMeet from '../components/JitsiMeet';
import CaptionOverlay from '../components/CaptionOverlay';
import LanguageSelector from '../components/LanguageSelector';
import toast from 'react-hot-toast';

const Meeting = () => {
  const { roomId } = useParams();
  const navigate = useNavigate();
  const { currentUser, userProfile } = useAuth();
  
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOff, setIsVideoOff] = useState(false);
  const [showCaptions, setShowCaptions] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [captions, setCaptions] = useState([]);
  const [participants, setParticipants] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  const jitsiRef = useRef(null);
  const captionServiceRef = useRef(null);

  useEffect(() => {
    if (!currentUser) {
      navigate('/');
      return;
    }

    // Initialize caption service
    initializeCaptionService();
    
    // Simulate loading
    setTimeout(() => setIsLoading(false), 2000);
  }, [currentUser, navigate]);

  const initializeCaptionService = () => {
    // This will be connected to the backend AI services
    captionServiceRef.current = {
      startVoiceRecognition: () => {
        console.log('Starting voice recognition...');
        // Connect to backend voice-to-text API
      },
      startSignRecognition: () => {
        console.log('Starting sign recognition...');
        // Connect to backend sign-to-text API
      },
      stopRecognition: () => {
        console.log('Stopping recognition...');
      }
    };
  };

  const handleMuteToggle = () => {
    setIsMuted(!isMuted);
    // Toggle Jitsi audio
    if (jitsiRef.current) {
      jitsiRef.current.executeCommand('toggleAudio');
    }
  };

  const handleVideoToggle = () => {
    setIsVideoOff(!isVideoOff);
    // Toggle Jitsi video
    if (jitsiRef.current) {
      jitsiRef.current.executeCommand('toggleVideo');
    }
  };

  const handleLeaveMeeting = () => {
    if (jitsiRef.current) {
      jitsiRef.current.dispose();
    }
    navigate('/');
  };

  const handleLanguageChange = (language) => {
    setSelectedLanguage(language);
    toast.success(`Language changed to ${getLanguageName(language)}`);
  };

  const getLanguageName = (code) => {
    const languages = {
      'en': 'English',
      'ta': 'Tamil',
      'ml': 'Malayalam',
      'te': 'Telugu'
    };
    return languages[code] || 'English';
  };

  const addCaption = (text, type, userId, userName, userPhoto) => {
    const newCaption = {
      id: Date.now() + Math.random(),
      text,
      type, // 'voice' or 'sign'
      userId,
      userName,
      userPhoto,
      timestamp: new Date(),
      language: selectedLanguage
    };
    
    setCaptions(prev => [...prev.slice(-9), newCaption]); // Keep last 10 captions
  };

  // Simulate receiving captions (this will be replaced with real AI integration)
  useEffect(() => {
    if (!showCaptions) return;

    const interval = setInterval(() => {
      const sampleCaptions = [
        { text: "Hello everyone, how are you doing?", type: "voice" },
        { text: "Thank you for joining the meeting", type: "sign" },
        { text: "Can you hear me clearly?", type: "voice" },
        { text: "Yes, I can hear you perfectly", type: "voice" }
      ];
      
      const randomCaption = sampleCaptions[Math.floor(Math.random() * sampleCaptions.length)];
      addCaption(
        randomCaption.text,
        randomCaption.type,
        currentUser?.uid || 'demo-user',
        currentUser?.displayName || 'Demo User',
        currentUser?.photoURL || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'
      );
    }, 5000);

    return () => clearInterval(interval);
  }, [showCaptions, currentUser, selectedLanguage]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white text-lg">Joining meeting...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-white text-xl font-semibold">
            SignSync Meet - {roomId}
          </h1>
          <div className="flex items-center space-x-2 text-sm text-gray-300">
            <Users className="w-4 h-4" />
            <span>{participants.length + 1} participants</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <LanguageSelector
            selectedLanguage={selectedLanguage}
            onLanguageChange={handleLanguageChange}
          />
          
          <button
            onClick={() => setShowCaptions(!showCaptions)}
            className={`p-2 rounded-lg transition-colors ${
              showCaptions 
                ? 'bg-primary-600 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
            title={showCaptions ? 'Hide Captions' : 'Show Captions'}
          >
            {showCaptions ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
          </button>
          
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors"
            title="Settings"
          >
            <Settings className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Video Area */}
        <div className="flex-1 relative">
          <JitsiMeet
            ref={jitsiRef}
            roomName={roomId}
            userInfo={{
              displayName: currentUser?.displayName || 'User',
              email: currentUser?.email || ''
            }}
            onParticipantsChange={setParticipants}
          />
          
          {/* Caption Overlay */}
          <AnimatePresence>
            {showCaptions && (
              <CaptionOverlay
                captions={captions}
                participants={participants}
                currentUser={currentUser}
              />
            )}
          </AnimatePresence>
        </div>

        {/* Settings Panel */}
        <AnimatePresence>
          {showSettings && (
            <motion.div
              initial={{ x: 300, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 300, opacity: 0 }}
              className="w-80 bg-gray-800 border-l border-gray-700 p-6"
            >
              <h3 className="text-white text-lg font-semibold mb-4">Meeting Settings</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-gray-300 text-sm mb-2">Audio Input</label>
                  <select className="w-full bg-gray-700 text-white rounded-lg px-3 py-2 border border-gray-600">
                    <option>Default Microphone</option>
                    <option>External Microphone</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-gray-300 text-sm mb-2">Video Input</label>
                  <select className="w-full bg-gray-700 text-white rounded-lg px-3 py-2 border border-gray-600">
                    <option>Default Camera</option>
                    <option>External Camera</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-gray-300 text-sm mb-2">Caption Language</label>
                  <select 
                    value={selectedLanguage}
                    onChange={(e) => handleLanguageChange(e.target.value)}
                    className="w-full bg-gray-700 text-white rounded-lg px-3 py-2 border border-gray-600"
                  >
                    <option value="en">English</option>
                    <option value="ta">Tamil</option>
                    <option value="ml">Malayalam</option>
                    <option value="te">Telugu</option>
                  </select>
                </div>
                
                <div className="pt-4 border-t border-gray-700">
                  <h4 className="text-gray-300 text-sm font-medium mb-2">AI Features</h4>
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2 text-gray-300">
                      <input type="checkbox" defaultChecked className="rounded" />
                      <span className="text-sm">Voice Recognition</span>
                    </label>
                    <label className="flex items-center space-x-2 text-gray-300">
                      <input type="checkbox" defaultChecked className="rounded" />
                      <span className="text-sm">Sign Language Recognition</span>
                    </label>
                    <label className="flex items-center space-x-2 text-gray-300">
                      <input type="checkbox" defaultChecked className="rounded" />
                      <span className="text-sm">Real-time Translation</span>
                    </label>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Controls */}
      <div className="bg-gray-800 px-6 py-4">
        <div className="flex items-center justify-center space-x-4">
          <button
            onClick={handleMuteToggle}
            className={`p-3 rounded-full transition-all ${
              isMuted 
                ? 'bg-red-600 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
            title={isMuted ? 'Unmute' : 'Mute'}
          >
            {isMuted ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
          </button>
          
          <button
            onClick={handleVideoToggle}
            className={`p-3 rounded-full transition-all ${
              isVideoOff 
                ? 'bg-red-600 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
            title={isVideoOff ? 'Turn on Camera' : 'Turn off Camera'}
          >
            {isVideoOff ? <VideoOff className="w-6 h-6" /> : <Video className="w-6 h-6" />}
          </button>
          
          <button
            onClick={handleLeaveMeeting}
            className="p-3 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors"
            title="Leave Meeting"
          >
            <Phone className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Meeting;
