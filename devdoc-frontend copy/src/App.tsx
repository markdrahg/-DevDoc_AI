import { useState } from 'react';
import { UploadPage } from './pages/UploadPage';
import { ResultsPage } from './pages/ResultsPage';

export default function App() {
  const [showResults, setShowResults] = useState(false);

  const handleSubmit = (data: any) => {
    console.log('Submitted:', data);
    setShowResults(true);
  };

  const handleBack = () => {
    setShowResults(false);
  };

  return (
    <>
      {!showResults ? (
        <UploadPage onSubmit={handleSubmit} />
      ) : (
        <ResultsPage onBack={handleBack} />
      )}
    </>
  );
}
