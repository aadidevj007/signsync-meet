import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Eye } from 'lucide-react';

const CaptionOverlay = ({ captions, participants, currentUser }) => {
  const getParticipantInfo = (userId) => {
    if (userId === currentUser?.uid) {
      return {
        name: currentUser?.displayName || 'You',
        photo: currentUser?.photoURL || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'
      };
    }
    
    const participant = participants.find(p => p.id === userId);
    return {
      name: participant?.displayName || 'Unknown User',
      photo: participant?.avatarURL || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face'
    };
  };

  const getTypeIcon = (type) => {
    return type === 'voice' ? (
      <Mic className="w-4 h-4 text-blue-500" />
    ) : (
      <Eye className="w-4 h-4 text-green-500" />
    );
  };

  const getTypeColor = (type) => {
    return type === 'voice' ? 'border-blue-200 bg-blue-50' : 'border-green-200 bg-green-50';
  };

  return (
    <div className="absolute bottom-20 left-4 right-4 pointer-events-none">
      <div className="max-w-4xl mx-auto">
        <AnimatePresence>
          {captions.map((caption, index) => {
            const participantInfo = getParticipantInfo(caption.userId);
            
            return (
              <motion.div
                key={caption.id}
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.9 }}
                transition={{ 
                  duration: 0.3,
                  delay: index * 0.1
                }}
                className={`mb-3 caption-bubble ${getTypeColor(caption.type)}`}
                style={{
                  animationDelay: `${index * 0.1}s`
                }}
              >
                <div className="flex items-start space-x-3">
                  <img
                    src={participantInfo.photo}
                    alt={participantInfo.name}
                    className="w-8 h-8 rounded-full object-cover flex-shrink-0"
                  />
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-medium text-gray-800 text-sm">
                        {participantInfo.name}
                      </span>
                      {getTypeIcon(caption.type)}
                      <span className="text-xs text-gray-500">
                        {caption.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                    
                    <p className="text-gray-700 text-sm leading-relaxed">
                      {caption.text}
                    </p>
                    
                    {caption.language !== 'en' && (
                      <div className="mt-1">
                        <span className="inline-block px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                          {caption.language.toUpperCase()}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default CaptionOverlay;
