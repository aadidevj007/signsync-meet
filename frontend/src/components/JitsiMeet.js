import React, { useEffect, useRef, forwardRef, useImperativeHandle } from 'react';

const JitsiMeet = forwardRef(({ roomName, userInfo, onParticipantsChange }, ref) => {
  const jitsiContainerRef = useRef(null);
  const jitsiApiRef = useRef(null);

  useImperativeHandle(ref, () => ({
    executeCommand: (command) => {
      if (jitsiApiRef.current) {
        jitsiApiRef.current.executeCommand(command);
      }
    },
    dispose: () => {
      if (jitsiApiRef.current) {
        jitsiApiRef.current.dispose();
      }
    }
  }));

  useEffect(() => {
    const loadJitsiScript = () => {
      return new Promise((resolve, reject) => {
        if (window.JitsiMeetExternalAPI) {
          resolve();
          return;
        }

        const script = document.createElement('script');
        script.src = 'https://meet.jit.si/external_api.js';
        script.async = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    };

    const initializeJitsi = async () => {
      try {
        await loadJitsiScript();
        
        const options = {
          roomName: roomName,
          width: '100%',
          height: '100%',
          parentNode: jitsiContainerRef.current,
          userInfo: {
            displayName: userInfo.displayName,
            email: userInfo.email
          },
          configOverwrite: {
            startWithAudioMuted: false,
            startWithVideoMuted: false,
            enableWelcomePage: false,
            prejoinPageEnabled: false,
            disableModeratorIndicator: true,
            startScreenSharing: false,
            enableEmailInStats: false
          },
          interfaceConfigOverwrite: {
            TOOLBAR_BUTTONS: [
              'microphone', 'camera', 'closedcaptions', 'desktop', 'fullscreen',
              'fodeviceselection', 'hangup', 'profile', 'chat', 'recording',
              'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
              'videoquality', 'filmstrip', 'invite', 'feedback', 'stats', 'shortcuts',
              'tileview', 'videobackgroundblur', 'download', 'help', 'mute-everyone', 'security'
            ],
            SETTINGS_SECTIONS: ['devices', 'language', 'moderator', 'profile', 'calendar'],
            SHOW_JITSI_WATERMARK: false,
            SHOW_WATERMARK_FOR_GUESTS: false,
            SHOW_BRAND_WATERMARK: false,
            SHOW_POWERED_BY: false,
            SHOW_POLICY_WATERMARK: false,
            SHOW_LOBBY_BUTTON: true,
            AUDIO_LEVEL_PRIMARY_COLOR: 'rgba(59, 130, 246, 0.5)',
            AUDIO_LEVEL_SECONDARY_COLOR: 'rgba(59, 130, 246, 0.2)'
          }
        };

        jitsiApiRef.current = new window.JitsiMeetExternalAPI('meet.jit.si', options);

        // Event listeners
        jitsiApiRef.current.addEventListeners({
          readyToClose: () => {
            console.log('Jitsi ready to close');
          },
          participantLeft: (participant) => {
            console.log('Participant left:', participant);
            updateParticipants();
          },
          participantJoined: (participant) => {
            console.log('Participant joined:', participant);
            updateParticipants();
          },
          videoConferenceJoined: () => {
            console.log('Video conference joined');
            updateParticipants();
          },
          videoConferenceLeft: () => {
            console.log('Video conference left');
          },
          audioMuteStatusChanged: (data) => {
            console.log('Audio mute status changed:', data);
          },
          videoMuteStatusChanged: (data) => {
            console.log('Video mute status changed:', data);
          }
        });

      } catch (error) {
        console.error('Error initializing Jitsi:', error);
      }
    };

    const updateParticipants = () => {
      if (jitsiApiRef.current && onParticipantsChange) {
        const participants = jitsiApiRef.current.getParticipantsInfo();
        onParticipantsChange(participants);
      }
    };

    if (roomName && userInfo) {
      initializeJitsi();
    }

    return () => {
      if (jitsiApiRef.current) {
        jitsiApiRef.current.dispose();
      }
    };
  }, [roomName, userInfo, onParticipantsChange]);

  return (
    <div 
      ref={jitsiContainerRef} 
      className="w-full h-full"
      style={{ minHeight: '500px' }}
    />
  );
});

JitsiMeet.displayName = 'JitsiMeet';

export default JitsiMeet;
