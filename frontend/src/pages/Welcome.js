import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  Video, 
  Users, 
  Mic, 
  Eye, 
  Globe, 
  ArrowRight,
  Play,
  Sparkles,
  Shield,
  Zap
} from 'lucide-react';
import AuthModal from '../components/AuthModal';
import TeamSection from '../components/TeamSection';

const Welcome = () => {
  const navigate = useNavigate();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login');

  const handleCreateMeeting = () => {
    setShowAuthModal(true);
    setAuthMode('login');
  };

  const handleJoinMeeting = () => {
    const roomId = prompt('Enter Meeting ID:');
    if (roomId) {
      navigate(`/meeting/${roomId}`);
    }
  };

  const features = [
    {
      icon: <Mic className="w-8 h-8" />,
      title: "Voice-to-Text",
      description: "Real-time speech recognition in multiple languages"
    },
    {
      icon: <Eye className="w-8 h-8" />,
      title: "Sign-to-Text",
      description: "AI-powered sign language recognition and translation"
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: "Multilingual",
      description: "Support for English, Tamil, Malayalam, and Telugu"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Collaborative",
      description: "Seamless video conferencing with Jitsi Meet"
    }
  ];

  const benefits = [
    {
      icon: <Shield className="w-6 h-6" />,
      text: "Secure & Private"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      text: "Real-time Processing"
    },
    {
      icon: <Sparkles className="w-6 h-6" />,
      text: "AI-Powered"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="relative z-10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2"
          >
            <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
              <Video className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
              SignSync Meet
            </span>
          </motion.div>
          
          <motion.button
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={() => setShowAuthModal(true)}
            className="btn-primary"
          >
            Get Started
          </motion.button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-6 py-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-8"
            >
              <h1 className="text-6xl md:text-7xl font-bold mb-6">
                <span className="bg-gradient-to-r from-primary-600 via-purple-600 to-blue-600 bg-clip-text text-transparent">
                  SignSync Meet
                </span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
                AI-Powered Video Conferencing with Real-Time Captions
                <br />
                <span className="text-lg text-gray-500">Breaking barriers through technology</span>
              </p>
            </motion.div>

            {/* Benefits */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex flex-wrap justify-center gap-6 mb-12"
            >
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-center space-x-2 text-gray-600">
                  {benefit.icon}
                  <span className="font-medium">{benefit.text}</span>
                </div>
              ))}
            </motion.div>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <button
                onClick={handleCreateMeeting}
                className="btn-primary text-lg px-8 py-4 flex items-center space-x-2 group"
              >
                <Video className="w-5 h-5" />
                <span>Create Meeting</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <button
                onClick={handleJoinMeeting}
                className="btn-secondary text-lg px-8 py-4 flex items-center space-x-2"
              >
                <Users className="w-5 h-5" />
                <span>Join Meeting</span>
              </button>
            </motion.div>
          </div>

          {/* Demo Video Section */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="relative max-w-4xl mx-auto"
          >
            <div className="glass-card rounded-3xl p-8 shadow-2xl">
              <div className="aspect-video bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl flex items-center justify-center relative overflow-hidden">
                <div className="text-center text-white">
                  <Play className="w-16 h-16 mx-auto mb-4 opacity-80" />
                  <h3 className="text-2xl font-semibold mb-2">See SignSync Meet in Action</h3>
                  <p className="text-gray-300">Watch how AI-powered captions make meetings accessible</p>
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
              Powerful Features
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience the future of accessible video conferencing
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="glass-card rounded-2xl p-6 text-center hover:shadow-2xl transition-all duration-300 group"
              >
                <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center text-white mx-auto mb-4 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <TeamSection />

      {/* Footer */}
      <footer className="px-6 py-12 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <Video className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold">SignSync Meet</span>
          </div>
          <p className="text-gray-400 mb-6">
            Making video conferencing accessible for everyone through AI technology
          </p>
          <div className="flex justify-center space-x-6 text-sm text-gray-500">
            <span>© 2024 SignSync Team</span>
            <span>•</span>
            <span>Privacy Policy</span>
            <span>•</span>
            <span>Terms of Service</span>
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      {showAuthModal && (
        <AuthModal
          isOpen={showAuthModal}
          onClose={() => setShowAuthModal(false)}
          mode={authMode}
          onModeChange={setAuthMode}
        />
      )}
    </div>
  );
};

export default Welcome;
