import { useState } from 'react';
import { UploadPage } from './pages/UploadPage';
import { ResultsPage } from './pages/ResultsPage';

export default function App() {
  const [showResults, setShowResults] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [showSuccessBanner, setShowSuccessBanner] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleSubmit = (data: any) => {
    console.log('Submitted:', data);
    setIsGenerating(true);
    
    // Simulate the 8-second loading process from RepositoryInput
    setTimeout(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setShowResults(true);
        setIsTransitioning(false);
        setIsGenerating(false);
        // Show success banner after results are displayed
        setTimeout(() => {
          setShowSuccessBanner(true);
          // Auto-dismiss banner after 3 seconds
          setTimeout(() => {
            setShowSuccessBanner(false);
          }, 3000);
        }, 500);
      }, 300);
    }, 8000);
  };

  const handleBack = () => {
    setIsTransitioning(true);
    setShowSuccessBanner(false);
    setTimeout(() => {
      setShowResults(false);
      setIsTransitioning(false);
    }, 300);
  };

  return (
    <div className="relative overflow-hidden">
      <div
        className={`transition-all duration-300 ${
          isTransitioning ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
        }`}
      >
        {!showResults ? (
          <UploadPage onSubmit={handleSubmit} isGenerating={isGenerating} />
        ) : (
          <ResultsPage onBack={handleBack} showSuccessBanner={showSuccessBanner} />
        )}
      </div>
    </div>
  );
}
