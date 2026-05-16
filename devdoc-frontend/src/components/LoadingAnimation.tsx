import { useEffect, useState } from 'react';

interface LoadingAnimationProps {
  messages?: string[];
  typingSpeed?: number;
}

export function LoadingAnimation({ 
  messages = [
    'Analyzing repository structure...',
    'Processing code files...',
    'Generating documentation...',
    'Almost there...'
  ],
  typingSpeed = 50
}: LoadingAnimationProps) {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    const currentMessage = messages[currentMessageIndex];
    
    if (isTyping && displayedText.length < currentMessage.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(currentMessage.slice(0, displayedText.length + 1));
      }, typingSpeed);
      return () => clearTimeout(timeout);
    } else if (displayedText.length === currentMessage.length) {
      const timeout = setTimeout(() => {
        if (currentMessageIndex < messages.length - 1) {
          setIsTyping(false);
          setDisplayedText('');
          setCurrentMessageIndex(prev => prev + 1);
          setIsTyping(true);
        }
      }, 1500);
      return () => clearTimeout(timeout);
    }
  }, [displayedText, currentMessageIndex, isTyping, messages, typingSpeed]);

  return (
    <div className="flex flex-col items-center justify-center space-y-8 p-8">
      {/* Animated spinner */}
      <div className="relative">
        <div className="w-16 h-16 border-4 border-primary/20 rounded-full"></div>
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>

      {/* Typing text with cursor */}
      <div className="text-center space-y-2">
        <div className="flex items-center justify-center gap-1 min-h-[32px]">
          <span className="text-lg font-medium text-foreground">
            {displayedText}
          </span>
          <span className="inline-block w-0.5 h-5 bg-primary animate-pulse"></span>
        </div>
        
        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2 mt-4">
          {messages.map((_, index) => (
            <div
              key={index}
              className={`h-2 rounded-full transition-all duration-300 ${
                index === currentMessageIndex
                  ? 'w-8 bg-primary'
                  : index < currentMessageIndex
                  ? 'w-2 bg-primary/50'
                  : 'w-2 bg-border'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// Made with Bob
